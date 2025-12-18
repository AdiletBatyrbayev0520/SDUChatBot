# SDU Student Support Telegram Bot

## Product Overview

The SDU Student Support Telegram Bot is a multilingual assistant designed to help Sdu Demirel University students access essential services and information. The bot provides an intuitive interface for student services, IT support, and integrates with an AI-powered question-answering system to provide personalized assistance.

## Problem & Solution

**Problem:** SDU students often struggle to find information about university services, navigate bureaucratic processes, and get timely support for common issues like ID card applications, document requests, and IT problems.

**Solution:** This Telegram bot centralizes all student services in one accessible platform, offering:
- Multilingual support (English, Russian, Kazakh, Turkish, German)
- Interactive menu system for easy navigation
- Direct links to forms and payment systems
- AI-powered chat assistance for complex queries
- Administrative tools for user statistics

## Target Users

- **Primary:** SDU students needing assistance with university services
- **Secondary:** University administrators managing student support
- **Tertiary:** Graduates requiring archival documents and diploma restoration

## Tech Stack

### Backend
- **Python 3.12** - Core programming language
- **aiogram 3.20** - Telegram Bot API framework
- **SQLite** - Local database for user management
- **aiohttp** - HTTP client for AI service integration

### Infrastructure
- **Docker & Docker Compose** - Containerization and orchestration
- **PostgreSQL 15** - Production database (Docker)
- **External AI Service** - LLM-based question answering

### Dependencies
- `python-decouple` - Environment variable management
- `loguru` - Advanced logging
- `aiofiles` - Asynchronous file operations

## Local Development Setup

### System Requirements
- Python 3.12+
- Docker & Docker Compose
- Git

### Installation Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd sdu-telegram-bot
```

2. **Set up environment variables**
```bash
cp .env_example .env
```
Edit `.env` file with your values:
```
BOT_TOKEN=your_telegram_bot_token_here
POSTGRES_URL=postgresql://user:root@telegram_bot-postgres:5432/postgres
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Start with Docker (Recommended)**
```bash
docker-compose up -d
```

5. **Or run locally**
```bash
python main.py
```

### Getting a Bot Token
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the provided token to your `.env` file

## Testing Instructions

### Manual Testing
1. Start the bot locally or with Docker
2. Open Telegram and find your bot
3. Send `/start` to begin interaction
4. Test language selection and menu navigation
5. Verify admin commands with `/stat` (requires admin privileges)

### Database Testing
```bash
# Access SQLite database
sqlite3 DataStore/database.db
.tables
SELECT * FROM users;
SELECT * FROM admins;
```

### Docker Testing
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs bot-backend

# Access database container
docker-compose exec bot-postgres psql -U user -d postgres
```

## Project Structure

```
├── main.py                 # Application entry point and bot initialization
├── routers.py             # Route definitions for message and callback handlers
├── handlers.py            # Business logic for bot commands and interactions
├── db.py                  # Database operations and user management
├── tree_structure.py      # Menu tree structure and keyboard generation
├── config.py              # Configuration and file paths
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Multi-container orchestration
├── .env_example          # Environment variables template
│
├── DataStore/            # Local database storage
│   └── database.db       # SQLite database file
│
├── db_queries/           # SQL scripts
│   ├── create_tables.sql # Database schema
│   ├── create_triggers.sql
│   └── drop_tables.sql
│
├── input_files/          # Bot configuration files
│   ├── authorization/    # Language selection menu
│   ├── main_menu/       # Multilingual main menus
│   └── back_button.json # Navigation button texts
│
└── images/              # Static assets
    ├── sdupayment.jpg   # Payment QR codes
    └── sdupayment2.jpg
```

### Key Components

- **`main.py`** - Bot initialization, environment setup, and polling
- **`handlers.py`** - Core bot functionality including AI integration
- **`tree_structure.py`** - Dynamic menu system with multilingual support
- **`db.py`** - User management, language preferences, and admin controls
- **`input_files/`** - JSON-based menu configurations for easy content updates
- **Docker setup** - Production-ready containerization with PostgreSQL

## Additional Documentation

- [Environment Configuration](.env_example) - Required environment variables
- [Database Schema](db_queries/create_tables.sql) - Complete database structure
- [Menu Configuration](input_files/) - JSON-based menu system documentation
- [Docker Configuration](docker-compose.yml) - Container orchestration setup

## Features

### Core Functionality
- ✅ Multilingual interface (5 languages)
- ✅ Interactive menu navigation
- ✅ Student service information and forms
- ✅ IT support resources
- ✅ Payment QR code integration
- ✅ AI-powered question answering
- ✅ Admin statistics and user management

### Technical Features
- ✅ Dockerized deployment
- ✅ Database persistence
- ✅ Error handling and logging
- ✅ Modular architecture
- ✅ Environment-based configuration