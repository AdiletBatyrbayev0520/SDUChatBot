# SDUChatBot

## Short Product Overview

SDU ChatBot is an AI-powered assistant designed to provide quick and accurate information about Suleyman Demirel University (SDU). It serves as a knowledge base interface for students and staff, answering questions related to university policies, procedures, admissions, and other relevant topics.

## Main Problem and Proposed Solution

**Problem:** Students and staff at SDU often need immediate access to detailed information about university policies, procedures, academic calendars, admission requirements, and various administrative processes. Traditional methods of finding this information through websites or documents can be time-consuming and inefficient.

**Solution:** SDU ChatBot uses Retrieval-Augmented Generation (RAG) technology to provide conversational AI responses based on a comprehensive knowledge base. It offers multiple deployment options including cloud-based AWS services and on-premise solutions, ensuring accessibility and reliability.

## Target Users

- SDU students (undergraduate and graduate)
- SDU faculty and staff
- Prospective students seeking admission information
- International students and partners

## Tech Stack

- **Backend:** Python, FastAPI
- **AI/ML:** AWS Bedrock (Anthropic Claude), Qdrant vector database
- **Cloud Services:** AWS Lambda, AWS Bedrock, DynamoDB
- **Frontend:** React.js, Tailwind CSS
- **Messaging:** Telegram Bot API
- **Containerization:** Docker, Docker Compose
- **Other:** boto3, OpenAI API (for on-premise)

## Steps to Run the Project Locally

### System Requirements

- Python 3.11+
- Node.js 16+
- Docker and Docker Compose
- AWS CLI (for AWS deployment)
- Git

### Environment Variables

Create a `.env` file in the respective directories with the following variables:

For AWS ChatBotService (aws/ChatBotService/.env):
```
CHAT_HISTORY_TABLE=sdu-bot-chat-history
CONDENSE_PROMPT_ID=VL6CWMAAYR
CONDENSE_PROMPT_VERSION=9
KNOWLEDGE_BASE_ID=VCPJQ61K6D
MODEL_ID=eu.anthropic.claude-3-7-sonnet-20250219-v1:0
PROMPT_ID=2FLJ9VJKY9
PROMPT_VERSION=13
TOPIC_PROMPT_ID=MO77YNVRDJ
TOPIC_PROMPT_VERSION=6
REGION_NAME=eu-central-1
RERANKER_MODEL_ID=cohere.rerank-v3-5:0
```

For on-premise services, additional variables may be required (please check individual service READMEs).

### Running the Project

#### 1. Clone the Repository
```bash
git clone https://github.com/AdiletBatyrbayev0520/ChatBotAdmission.git
cd SDUChatBot
```

#### 2. AWS ChatBot Service
This is a serverless AWS Lambda function. For local development:
- Use AWS SAM or LocalStack for simulation
- Deploy to AWS for production

#### 3. On-Premise Qdrant RAG Service

This is a full-featured Retrieval-Augmented Generation (RAG) system using Qdrant as the vector database and FastAPI for the API.

**Prerequisites:**
- Docker and Docker Compose
- Python 3.11+ (for local development)

**Setup:**
```bash
cd on-premise/QdrantRagService
mkdir -p data qdrant_storage
docker-compose up -d
```

**Access:**
- RAG API: http://localhost:8000
- Qdrant Web UI: http://localhost:6333/dashboard
- API Documentation: http://localhost:8000/docs

**Health Check:**
```bash
curl http://localhost:8000/health
```

#### 4. Telegram Bot UI

**Build from source:**
```bash
cd on-premise/LocalChatBotService/tgbot
docker build -t sdu-bot .
```

**Or use pre-built image:**
```bash
docker pull sultanmukashev/tg-bot:latest
```

**Run the container:**
```bash
docker run sultanmukashev/tg-bot:latest
```

**Interact with the bot:**
Work with the bot in [Telegram](https://t.me/SDUGuideBot).

#### 5. Chat Versioning App

A React application with Tailwind CSS implementing tree-based chat versioning. Each user message can have multiple alternative versions (branches), creating a branched dialogue structure.

**Features:**
- Tree-structured dialogue
- Message editing with automatic bot response updates
- Version navigation
- Synchronous navigation across all messages

**Setup:**
```bash
cd SDUBot-ChatVersioning
npm install
npm start
```

Access at: http://localhost:3000

#### 6. Local ChatBot Service
```bash
cd on-premise/LocalChatBotService
docker build -t sdu-bot .
docker run sdu-bot
```

## API Usage

The AWS ChatBot Service provides a REST API for interacting with the chatbot.

### Endpoints

- **POST /**: Ask a question to the SDU knowledge base
  - Parameters: `question` (required), `user_id` (required), `language` (optional, default: en)
- **GET /**: Ask a question via query parameters
  - Parameters: `question` (required), `user_id` (optional, default: test_user), `language` (optional, default: en)

### Example Requests

**POST:**
```json
{
  "question": "What are the admission requirements for SDU?",
  "chat_id": "student123",
  "isNeedTopic": true
}
```

**GET:**
```
GET /?question=What are SDU office hours?&user_id=test_user&language=en
```

### CORS

Enabled with allowed origins set to origin, methods: GET, POST, OPTIONS.

## Project Structure

```
SDUChatBot/
├── aws/
│   └── ChatBotService/          # AWS Lambda-based chatbot service
│       ├── lambda_function.py   # Main Lambda handler
│       ├── api_docs.json        # API documentation
│       ├── docs/                # Knowledge base documents
│       └── *.txt                # Prompt templates
├── on-premise/
│   ├── LocalChatBotService/     # Local chatbot implementation
│   │   └── model/               # ML model components
│   ├── QdrantRagService/        # RAG system with Qdrant vector DB
│   │   ├── docker-compose.yaml
│   │   ├── main.py
│   │   └── src/                 # Source code
│   └── TelegramBotUI/           # Telegram bot interface
│       ├── Dockerfile
│       └── requirements.txt
├── SDUBot-ChatVersioning/       # React app for chat versioning
│   ├── src/
│   │   ├── components/
│   │   └── App.js
│   └── package.json
└── README.md                    # This file
```

## Links to Other Documents

- [AWS ChatBot Service README](aws/ChatBotService/README.md)
- [Local ChatBot Service README](on-premise/LocalChatBotService/README.md)
- [Qdrant RAG Service README](on-premise/QdrantRagService/README.md)
- [Chat Versioning App README](SDUBot-ChatVersioning/README.md)

## Knowledge Base

The chatbot's knowledge base includes comprehensive information about SDU:
- University policies and procedures
- Student guides
- Academic calendars
- Admission requirements
- Faculty information
- Social media and contact details
- LMS and learning resources

Documents are available in multiple languages (English, Kazakh, Russian) and cover various aspects of university life.