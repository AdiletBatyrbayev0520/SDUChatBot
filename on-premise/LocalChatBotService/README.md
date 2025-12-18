# SduBot - SDU University Assistant

A comprehensive AI-powered chatbot system designed to assist SDU University students with academic inquiries, university services, and general guidance through both Telegram bot interface and command-line interaction.

## Product Overview

SduBot is an intelligent assistant that leverages RAG (Retrieval-Augmented Generation) technology to provide accurate, contextual responses about SDU University. The system combines a fine-tuned GPT model with a comprehensive knowledge base to deliver personalized support to students, faculty, and staff.

## Problem & Solution

**Problem**: Students often struggle to find accurate, timely information about university services, academic procedures, room bookings, library resources, and general campus life, leading to confusion and inefficient information seeking.

**Solution**: SduBot provides an intelligent, 24/7 accessible assistant that can answer questions about university services, help with room and book management, and provide guidance on academic matters using natural language processing and a comprehensive university database.

## Target Users

- **Students**: Get instant answers about courses, schedules, room bookings, library services, and campus facilities
- **Faculty**: Access information about rooms, resources, and student management
- **Staff**: Utilize the system for administrative queries and resource management
- **Prospective Students**: Learn about programs, facilities, and university services

## Tech Stack

### Backend & AI
- **Python 3.12**: Core programming language
- **LangChain**: RAG implementation and chain management
- **OpenAI GPT-4**: Fine-tuned model for university-specific responses
- **ChromaDB**: Vector database for document embeddings
- **FastAPI**: API framework for model service

### Telegram Bot
- **aiogram 3.15**: Telegram Bot API framework
- **AsyncPG**: PostgreSQL async database driver
- **APScheduler**: Task scheduling for automated operations

### Database & Storage
- **PostgreSQL**: Primary database for structured data
- **ChromaDB**: Vector storage for document embeddings
- **Docker**: Containerization and deployment

### Additional Tools
- **PyPDF2**: PDF document processing
- **python-dotenv**: Environment variable management
- **SQLAlchemy**: Database ORM

## System Requirements

- **Python**: 3.12 or higher
- **Docker**: Latest version
- **PostgreSQL**: 13+ (if running locally)
- **Memory**: Minimum 4GB RAM
- **Storage**: 2GB free space for models and database

## Environment Variables

Create a `.env` file in both `model/` and `tgbot/` directories:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=ft:gpt-4o-mini-2024-07-18:personal:sdubot:AJHQiny8

# Database Configuration (for tgbot)
DATABASE_URL=postgresql://username:password@localhost:5432/sdubot
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sdubot
DB_USER=username
DB_PASSWORD=password

# Telegram Bot Configuration (for tgbot)
BOT_TOKEN=your_telegram_bot_token_here

# System Prompts
SYSTEM_PROMPT="You are a helpful bot assistant that helps students find answers to questions related to SDU university..."
CONTEXT_Q__SYSTEM_PROMPT="Given a chat history and the latest user question..."
```

## Running the Project Locally

### Option 1: Using Docker (Recommended)

#### Telegram Bot
```bash
# Clone the repository
git clone https://github.com/baauka/SduBot.git
cd SduBot

# Build and run the Telegram bot
cd tgbot
docker build -t sdubot-telegram .
docker run --env-file .env sdubot-telegram
```

#### AI Model Service
```bash
# Build and run the model service
cd model
docker build -t sdubot-model .
docker run --env-file .env -it sdubot-model
```

### Option 2: Local Development Setup

#### Prerequisites Setup
```bash
# Install Python dependencies for model
cd model
pip install -r requirements.txt

# Install Python dependencies for telegram bot
cd ../tgbot
pip install -r requirements.txt
```

#### Database Setup
```bash
# Start PostgreSQL (using Docker)
docker run --name sdubot-postgres -e POSTGRES_DB=sdubot -e POSTGRES_USER=username -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:13

# Create database tables
cd tgbot/sql
psql -h localhost -U username -d sdubot -f create_tables.sql
psql -h localhost -U username -d sdubot -f create_index.sql
psql -h localhost -U username -d sdubot -f triggers.sql

