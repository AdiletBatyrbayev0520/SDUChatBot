# SDU AI Chatbot Platform

## Product Overview

The SDU AI Chatbot Platform is a comprehensive, intelligent conversational system designed for Suleyman Demirel University (SDU). This MVP provides multiple interfaces (web, Telegram, on-premise) for students, faculty, and staff to access university information, services, and support through AI-powered conversations. The platform leverages advanced RAG (Retrieval-Augmented Generation) technology, combining large language models with a curated knowledge base to deliver accurate, contextual, and multilingual responses.

## Problem and Solution

### The Problem

University students, staff, and prospective applicants face several challenges:
- Difficulty finding accurate, up-to-date information about academic policies, procedures, and services
- Overwhelming and hard-to-navigate static documentation
- Limited availability of support staff for routine inquiries
- Language barriers for international students
- Time-consuming bureaucratic processes for common requests

### The Solution

The SDU AI Chatbot Platform provides:
- **24/7 Availability**: Instant access to information at any time
- **Multilingual Support**: Responses in English, Kazakh, Russian, Turkish, and German
- **Contextual Understanding**: Maintains conversation history for natural interactions
- **Multiple Interfaces**: Web application, Telegram bot, and on-premise deployment options
- **Accurate Information**: Draws from official SDU documents and policies
- **Service Integration**: Direct access to forms, payments, and administrative services
- **Conversation Versioning**: Tree-based chat history for exploring different conversation paths

## Target Users

- **Current Students**: Seeking information about courses, policies, services, and campus life
- **Prospective Students**: Inquiring about admission requirements, programs, and facilities
- **Faculty and Staff**: Accessing administrative procedures, policies, and resources
- **International Students**: Requiring multilingual assistance with university processes
- **Parents and Guardians**: Getting information about university services and student support
- **Administrators**: Managing user interactions and monitoring system usage

## Tech Stack

### Frontend Applications

**Web Application (SduChatBotFront)**
- React 19.1.0 - Modern UI library
- TypeScript 5.8.3 - Type-safe development
- Vite 6.3.5 - Fast build tool and dev server
- React Router 7.6.2 - Client-side routing
- Redux Toolkit 2.8.2 - State management with RTK Query
- Tailwind CSS 4.1.10 - Utility-first styling
- Axios 1.10.0 - HTTP client
- Docker & Nginx - Production deployment

**Chat Versioning Interface (SDUBot-ChatVersioning-Beta)**
- React 18.2.0 - UI framework
- Tailwind CSS 3.4.1 - Styling
- Tree-based conversation structure
- Version navigation and branching

### Backend Services

**REST API Backend (SduChatBotBack)**
- Java 21 - Language platform
- Spring Boot 3.5.0 - Application framework
- Spring Security - JWT authentication/authorization
- Spring Data JPA + Hibernate - Database access
- PostgreSQL 15 - Primary database
- JJWT 0.11.5 - JWT token management
- MapStruct 1.5.2 - DTO mapping
- SpringDoc OpenAPI 2.8.9 - API documentation
- Docker & Docker Compose - Containerization
- Gradle Kotlin DSL - Build system

### AI Services

**AWS Lambda Chatbot Service**
- Python 3.8+ - Programming language
- AWS Lambda - Serverless compute
- Amazon Bedrock - AI/ML service
- Claude 3.7 Sonnet - Language model
- Cohere Rerank v3.5 - Document reranking
- Amazon DynamoDB - Chat history storage
- Amazon S3 - Knowledge base storage
- Boto3 - AWS SDK

**On-Premise AI Service (LocalChatBotService)**
- Python 3.12 - Core language
- LangChain - RAG implementation
- OpenAI GPT-4 - Fine-tuned model
- ChromaDB - Vector database
- FastAPI - API framework
- PostgreSQL - Structured data storage

**RAG Service (QdrantRagService)**
- Python 3.13 - Programming language
- FastAPI - Web framework
- Qdrant - Vector database
- sentence-transformers - Embedding model (paraphrase-multilingual-MiniLM-L12-v2)
- Docker & Docker Compose - Deployment

### Telegram Bot Interface

**TelegramBotUI**
- Python 3.12 - Core language
- aiogram 3.20 - Telegram Bot API framework
- SQLite/PostgreSQL - User management
- aiohttp - HTTP client for AI integration
- Docker - Containerization

## System Requirements

### Development Environment
- **Node.js**: 18.x or higher (for frontend)
- **Java**: JDK 21 (for backend)
- **Python**: 3.8+ (AWS), 3.12+ (on-premise), 3.13+ (RAG service)
- **Docker**: Latest version with Docker Compose
- **PostgreSQL**: 15+ (for backend and on-premise services)
- **Git**: For version control

