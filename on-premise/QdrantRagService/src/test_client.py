import requests
import json
import time
from typing import List, Dict, Any

class RAGTestClient:
    def __init__(self, service_url: str = "http://localhost:8001"):
        self.service_url = service_url
    
    def check_health(self) -> bool:
        """Проверка работоспособности сервиса"""
        try:
            response = requests.get(f"{self.service_url}/health")
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ Service is healthy: {health_data}")
                return health_data.get("status") == "healthy"
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Получение информации о коллекции"""
        try:
            response = requests.get(f"{self.service_url}/collection/info")
            if response.status_code == 200:
                info = response.json()
                print(f"📊 Collection info: {info}")
                return info
            else:
                print(f"❌ Failed to get collection info: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ Error getting collection info: {e}")
            return {}
    
    def search(self, query: str, top_k: int = 5, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Поиск по запросу"""
        try:
            payload = {
                "query": query,
                "top_k": top_k,
                "threshold": threshold
            }
            
            response = requests.post(
                f"{self.service_url}/search",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"🔍 Search results for '{query}':")
                print(f"   Total found: {result['total_found']}")
                
                for i, res in enumerate(result['results'], 1):
                    print(f"   {i}. Score: {res['score']:.3f}")
                    print(f"      Text: {res['text']}")
                    if res.get('metadata'):
                        print(f"      Metadata: {res['metadata']}")
                    print()
                
                return result['results']
            else:
                print(f"❌ Search failed: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def add_document(self, text: str, metadata: Dict[str, Any] = None) -> bool:
        """Добавление одного документа"""
        try:
            payload = {
                "text": text,
                "metadata": metadata or {}
            }
            
            response = requests.post(
                f"{self.service_url}/add_document",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Document added: {result}")
                return True
            else:
                print(f"❌ Failed to add document: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error adding document: {e}")
            return False
    
    def clear_collection(self) -> bool:
        """Очистка коллекции"""
        try:
            response = requests.delete(f"{self.service_url}/collection/clear")
            if response.status_code == 200:
                print("✅ Collection cleared successfully")
                return True
            else:
                print(f"❌ Failed to clear collection: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error clearing collection: {e}")
            return False
    
    def run_interactive_search(self):
        """Интерактивный режим поиска"""
        print("🚀 Interactive RAG Search Mode")
        print("Type 'quit' to exit, 'info' for collection info, 'clear' to clear collection")
        print("-" * 50)
        
        while True:
            try:
                query = input("\n🔍 Enter your search query: ").strip()
                
                if query.lower() == 'quit':
                    print("👋 Goodbye!")
                    break
                elif query.lower() == 'info':
                    self.get_collection_info()
                    continue
                elif query.lower() == 'clear':
                    self.clear_collection()
                    continue
                elif not query:
                    continue
                
                # Выполнение поиска
                results = self.search(query, top_k=3, threshold=0.3)
                
                if not results:
                    print("❌ No relevant documents found. Try a different query or lower the threshold.")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def run_comprehensive_test():
    """Запуск комплексного теста RAG системы"""
    client = RAGTestClient()
    
    print("🧪 Starting comprehensive RAG system test...")
    print("=" * 50)
    
    # 1. Проверка здоровья
    print("\n1. Health Check")
    if not client.check_health():
        print("❌ Service is not healthy. Please check if the service is running.")
        return
    
    # 2. Информация о коллекции
    print("\n2. Collection Info")
    client.get_collection_info()
    
    # 3. Добавление тестовых документов
    print("\n3. Adding test documents")
    test_docs = [
        {
            "text": "Искусственный интеллект (ИИ) - это область компьютерных наук, которая занимается созданием интеллектуальных машин, способных работать и реагировать как люди.",
            "metadata": {"category": "AI", "topic": "definition"}
        },
        {
            "text": "Машинное обучение является подмножеством искусственного интеллекта, которое фокусируется на алгоритмах, позволяющих компьютерам учиться без явного программирования.",
            "metadata": {"category": "ML", "topic": "definition"}
        },
        {
            "text": "Глубокое обучение - это подкласс машинного обучения, основанный на искусственных нейронных сетях с множественными слоями между входными и выходными слоями.",
            "metadata": {"category": "DL", "topic": "definition"}
        }
    ]
    
    for doc in test_docs:
        client.add_document(doc["text"], doc["metadata"])
        time.sleep(0.5)  # Небольшая пауза между добавлениями
    
    # 4. Информация о коллекции после добавления
    print("\n4. Collection Info after adding documents")
    client.get_collection_info()
    
    # 5. Тестирование поиска
    print("\n5. Testing search functionality")
    test_queries = [
        "что такое искусственный интеллект",
        "машинное обучение алгоритмы",
        "нейронные сети глубокое обучение",
        "computer science AI"
    ]
    
    for query in test_queries:
        print(f"\n--- Testing query: '{query}' ---")
        client.search(query, top_k=2, threshold=0.3)
        time.sleep(1)
    
    print("\n✅ Comprehensive test completed!")
    print("=" * 50)
    client.clear_collection()
    
def main():
    """Основная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description="RAG System Test Client")
    parser.add_argument("--service-url", type=str, default="http://localhost:8001", help="RAG service URL")
    parser.add_argument("--test", action='store_true', help="Run comprehensive test")
    parser.add_argument("--interactive", action='store_true', help="Run interactive search mode")
    parser.add_argument("--query", type=str, help="Single search query")
    
    args = parser.parse_args()
    
    client = RAGTestClient(args.service_url)
    
    if args.test:
        run_comprehensive_test()
    elif args.interactive:
        client.run_interactive_search()
    elif args.query:
        client.search(args.query)
    else:
        # По умолчанию запускаем быструю проверку
        client.check_health()
        client.get_collection_info()

if __name__ == "__main__":
    main()