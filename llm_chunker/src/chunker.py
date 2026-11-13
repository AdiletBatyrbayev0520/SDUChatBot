import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .utils.client import get_openai_client
from .utils.pricing import get_model_cost_per_pdf
from ..config import DEFAULT_MODEL

logger = logging.getLogger(__name__)


@dataclass
class ChunkConfig:
    model: str = DEFAULT_MODEL
    max_completion_tokens: int = 4000
    temperature: float = 0.1
    max_chunk_size: int = 1000
    min_chunk_size: int = 200
    overlap_size: int = 100
    preserve_structure: bool = True
    language: str = "en"


@dataclass
class Chunk:
    id: str
    content: str
    slide_num: int
    slide_title: str
    chunk_index: int
    total_chunks: int
    topic: str
    keywords: List[str]
    metadata: Dict[str, Any]


class LLMChunker:
    def __init__(self, config: Optional[ChunkConfig] = None):
        self.config = config or ChunkConfig()
        self.client = get_openai_client()
        if self.client is None:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        # Track token usage across all slides
        self._total_prompt_tokens: int = 0
        self._total_completion_tokens: int = 0

    def _get_chunking_prompt(self, content: str, slide_title: str) -> str:
        if self.config.language == "ru":
            return f"""
Ты эксперт по разбиению текста на семантические блоки для RAG системы.

ЗАДАЧА: Разбей содержимое слайда на логические чанки для поиска и извлечения информации.

СЛАЙД: "{slide_title}"
СОДЕРЖИМОЕ:
{content}

ПРАВИЛА РАЗБИЕНИЯ:
1. Каждый чанк должен быть семантически завершенным (завершенная мысль/тема)
2. Размер чанка: {self.config.min_chunk_size}-{self.config.max_chunk_size} символов
3. Сохраняй структуру: заголовки, списки, таблицы
4. Выделяй ключевые темы и ключевые слова для каждого чанка
5. Чанки должны перекрываться на {self.config.overlap_size} символов для контекста но чтобы при этом не терял контектса 

ВЕРНИ JSON в формате:
{{
  "chunks": [
    {{
      "content": "текст чанка",
      "topic": "основная тема чанка",
      "keywords": ["ключевое", "слово1", "слово2"],
      "chunk_type": "text|table|list|header"
    }}
  ]
}}
"""
        return f"""
You are an expert at breaking text into semantic chunks for RAG systems.

TASK: Break down slide content into logical chunks for search and information retrieval.

SLIDE: "{slide_title}"
CONTENT:
{content}

CHUNKING RULES:
1. Each chunk should be semantically complete (complete thought/topic)
2. Chunk size: {self.config.min_chunk_size}-{self.config.max_chunk_size} characters
3. Preserve structure: headers, lists, tables
4. Extract key topics and keywords for each chunk
5. Chunks should overlap by {self.config.overlap_size} characters for context

RETURN JSON in format:
{{
  "chunks": [
    {{
      "content": "chunk text",
      "topic": "main topic of chunk",
      "keywords": ["key", "word1", "word2"],
      "chunk_type": "text|table|list|header"
    }}
  ]
}}
"""

    def _call_openai_chunker(self, content: str, slide_title: str) -> Dict[str, Any]:
        prompt = self._get_chunking_prompt(content, slide_title)
        response = self.client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            max_completion_tokens=self.config.max_completion_tokens,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are an expert at semantic text chunking for RAG systems. Always return valid JSON."},
                {"role": "user", "content": prompt},
            ],
        )
        # accumulate usage if available
        usage = getattr(response, "usage", None)
        if usage is not None:
            self._total_prompt_tokens += int(getattr(usage, "prompt_tokens", 0) or 0)
            self._total_completion_tokens += int(getattr(usage, "completion_tokens", 0) or 0)
        result = response.choices[0].message.content
        if not result:
            raise ValueError("Empty response from OpenAI")
        return json.loads(result)

    def _create_chunks_with_overlap(self, llm_chunks: List[Dict], slide_num: int, slide_title: str) -> List[Chunk]:
        chunks: List[Chunk] = []
        for i, chunk_data in enumerate(llm_chunks):
            chunk_id = f"slide_{slide_num}_chunk_{i+1}"
            chunks.append(
                Chunk(
                    id=chunk_id,
                    content=chunk_data["content"],
                    slide_num=slide_num,
                    slide_title=slide_title,
                    chunk_index=i + 1,
                    total_chunks=len(llm_chunks),
                    topic=chunk_data.get("topic", ""),
                    keywords=chunk_data.get("keywords", []),
                    metadata={
                        "chunk_type": chunk_data.get("chunk_type", "text"),
                        "original_slide_title": slide_title,
                        "processing_model": self.config.model,
                        "language": self.config.language,
                    },
                )
            )
        return chunks

    def chunk_slide(self, slide_data: Dict[str, Any]) -> List[Chunk]:
        slide_num = slide_data["slide_num"]
        slide_title = slide_data["title"]
        content = slide_data["content"]
        logger.info(f"Chunking slide {slide_num}: {slide_title}")

        if len(content) <= self.config.max_chunk_size:
            return [
                Chunk(
                    id=f"slide_{slide_num}_chunk_1",
                    content=content,
                    slide_num=slide_num,
                    slide_title=slide_title,
                    chunk_index=1,
                    total_chunks=1,
                    topic=slide_title,
                    keywords=slide_title.split(),
                    metadata={
                        "chunk_type": "text",
                        "original_slide_title": slide_title,
                        "processing_model": self.config.model,
                        "language": self.config.language,
                        "single_chunk": True,
                    },
                )
            ]

        try:
            llm_result = self._call_openai_chunker(content, slide_title)
            llm_chunks = llm_result.get("chunks", [])
            if not llm_chunks:
                logger.warning(f"No chunks returned for slide {slide_num}")
                return []
            return self._create_chunks_with_overlap(llm_chunks, slide_num, slide_title)
        except Exception as error:
            logger.error(f"Error chunking slide {slide_num}: {error}")
            return self._fallback_chunking(content, slide_num, slide_title)

    def _fallback_chunking(self, content: str, slide_num: int, slide_title: str) -> List[Chunk]:
        sentences = content.split('. ')
        chunks: List[Chunk] = []
        current_chunk = ""
        chunk_index = 1
        for sentence in sentences:
            if len(current_chunk + sentence) > self.config.max_chunk_size and current_chunk:
                chunks.append(
                    Chunk(
                        id=f"slide_{slide_num}_chunk_{chunk_index}",
                        content=current_chunk.strip(),
                        slide_num=slide_num,
                        slide_title=slide_title,
                        chunk_index=chunk_index,
                        total_chunks=0,
                        topic=slide_title,
                        keywords=slide_title.split(),
                        metadata={
                            "chunk_type": "text",
                            "original_slide_title": slide_title,
                            "processing_model": "fallback",
                            "language": self.config.language,
                            "fallback_chunking": True,
                        },
                    )
                )
                current_chunk = sentence
                chunk_index += 1
            else:
                current_chunk += sentence + ". "

        if current_chunk.strip():
            chunks.append(
                Chunk(
                    id=f"slide_{slide_num}_chunk_{chunk_index}",
                    content=current_chunk.strip(),
                    slide_num=slide_num,
                    slide_title=slide_title,
                    chunk_index=chunk_index,
                    total_chunks=chunk_index,
                    topic=slide_title,
                    keywords=slide_title.split(),
                    metadata={
                        "chunk_type": "text",
                        "original_slide_title": slide_title,
                        "processing_model": "fallback",
                        "language": self.config.language,
                        "fallback_chunking": True,
                    },
                )
            )

        for chunk in chunks:
            chunk.total_chunks = len(chunks)
        return chunks

    def chunk_slides(self, slides_data: List[Dict[str, Any]]) -> List[Chunk]:
        all_chunks: List[Chunk] = []
        for slide_data in slides_data:
            try:
                all_chunks.extend(self.chunk_slide(slide_data))
            except Exception as error:
                logger.error(f"Failed to chunk slide {slide_data.get('slide_num', 'unknown')}: {error}")
        logger.info(f"Total chunks created: {len(all_chunks)}")
        return all_chunks

    def chunk_from_json_file(self, json_file_path: str) -> List[Chunk]:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        slides = data.get("slides", [])
        if not slides:
            logger.warning("No slides found in JSON file")
            return []
        return self.chunk_slides(slides)

    def save_chunks_to_json(self, chunks: List[Chunk], output_path: str):
        chunks_data: List[Dict[str, Any]] = []
        for chunk in chunks:
            chunks_data.append({
                "id": chunk.id,
                "content": chunk.content,
                "slide_num": chunk.slide_num,
                "slide_title": chunk.slide_title,
                "chunk_index": chunk.chunk_index,
                "total_chunks": chunk.total_chunks,
                "topic": chunk.topic,
                "keywords": chunk.keywords,
                "metadata": chunk.metadata,
            })

        total_cost_usd = get_model_cost_per_pdf(
            model=self.config.model,
            total_input_tokens=self._total_prompt_tokens,
            total_output_tokens=self._total_completion_tokens,
        )

        output_data = {
            "chunks": chunks_data,
            "total_chunks": len(chunks_data),
            "processing_info": {
                "model": self.config.model,
                "language": self.config.language,
                "max_chunk_size": self.config.max_chunk_size,
                "min_chunk_size": self.config.min_chunk_size,
                "overlap_size": self.config.overlap_size,
                "total_prompt_tokens": self._total_prompt_tokens,
                "total_completion_tokens": self._total_completion_tokens,
                "total_cost_usd": total_cost_usd,
            },
        }
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        logger.info(f"Chunks saved to: {output_path}")