### Production Environment
- **Memory**: Minimum 8GB RAM (16GB recommended)
- **Storage**: 10GB+ free space
- **AWS Account**: For cloud deployment (Lambda, Bedrock, DynamoDB, S3)
- **Modern Web Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

## Running the Project Locally

### 1. Clone the Repository

```bash
git clone <repository-url>
cd sdu-chatbot-platform
```

### 2. Frontend Setup (Web Application)

```bash
cd frontend/SduChatBotFront

# Install dependencies
npm install

# Create environment file
cat > .env << EOF
VITE_API_URL=http://localhost:8080/api
EOF

# Start development server
npm run dev
# Access at http://localhost:5173

# Or use Docker
docker-compose up
```

### 3. Backend Setup (REST API)

```bash
cd backend/SduChatBotBack

# Set environment variables
export SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/sduchat
export SPRING_DATASOURCE_USERNAME=k_app
export SPRING_DATASOURCE_PASSWORD=123
export GOOGLE_CLIENT_ID=your_google_client_id
export GOOGLE_CLIENT_SECRET=your_google_client_secret
export SDU_AI_API_KEY=your_sdu_ai_api_key
export SDU_AI_API_URL=your_lambda_url

# Run with Docker (recommended)
docker-compose up -d --build
# Access API at http://localhost:8080/api
# Swagger UI at http://localhost:8080/api/swagger-ui.html

# Or run locally with Gradle
./gradlew bootRun
```

### 4. AWS Lambda Chatbot Service

```bash
cd aws/ChatBotService

# Install dependencies
pip install boto3 python-dotenv

# Create .env file
cp .env.example .env
# Edit .env with your AWS resource IDs:
# KNOWLEDGE_BASE_ID, MODEL_ID, REGION_NAME, etc.

# Configure AWS credentials
aws configure

# Test locally
python lambda_function.py

# Deploy to AWS Lambda
zip -r deployment.zip lambda_function.py
aws lambda update-function-code --function-name sdu-chatbot --zip-file fileb://deployment.zip
```

### 5. On-Premise AI Service

```bash
cd on-premise/LocalChatBotService

# Using Docker (recommended)
cd tgbot
docker build -t sdubot-telegram .
docker run --env-file .env sdubot-telegram

# Or local setup
cd model
pip install -r requirements.txt
python model_rag.py
```

### 6. RAG Service

```bash
cd on-premise/QdrantRagService

# Start with Docker Compose
docker-compose up -d

# Verify installation
curl http://localhost:8000/health

# Load sample data
python src/data_loader.py --file data/documents.json

# Test search
python src/test_client.py --query "machine learning"

# Access API docs at http://localhost:8000/docs
```

### 7. Telegram Bot

```bash
cd on-premise/TelegramBotUI

# Create .env file
cp .env_example .env
# Add your BOT_TOKEN from @BotFather

# Run with Docker
docker-compose up -d

# Or run locally
pip install -r requirements.txt
python main.py
```

## Environment Variables

### Frontend (SduChatBotFront)
```env
VITE_API_URL=https://chat-back.sdu.edu.kz/api
```

### Backend (SduChatBotBack)
```env
SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/sduchat
SPRING_DATASOURCE_USERNAME=k_app
SPRING_DATASOURCE_PASSWORD=123
GOOGLE_CLIENT_ID=your_google_oauth_client_id
GOOGLE_CLIENT_SECRET=your_google_oauth_secret
GOOGLE_REDIRECT_URI=your_frontend_redirect_uri
SDU_AI_API_KEY=your_lambda_api_key
SDU_AI_API_URL=your_lambda_function_url
JWT_SECRET_KEY=auto_generated_secret
```

### AWS Lambda Service
```env
KNOWLEDGE_BASE_ID=your_knowledge_base_id
MODEL_ID=eu.anthropic.claude-3-7-sonnet-20250219-v1:0
REGION_NAME=eu-central-1
PROMPT_ID=your_main_prompt_id
PROMPT_VERSION=your_prompt_version
CONDENSE_PROMPT_ID=your_condense_prompt_id
CONDENSE_PROMPT_VERSION=your_condense_version
TOPIC_PROMPT_ID=your_topic_prompt_id
TOPIC_PROMPT_VERSION=your_topic_version
CHAT_HISTORY_TABLE=sdu-bot-chat-history
RERANKER_MODEL_ID=cohere.rerank-v3-5:0
```

