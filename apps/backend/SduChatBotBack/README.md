# SDU Chat Bot Backend
## О проекте
`SduChatBotBack` — это серверная часть, предоставляющий REST-API для чат-бота SDU. Сервис обрабатывает сообщения пользователей, интегрируется с Google OAuth и проксирует запросы к AI-модели SDU AI.
 
## Технологический стэк
| Технология | Версия | Назначение |
|------------|--------|------------|
| Java | 21 | Языковая платформа |
| Spring Boot | 3.5.x | Каркас приложения |
| Spring Security | — | JWT-аутентификация/авторизация |
| Spring Data JPA + Hibernate | — | Доступ к PostgreSQL |
| JJWT | 0.11.5 | Генерация/валидация JWT |
| MapStruct | 1.5.x | Типобезопасные мапперы DTO ↔ Entity |
| Feign Client | — | HTTP-интеграции (Google OAuth, SDU AI) |
| Lombok | — | Уменьшение бойлерплейта |
| SpringDoc OpenAPI | 2.x | Генерация Swagger UI |
| PostgreSQL | 15 | СУБД |
| Docker & Docker Compose | — | Контейнеризация |
| Gradle Kotlin DSL | — | Система сборки |

## Структура проекта
```
src/main/java/kz/sdu/chat/mainservice/
├─ config/          # Конфигурации Spring (Security, JPA, i18n, OpenAPI, AOP-логгер)
├─ constants/       # Общие константы и утилиты
├─ entities/        # JPA-сущности (с базовым аудитом)
├─ repositories/    # Spring Data репозитории
├─ mappers/         # MapStruct-мапперы Entity ↔ DTO
├─ services/
│  ├─ impl/         # Реализации бизнес-логики
│  └─ ...           # Интерфейсы сервисов
├─ rest/
│  ├─ controllers/  # REST-контроллеры
│  └─ dto/          # Запросы/ответы + пагинация и ошибки
├─ security/        # JWT-фильтр, CORS-фильтр, точка входа
├─ feign/           # Клиенты Google OAuth и SDU AI
└─ exceptions/      # Кастомные исключения и GlobalExceptionHandler
```

### Ключевые паттерны
- Layered Architecture (Controller → Service → Repository → DB)
- DTO/Mapper Pattern (отделение транспортных моделей от доменных)
- Repository Pattern (Spring Data)
- AOP-логирование и глобальная обработка ошибок
- Auditing через `AuditorAware` (+ `@CreatedDate`, `@LastModifiedDate`)

## Быстрый старт
### Предварительные требования
- Docker >= 20.10 и Compose
- JDK 21 (для локального запуска без контейнера)
- Gradle Wrapper поставляется в репозитории

### Запуск через Docker Compose (рекомендуется)
```bash
# из каталога SduChatBotBack
docker compose up -d --build
```
Доступ:
- API: http://localhost:8080/api
- Swagger UI: http://localhost:8080/api/swagger-ui.html

### Локальный запуск с Gradle
```bash
./gradlew bootRun
```
По умолчанию приложение ищет PostgreSQL на `localhost:5432`. Можно указать иной URL через переменную `SPRING_DATASOURCE_URL`.

## Переменные окружения
| Переменная | Значение по умолчанию | Описание |
|------------|-----------------------|----------|
| `SPRING_DATASOURCE_URL` | `jdbc:postgresql://localhost:5432/sduchat` | JDBC-строка БД |
| `SPRING_DATASOURCE_USERNAME` | `k_app` | Логин БД |
| `SPRING_DATASOURCE_PASSWORD` | `123` | Пароль БД |
| `GOOGLE_CLIENT_ID` | — | OAuth 2.0 client id |
| `GOOGLE_CLIENT_SECRET` | — | OAuth 2.0 secret |
| `GOOGLE_REDIRECT_URI` | — | Redirect URI фронтенда |
| `SDU_AI_API_KEY` | — | Токен доступа к SDU AI |
| `SDU_AI_API_URL` | — | URL Lambda-функции SDU AI |
| `JWT_SECRET_KEY` | _сгенерирован_ | Секрет для подписи JWT |

_Полный список смотрите в `src/main/resources/application.yml`._

## Тестирование
```
./gradlew test
```
Тесты используют Spring Boot Test и JUnit 5.

## CI/CD и развёртывание
- `Dockerfile` — многослойная сборка (gradle build → distroless-runtime).
- `Dockerrun.aws.json` — манифест для AWS Elastic Beanstalk.

## Лицензия
Проект распространяется под лицензией MIT (при необходимости изменить).
