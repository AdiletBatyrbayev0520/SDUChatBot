.PHONY: help build up down restart logs clean test load-sample interactive search health info

# Цвета для вывода
GREEN=\033[0;32m
YELLOW=\033[1;33m
RED=\033[0;31m
NC=\033[0m # No Color

# Переменные
SERVICE_URL=http://localhost:8000
DOCKER_COMPOSE=docker-compose

help: ## Показать эту справку
	@echo "$(GREEN)Доступные команды:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Собрать Docker образы
	@echo "$(GREEN)Сборка Docker образов...$(NC)"
	$(DOCKER_COMPOSE) build

up: ## Запустить все сервисы
	@echo "$(GREEN)Запуск RAG системы...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)Ждем запуска сервисов...$(NC)"
	@sleep 10
	@make health

down: ## Остановить все сервисы
	@echo "$(YELLOW)Остановка сервисов...$(NC)"
	$(DOCKER_COMPOSE) down

restart: down up ## Перезапустить все сервисы

logs: ## Показать логи всех сервисов
	$(DOCKER_COMPOSE) logs -f

logs-rag: ## Показать логи RAG сервиса
	$(DOCKER_COMPOSE) logs -f rag-service

logs-qdrant: ## Показать логи Qdrant
	$(DOCKER_COMPOSE) logs -f qdrant

clean: ## Очистить данные и остановить сервисы
	@echo "$(RED)Очистка системы...$(NC)"
	$(DOCKER_COMPOSE) down -v
	@sudo rm -rf qdrant_storage/*
	@echo "$(GREEN)Система очищена$(NC)"

health: ## Проверить здоровье сервиса
	@echo "$(GREEN)Проверка здоровья сервиса...$(NC)"
	@python test_client.py --service-url $(SERVICE_URL)

info: ## Показать информацию о коллекции
	@echo "$(GREEN)Информация о коллекции:$(NC)"
	@curl -s $(SERVICE_URL)/collection/info | python -m json.tool

test: ## Запустить комплексный тест
	@echo "$(GREEN)Запуск комплексного теста...$(NC)"
	@python test_client.py --test --service-url $(SERVICE_URL)

load-sample: ## Загрузить примеры данных
	@echo "$(GREEN)Загрузка примеров данных...$(NC)"
	@python data_loader.py --sample --service-url $(SERVICE_URL)

interactive: ## Запустить интерактивный режим поиска
	@echo "$(GREEN)Запуск интерактивного режима поиска...$(NC)"
	@python test_client.py --interactive --service-url $(SERVICE_URL)

search: ## Выполнить поиск (использование: make search QUERY="ваш запрос")
	@echo "$(GREEN)Поиск: $(QUERY)$(NC)"
	@python test_client.py --query "$(QUERY)" --service-url $(SERVICE_URL)

load-json: ## Загрузить данные из JSON файла (использование: make load-json FILE=data.json)
	@echo "$(GREEN)Загрузка данных из $(FILE)...$(NC)"
	@python data_loader.py --file $(FILE) --type json --service-url $(SERVICE_URL)

load-csv: ## Загрузить данные из CSV файла (использование: make load-csv FILE=data.csv COLUMN=text)
	@echo "$(GREEN)Загрузка данных из $(FILE)...$(NC)"
	@python data_loader.py --file $(FILE) --type csv --text-column $(COLUMN) --service-url $(SERVICE_URL)

load-txt: ## Загрузить данные из TXT файла (использование: make load-txt FILE=data.txt)
	@echo "$(GREEN)Загрузка данных из $(FILE)...$(NC)"
	@python data_loader.py --file $(FILE) --type txt --service-url $(SERVICE_URL)

clear-collection: ## Очистить коллекцию документов
	@echo "$(YELLOW)Очистка коллекции...$(NC)"
	@curl -X DELETE $(SERVICE_URL)/collection/clear

dev-install: ## Установить зависимости для разработки
	@echo "$(GREEN)Установка зависимостей для разработки...$(NC)"
	@pip install -r requirements.txt

dev-run: ## Запустить только Qdrant и RAG сервис локально
	@echo "$(GREEN)Запуск Qdrant...$(NC)"
	@docker run -d --name qdrant-dev -p 6333:6333 -p 6334:6334 qdrant/qdrant:latest
	@echo "$(GREEN)Ждем запуска Qdrant...$(NC)"
	@sleep 5
	@echo "$(GREEN)Запуск RAG сервиса...$(NC)"
	@QDRANT_HOST=localhost QDRANT_PORT=6333 python main.py

dev-stop: ## Остановить dev окружение
	@echo "$(YELLOW)Остановка dev окружения...$(NC)"
	@docker stop qdrant-dev || true
	@docker rm qdrant-dev || true

status: ## Показать статус сервисов
	@echo "$(GREEN)Статус сервисов:$(NC)"
	@$(DOCKER_COMPOSE) ps

setup: build up load-sample ## Полная настройка системы с примерами данных
	@echo "$(GREEN)✅ RAG система готова к работе!$(NC)"
	@echo "$(YELLOW)📊 Веб-интерфейс Qdrant: http://localhost:6333/dashboard$(NC)"
	@echo "$(YELLOW)📚 API документация: http://localhost:8000/docs$(NC)"
	@echo "$(YELLOW)🔍 Интерактивный поиск: make interactive$(NC)"

# Алиасы для удобства
start: up
stop: down
reset: clean up