### On-Premise Services
```env
# LocalChatBotService
OPENAI_API_KEY=your_openai_api_key
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=ft:gpt-4o-mini-2024-07-18:personal:sdubot:AJHQiny8
DATABASE_URL=postgresql://username:password@localhost:5432/sdubot

# TelegramBotUI
BOT_TOKEN=your_telegram_bot_token
POSTGRES_URL=postgresql://user:root@telegram_bot-postgres:5432/postgres

# QdrantRagService
QDRANT_HOST=localhost
QDRANT_PORT=6333
COLLECTION_NAME=documents
```

## Testing Instructions

### Frontend Testing
```bash
cd frontend/SduChatBotFront

# Manual testing checklist:
# 1. Navigate to /login and complete authentication
# 2. Send messages and verify responses
# 3. Create new chat sessions
# 4. Test responsive design on different screen sizes
# 5. Verify error handling with network disconnection

npm run lint  # Code quality check
```

### Backend Testing
```bash
cd backend/SduChatBotBack

# Run unit tests
./gradlew test

# Access Swagger UI for API testing
# http://localhost:8080/api/swagger-ui.html
```

### AWS Lambda Testing
```bash
cd aws/ChatBotService

# Test with sample request
curl -X POST https://your-api-gateway-url/ \
  -H "Content-Type: application/json" \
  -d @request.json
```

### RAG Service Testing
```bash
cd on-premise/QdrantRagService

# Run automated tests
python src/test_client.py --service-url http://localhost:8000

# Interactive search mode
python src/test_client.py --interactive
```

### Telegram Bot Testing
```bash
# 1. Start the bot
# 2. Message your bot on Telegram
# 3. Send /start command
# 4. Test language selection
# 5. Navigate through menus
# 6. Test AI question answering
```

## Project Structure

```
sdu-chatbot-platform/
├── README.md                           # This file - main project documentation
├── .gitignore                          # Git ignore rules
│
├── frontend/                           # Frontend applications
│   ├── SduChatBotFront/               # Main web application
│   │   ├── src/
│   │   │   ├── components/            # React components
│   │   │   │   ├── chat/             # Chat interface components
│   │   │   │   └── chat-side-bar/    # Sidebar components
│   │   │   ├── pages/                # Page components
│   │   │   ├── route/                # Routing configuration
│   │   │   ├── services/             # API services (RTK Query)
│   │   │   ├── store/                # Redux store
│   │   │   └── main.tsx              # Application entry point
│   │   ├── public/                   # Static assets
│   │   ├── Dockerfile                # Docker configuration
│   │   ├── docker-compose.yml        # Docker Compose setup
│   │   ├── nginx.conf                # Nginx configuration
│   │   ├── package.json              # Dependencies
│   │   ├── vite.config.ts            # Vite configuration
│   │   └── README.md                 # Frontend documentation
│   │
│   └── SDUBot-ChatVersioning-Beta/   # Chat versioning prototype
│       ├── src/
│       │   ├── components/           # React components
│       │   │   └── Chat.js          # Tree-based chat component
│       │   ├── App.js               # Main application
│       │   └── index.js             # Entry point
│       ├── package.json             # Dependencies
│       └── README.md                # Versioning documentation
│
├── backend/                          # Backend services
│   └── SduChatBotBack/              # Spring Boot REST API
│       ├── src/main/java/kz/sdu/chat/mainservice/
│       │   ├── config/              # Spring configurations
│       │   ├── entities/            # JPA entities
│       │   ├── repositories/        # Data repositories
│       │   ├── services/            # Business logic
│       │   ├── rest/
│       │   │   ├── controllers/     # REST controllers
│       │   │   └── dto/            # Data transfer objects
│       │   ├── security/           # JWT security
│       │   ├── feign/              # External API clients
│       │   └── exceptions/         # Exception handling
│       ├── Dockerfile              # Docker configuration
│       ├── docker-compose.yml      # Docker Compose setup
│       ├── build.gradle.kts        # Gradle build configuration
│       └── README.md               # Backend documentation
│
├── aws/                             # AWS cloud services
│   └── ChatBotService/             # Lambda-based chatbot
│       ├── lambda_function.py      # Main Lambda handler
│       ├── docs/                   # Knowledge base documents
│       ├── api_docs.json           # API documentation
│       ├── main_prompt_system.txt  # System prompts
│       ├── condense_prompt_*.txt   # Condensation prompts
│       ├── topic_prompt_*.txt      # Topic generation prompts
│       ├── .env.example            # Environment template
│       ├── request.json            # Sample request
│       └── README.md               # AWS service documentation
│
└── on-premise/                      # On-premise deployment options
    ├── LocalChatBotService/        # Local AI chatbot
    │   ├── model/                  # AI model service
    │   │   ├── model_rag.py       # RAG implementation
    │   │   ├── database_create.py # Vector DB setup
    │   │   └── requirements.txt   # Python dependencies
    │   ├── tgbot/                 # Telegram bot
    │   │   ├── telegram_bot/      # Bot implementation
    │   │   ├── sql/               # Database schema
    │   │   └── requirements.txt   # Python dependencies
    │   └── README.md              # Local service documentation
    │
    ├── QdrantRagService/          # RAG service with Qdrant
    │   ├── main.py                # FastAPI application
    │   ├── src/
    │   │   ├── data_loader.py    # Data loading utilities
    │   │   └── test_client.py    # Testing client
    │   ├── docker-compose.yaml   # Docker Compose setup
    │   ├── Dockerfile            # Docker configuration
    │   ├── Makefile              # Development commands
    │   ├── requirements.txt      # Python dependencies
    │   └── README.md             # RAG service documentation
    │
    └── TelegramBotUI/             # Telegram bot interface
        ├── main.py                # Bot entry point
        ├── handlers.py            # Message handlers
        ├── routers.py             # Route definitions
        ├── db.py                  # Database operations
        ├── tree_structure.py      # Menu system
        ├── config.py              # Configuration
        ├── DataStore/             # Local database
        ├── db_queries/            # SQL scripts
        ├── input_files/           # Menu configurations
        ├── images/                # Static assets
        ├── docker-compose.yml     # Docker Compose setup
        ├── requirements.txt       # Python dependencies
        └── README.md              # Telegram bot documentation
```

