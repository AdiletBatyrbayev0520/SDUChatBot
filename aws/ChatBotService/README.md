# SDU University AI Chatbot

## Product Overview

The SDU University AI Chatbot is an intelligent conversational assistant designed specifically for Suleyman Demirel University (SDU) students, staff, and prospective applicants. This AWS Lambda-based chatbot leverages Amazon Bedrock's advanced AI capabilities to provide accurate, contextual responses about university policies, procedures, academic programs, and general information.

The system uses a Retrieval-Augmented Generation (RAG) architecture, combining a comprehensive knowledge base with conversational AI to deliver personalized, multilingual support in English, Kazakh, and Russian.

## Problem and Solution

### The Problem
University students and staff often struggle to find accurate, up-to-date information about:
- Academic policies and procedures
- Admission requirements and processes
- Campus services and facilities
- Student life and activities
- Administrative procedures
- University resources and contacts

Traditional static websites and documentation can be overwhelming, outdated, or difficult to navigate, leading to frustration and inefficient information retrieval.

### The Solution
Our AI chatbot provides:
- **Instant Access**: 24/7 availability for immediate responses to university-related queries
- **Contextual Understanding**: Maintains conversation history for more natural, context-aware interactions
- **Multilingual Support**: Responds in the user's preferred language (English, Kazakh, Russian)
- **Accurate Information**: Draws from a curated knowledge base of official SDU documents and policies
- **Personalized Experience**: Tracks user conversations and generates relevant topics for better engagement

## Target Users

- **Current Students**: Seeking information about courses, policies, services, and campus life
- **Prospective Students**: Inquiring about admission requirements, programs, and university facilities
- **Faculty and Staff**: Accessing administrative procedures, policies, and university resources
- **Parents and Guardians**: Getting information about university services and student support
- **International Students**: Requiring assistance with university processes and integration

## Tech Stack

### Backend Infrastructure
- **AWS Lambda**: Serverless compute for handling API requests
- **Amazon Bedrock**: AI/ML service for language model inference
- **Amazon DynamoDB**: NoSQL database for chat history storage
- **Amazon S3**: Document storage for the knowledge base

### AI/ML Components
- **Claude 3.7 Sonnet**: Primary language model for response generation
- **Cohere Rerank v3.5**: Document reranking for improved retrieval accuracy
- **Amazon Bedrock Knowledge Base**: Vector database for document retrieval
- **Custom Prompt Engineering**: Specialized prompts for conversation management

### Development Tools
- **Python 3.x**: Primary programming language
- **Boto3**: AWS SDK for Python
- **JSON**: Data interchange format

## System Requirements

### AWS Services Required
- AWS Lambda (with appropriate execution role)
- Amazon Bedrock (with model access permissions)
- Amazon DynamoDB (for chat history)
- Amazon S3 (for knowledge base documents)
- Amazon Bedrock Knowledge Base service

### Local Development
- Python 3.8 or higher
- AWS CLI configured with appropriate credentials
- Access to AWS Bedrock models in your region

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Core Configuration
KNOWLEDGE_BASE_ID=your_knowledge_base_id
MODEL_ID=eu.anthropic.claude-3-7-sonnet-20250219-v1:0
REGION_NAME=eu-central-1

# Prompt Configuration
PROMPT_ID=your_main_prompt_id
PROMPT_VERSION=your_prompt_version
CONDENSE_PROMPT_ID=your_condense_prompt_id
CONDENSE_PROMPT_VERSION=your_condense_version
TOPIC_PROMPT_ID=your_topic_prompt_id
TOPIC_PROMPT_VERSION=your_topic_version

# Database and Reranking
CHAT_HISTORY_TABLE=sdu-bot-chat-history
RERANKER_MODEL_ID=cohere.rerank-v3-5:0
```

## Running the Project Locally

### 1. Clone and Setup
```bash
git clone <repository-url>
cd sdu-chatbot
```

### 2. Install Dependencies
```bash
pip install boto3 python-dotenv
```

### 3. Configure AWS Credentials
```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and Region
```

### 4. Set Environment Variables
```bash
cp .env.example .env
# Edit .env with your actual AWS resource IDs
```

### 5. Test Locally
```bash
python lambda_function.py
```

### 6. Deploy to AWS Lambda
```bash
# Create deployment package
zip -r deployment.zip lambda_function.py

# Upload to Lambda using AWS CLI or Console
aws lambda update-function-code --function-name sdu-chatbot --zip-file fileb://deployment.zip
```

## API Usage

### POST Request
```bash
curl -X POST https://your-api-gateway-url/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the admission requirements for SDU?",
    "chat_id": "user123",
    "is_need_topic": true
  }'
```

### Response Format
```json
{
  "question": "What are the admission requirements for SDU?",
  "answer": "SDU admission requirements include...",
  "sources": ["admission_policy.pdf", "student_guide.pdf"],
  "topic": "SDU Admission Requirements",
  "usage_metadata": {
    "input_tokens": 1250,
    "output_tokens": 380,
    "total_tokens": 1630,
    "costUsd": 0.0087
  }
}
```

## Testing

### Manual Testing
1. Use the provided `request.json` for sample requests
2. Test different languages by asking questions in English, Kazakh, or Russian
3. Verify conversation continuity by sending multiple messages with the same `chat_id`

### API Documentation
Access the built-in API documentation:
```bash
curl -X GET https://your-api-gateway-url/
```

## Project Structure

```
sdu-chatbot/
├── lambda_function.py              # Main Lambda handler and chatbot logic
├── api_docs.json                   # API documentation and examples
├── .env.example                    # Environment variables template
├── request.json                    # Sample API request for testing
├── response.json                   # Sample API response for reference
├── main_prompt_system.txt          # System prompt for main responses
├── condense_prompt_system.txt      # Prompt for question condensation
├── condense_prompt_user.txt        # User template for condensation
├── topic_prompt_system.txt         # Prompt for topic generation
├── topic_prompt_user.txt           # User template for topics
├── docs/                           # Knowledge base documents
│   ├── Academic_calendar_2025-2026_*.md    # Academic calendars (multilingual)
│   ├── SDU_intro_*.md              # University introduction (multilingual)
│   ├── SDU_specialities_*.md       # Academic programs information
│   ├── SDU_structure_*.md          # University structure and organization
│   ├── assessment_policy_*.md      # Academic assessment policies
│   ├── academic_leave_*.md         # Academic leave procedures
│   └── [other policy documents]    # Various university policies and guides
└── README.md                       # This file
```

### Key Components

- **`lambda_function.py`**: Core application logic including conversation management, document retrieval, and AI response generation
- **`docs/`**: Multilingual knowledge base containing official SDU documents, policies, and procedures
- **Prompt files**: Specialized prompts for different AI tasks (main responses, question condensation, topic generation)
- **Configuration files**: API documentation and environment setup templates

## Related Documentation

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Amazon Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [SDU Official Website](https://sdu.edu.kz)
- [API Documentation](api_docs.json) - Built-in API reference
- [Environment Setup](.env.example) - Configuration template

## Features

- **Conversational Memory**: Maintains chat history for contextual responses
- **Multilingual Support**: Automatic language detection and response in user's language
- **Document Retrieval**: Intelligent search through university knowledge base
- **Cost Tracking**: Built-in token usage and cost monitoring
- **Topic Generation**: Automatic conversation topic extraction
- **Source Attribution**: Provides references to source documents
- **Reranking**: Advanced document relevance scoring for better accuracy

## Support

For technical issues or questions about the chatbot system, please refer to the SDU Helpdesk or contact the development team through the university's official channels.