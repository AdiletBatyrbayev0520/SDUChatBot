import argparse
import logging

from .src.chunker import LLMChunker, ChunkConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="LLM Chunker CLI")
    parser.add_argument("--input", dest="input_json", required=True, help="Path to input slides JSON (from vlm_parser)")
    parser.add_argument("--output", dest="output_json", required=True, help="Path to output chunks JSON")
    parser.add_argument("--model", dest="model", default=None, help="Override model name")
    parser.add_argument("--lang", dest="language", default=None, help="ru|en")
    args = parser.parse_args()

    cfg = ChunkConfig()
    if args.model:
        cfg.model = args.model
    if args.language:
        cfg.language = args.language

    chunker = LLMChunker(cfg)
    chunks = chunker.chunk_from_json_file(args.input_json)
    chunker.save_chunks_to_json(chunks, args.output_json)


if __name__ == "__main__":
    main()