### Folder Descriptions

- **`frontend/`** - Web-based user interfaces built with React
  - `SduChatBotFront/` - Production web application with authentication and chat features
  - `SDUBot-ChatVersioning-Beta/` - Experimental tree-based conversation versioning interface

- **`backend/`** - Server-side REST API services
  - `SduChatBotBack/` - Spring Boot application handling authentication, chat management, and API integration

- **`aws/`** - Cloud-based AI services
  - `ChatBotService/` - AWS Lambda function with Bedrock integration for AI responses

- **`on-premise/`** - Self-hosted deployment options
  - `LocalChatBotService/` - Complete local AI chatbot with Telegram interface
  - `QdrantRagService/` - Vector database RAG service for semantic search
  - `TelegramBotUI/` - Standalone Telegram bot with multilingual support

## Links to Documentation

### Component Documentation
- [Frontend Web App](frontend/SduChatBotFront/README.md) - React web application
- [Chat Versioning](frontend/SDUBot-ChatVersioning-Beta/README.md) - Tree-based chat interface
- [Backend API](backend/SduChatBotBack/README.md) - Spring Boot REST API
- [AWS Lambda Service](aws/ChatBotService/README.md) - Cloud AI chatbot
- [Local AI Service](on-premise/LocalChatBotService/README.md) - On-premise chatbot
- [RAG Service](on-premise/QdrantRagService/README.md) - Vector search service
- [Telegram Bot](on-premise/TelegramBotUI/README.md) - Telegram interface

### External Resources
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Amazon Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [React Documentation](https://react.dev/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [aiogram Documentation](https://docs.aiogram.dev/)
- [SDU Official Website](https://sdu.edu.kz)

## Features

### Core Capabilities
- ✅ Multilingual support (English, Kazakh, Russian, Turkish, German)
- ✅ Multiple deployment options (cloud, on-premise, Telegram)
- ✅ Secure authentication with JWT and OAuth
- ✅ Conversation history and context management
- ✅ Real-time chat interface
- ✅ Document retrieval with semantic search
- ✅ AI-powered responses with source attribution
- ✅ Cost tracking and usage monitoring
- ✅ Administrative tools and statistics
- ✅ Responsive design for all devices

### Advanced Features
- ✅ Tree-based conversation versioning
- ✅ Branch navigation and exploration
- ✅ Document reranking for accuracy
- ✅ Automatic topic generation
- ✅ Multi-session support
- ✅ Connection status monitoring
- ✅ Interactive menu systems
- ✅ Payment integration
- ✅ Form and service links

## Deployment Options

### Cloud Deployment (AWS)
- AWS Lambda for serverless compute
- Amazon Bedrock for AI models
- DynamoDB for chat history
- S3 for knowledge base
- API Gateway for HTTP endpoints

### On-Premise Deployment
- Docker Compose for orchestration
- PostgreSQL for data storage
- Local LLM models (GPT-4, Claude)
- Qdrant for vector search
- Nginx for web serving

### Hybrid Deployment
- Frontend on cloud (Vercel, Netlify)
- Backend on-premise or cloud
- AI services on AWS Bedrock
- Database on-premise

## Support and Contributing

For technical issues, questions, or contributions:
1. Check component-specific README files
2. Review API documentation (Swagger UI)
3. Contact the development team
4. Create issues in the repository

## License

This project is proprietary to Suleyman Demirel University (SDU).