# Load sample data (optional)
# Import CSV files from tgbot/sql/data/ directory
```

#### Running Services
```bash
# Terminal 1: Run the AI model service
cd model
python model_rag.py

# Terminal 2: Run the Telegram bot
cd tgbot/telegram_bot
python aiogram_run.py
```

### Option 3: Using Pre-built Images
```bash
# Pull and run Telegram bot
docker pull sultanmukashev/tg-bot:latest
docker run --env-file .env sultanmukashev/tg-bot:latest

# Pull and run model service
docker pull sultanmukashev/sdu-bot:latest
docker run --env-file .env -it sultanmukashev/sdu-bot:latest
```

## Testing Instructions

### Manual Testing
1. **Telegram Bot**: Message [@SDUGuideBot](https://t.me/SDUGuideBot) on Telegram
2. **Model Service**: Run `python model_rag.py` and interact via command line
3. **Database**: Verify data integrity using SQL queries in `tgbot/sql/queries/`

### Test Scenarios
- Ask about course information
- Request room booking assistance
- Inquire about library services
- Test multilingual support
- Verify database operations

## Project Structure

```
SduBot/
├── README.md                          # Main project documentation
├── .gitignore                         # Git ignore rules
├── .dockerignore                      # Docker ignore rules
│
├── model/                             # AI Model Service
│   ├── README.md                      # Model-specific documentation
│   ├── requirements.txt               # Python dependencies
│   ├── dockerfile                     # Docker configuration
│   ├── chat_model.py                  # Simple chat interface
│   ├── model_rag.py                   # RAG implementation
│   ├── database_create.py             # Vector database setup
│   └── .gitignore                     # Model-specific ignores
│
└── tgbot/                             # Telegram Bot Service
    ├── requirements.txt               # Bot dependencies
    ├── Dockerfile                     # Docker configuration
    ├── .dockerignore                  # Docker ignore rules
    ├── .gitignore                     # Bot-specific ignores
    │
    ├── sql/                           # Database Schema & Data
    │   ├── create_tables.sql          # Database schema
    │   ├── create_index.sql           # Database indexes
    │   ├── drop_tables.sql            # Cleanup scripts
    │   ├── drop_index.sql             # Index cleanup
    │   ├── triggers.sql               # Database triggers
    │   ├── data/                      # Sample data (CSV files)
    │   │   ├── Access_Control.csv     # Access permissions
    │   │   ├── Books.csv              # Library books
    │   │   ├── Courses.csv            # Course information
    │   │   ├── Faculties.csv          # Faculty data
    │   │   ├── Groups.csv             # Student groups
    │   │   ├── Persons.csv            # User profiles
    │   │   ├── Rooms.csv              # Room information
    │   │   ├── Students.csv           # Student records
    │   │   └── Teachers.csv           # Faculty records
    │   └── queries/                   # SQL query examples
    │
    └── telegram_bot/                  # Bot Implementation
        ├── requirements.txt           # Bot-specific dependencies
        ├── aiogram_run.py             # Main bot runner
        ├── create_bot.py              # Bot initialization
        ├── run.py                     # Alternative runner
        ├── handlers/                  # Message handlers
        ├── keyboards/                 # Bot keyboards/menus
        ├── middlewares/               # Bot middlewares
        ├── filters/                   # Custom filters
        ├── utils/                     # Utility functions
        ├── db_handler/                # Database operations
        ├── db_pdf/                    # PDF document storage
        └── work_time/                 # Scheduling utilities
```

## Additional Documentation

- [Model Documentation](model/README.md) - Detailed AI model setup and usage
- [Database Schema](tgbot/sql/create_tables.sql) - Complete database structure
- [SQL Queries](tgbot/sql/queries/) - Example database operations
- [Bot Handlers](tgbot/telegram_bot/handlers/) - Telegram bot command implementations

## Live Demo

Interact with the bot on Telegram: [@SDUGuideBot](https://t.me/SDUGuideBot)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For technical issues or questions, please open an issue in the repository or contact the development team.
