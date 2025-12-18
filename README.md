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
```bash
cd on-premise/QdrantRagService
docker-compose up -d
```
Access at: http://localhost:8000

#### 4. Telegram Bot UI
```bash
cd TelegramBotUI
pip install -r requirements.txt
# Run the bot (specific commands in the service directory)
```

#### 5. Chat Versioning App
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

## Instructions for Tests

No automated tests are currently implemented in the project. Manual testing can be performed by interacting with the deployed services or running the applications locally and verifying responses.

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

---

**Note:** Some information such as detailed system requirements, complete environment variable lists, and test instructions are not fully available in the current files. Please provide additional details for these sections if needed.