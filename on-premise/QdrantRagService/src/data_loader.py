import json
import csv
import os
import asyncio
from pathlib import Path
from typing import List, Dict, Any
import requests
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, service_url: str = "http://localhost:8000"):
        self.service_url = service_url
        
    def load_from_json(self, file_path: str) -> List[Dict[str, Any]]:
        """Загрузка данных из JSON файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            documents = []
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        text = item.get('text', str(item))
                        metadata = {k: v for k, v in item.items() if k != 'text'}
                        documents.append({
                            "text": text,
                            "metadata": metadata
                        })
                    else:
                        documents.append({
                            "text": str(item),
                            "metadata": {}
                        })
            else:
                documents.append({
                    "text": str(data),
                    "metadata": {}
                })
            
            return documents
            
        except Exception as e:
            logger.error(f"Error loading JSON file {file_path}: {e}")
            return []
    
    def load_from_csv(self, file_path: str, text_column: str = None) -> List[Dict[str, Any]]:
        """Загрузка данных из CSV файла"""
        try:
            documents = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if text_column and text_column in row:
                        text = row[text_column]
                        metadata = {k: v for k, v in row.items() if k != text_column}
                    else:
                        # Если колонка не указана, используем первую колонку как текст
                        columns = list(row.keys())
                        text = row[columns[0]] if columns else ""
                        metadata = {k: v for k, v in row.items() if k != columns[0]} if len(columns) > 1 else {}
                    
                    documents.append({
                        "text": text,
                        "metadata": metadata
                    })
            
            return documents
            
        except Exception as e:
            logger.error(f"Error loading CSV file {file_path}: {e}")
            return []
    
    def load_from_txt(self, file_path: str, chunk_size: int = 1000) -> List[Dict[str, Any]]:
        """Загрузка данных из текстового файла с разбивкой на чанки"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            documents = []
            # Разбиваем текст на чанки
            for i in range(0, len(content), chunk_size):
                chunk = content[i:i + chunk_size]
                if chunk.strip():  # Пропускаем пустые чанки
                    documents.append({
                        "text": chunk.strip(),
                        "metadata": {
                            "source_file": os.path.basename(file_path),
                            "chunk_index": i // chunk_size,
                            "char_start": i,
                            "char_end": min(i + chunk_size, len(content))
                        }
                    })
            
            return documents
            
        except Exception as e:
            logger.error(f"Error loading TXT file {file_path}: {e}")
            return []
    
    def upload_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Загрузка документов в RAG сервис"""
        try:
            response = requests.post(
                f"{self.service_url}/add_documents",
                json=documents,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Successfully uploaded {result.get('added_count', 0)} documents")
                return True
            else:
                logger.error(f"Error uploading documents: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error uploading documents: {e}")
            return False
    
    def load_and_upload_file(self, file_path: str, file_type: str = None, **kwargs) -> bool:
        """Загрузка и отправка файла в RAG сервис"""
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
        
        # Определение типа файла
        if file_type is None:
            file_extension = Path(file_path).suffix.lower()
            if file_extension == '.json':
                file_type = 'json'
            elif file_extension == '.csv':
                file_type = 'csv'
            elif file_extension in ['.txt', '.md']:
                file_type = 'txt'
            else:
                logger.error(f"Unsupported file type: {file_extension}")
                return False
        
        # Загрузка документов в зависимости от типа
        if file_type == 'json':
            documents = self.load_from_json(file_path)
        elif file_type == 'csv':
            text_column = kwargs.get('text_column')
            documents = self.load_from_csv(file_path, text_column)
        elif file_type == 'txt':
            chunk_size = kwargs.get('chunk_size', 1000)
            documents = self.load_from_txt(file_path, chunk_size)
        else:
            logger.error(f"Unsupported file type: {file_type}")
            return False
        
        if not documents:
            logger.warning(f"No documents loaded from {file_path}")
            return False
        
        logger.info(f"Loaded {len(documents)} documents from {file_path}")
        
        # Загрузка в сервис батчами
        batch_size = 50
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            if not self.upload_documents(batch):
                logger.error(f"Failed to upload batch {i // batch_size + 1}")
                return False
            logger.info(f"Uploaded batch {i // batch_size + 1}/{(len(documents) - 1) // batch_size + 1}")
        
        return True
    
    def load_sample_data(self) -> bool:
        """Загрузка примеров данных для тестирования"""
        sample_documents = [
            {
                "text": "Машинное обучение — это метод анализа данных, который автоматизирует построение аналитических моделей.",
                "metadata": {"category": "AI", "language": "ru"}
            },
            {
                "text": "Python — высокоуровневый язык программирования общего назначения с динамической типизацией.",
                "metadata": {"category": "Programming", "language": "ru"}
            },
            {
                "text": "Qdrant — это векторная база данных с открытым исходным кодом, написанная на Rust.",
                "metadata": {"category": "Database", "language": "ru"}
            },
            {
                "text": "FastAPI — современный, быстрый веб-фреймворк для создания API с Python 3.6+.",
                "metadata": {"category": "Web Development", "language": "ru"}
            },
            {
                "text": "Docker — это платформа для разработки, доставки и запуска приложений в контейнерах.",
                "metadata": {"category": "DevOps", "language": "ru"}
            }
        ]
        
        return self.upload_documents(sample_documents)

def main():
    """Основная функция для работы с загрузчиком данных"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Data Loader for RAG Service")
    parser.add_argument("--file", type=str, help="Path to data file")
    parser.add_argument("--type", type=str, choices=['json', 'csv', 'txt'], help="File type")
    parser.add_argument("--text-column", type=str, help="Text column name for CSV files")
    parser.add_argument("--chunk-size", type=int, default=1000, help="Chunk size for TXT files")
    parser.add_argument("--sample", action='store_true', help="Load sample data")
    parser.add_argument("--service-url", type=str, default="http://localhost:8000", help="RAG service URL")
    
    args = parser.parse_args()
    
    loader = DataLoader(args.service_url)
    
    if args.sample:
        logger.info("Loading sample data...")
        if loader.load_sample_data():
            logger.info("Sample data loaded successfully!")
        else:
            logger.error("Failed to load sample data")
            return
    
    if args.file:
        logger.info(f"Loading data from {args.file}...")
        kwargs = {}
        if args.text_column:
            kwargs['text_column'] = args.text_column
        if args.chunk_size:
            kwargs['chunk_size'] = args.chunk_size
            
        if loader.load_and_upload_file(args.file, args.type, **kwargs):
            logger.info("Data loaded successfully!")
        else:
            logger.error("Failed to load data")

if __name__ == "__main__":
    main()