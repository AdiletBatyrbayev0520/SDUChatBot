# RAG Service MVP

A production-ready Retrieval-Augmented Generation (RAG) service built with FastAPI and Qdrant vector database, designed for semantic document search and retrieval.

## Product Overview

This RAG Service MVP provides a complete solution for document indexing, semantic search, and retrieval. It combines the power of modern embedding models with Qdrant's high-performance vector database to enable intelligent document search capabilities. The service offers both REST API endpoints and command-line tools for easy integration and testing.

## Problem & Solution

**Problem**: Traditional keyword-based search systems fail to understand semantic meaning and context, making it difficult to find relevant information when queries don't match exact terms in documents.

**Solution**: Our RAG service uses advanced sentence transformers to convert documents and queries into high-dimensional vectors, enabling semantic similarity search. This allows users to find relevant documents even when using different terminology or phrasing.

## Target Users

- **Developers** building AI-powered applications requiring semantic search
- **Data Scientists** working with large document collections
- **Product Teams** implementing intelligent search features
- **Researchers** needing efficient document retrieval systems
- **Enterprises** looking to enhance their knowledge management systems

## Tech Stack

- **Backend Framework**: FastAPI (Python 3.13)
- **Vector Database**: Qdrant
- **Embedding Model**: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- **Containerization**: Docker & Docker Compose
- **HTTP Client**: Uvicorn ASGI server
- **Data Processing**: NumPy, Pydantic
- **Development Tools**: Make, Python scripts

## Running the Project Locally

### System Requirements

- Docker and Docker Compose
- Python 3.13+ (for local development)
- 4GB+ RAM (recommended for embedding model)
- 2GB+ free disk space

### Environment Variables

The service uses the following environment variables:

```bash
QDRANT_HOST=localhost          # Qdrant server host
QDRANT_PORT=6333              # Qdrant server port
COLLECTION_NAME=documents     # Vector collection name
```

### Quick Start Commands

1. **Clone and setup**:
```bash
git clone <repository-url>
cd qdrantragservice
```

2. **Start the complete system**:
```bash
# Build and start all services
make setup

# Or manually:
docker-compose up -d
```

3. **Verify installation**:
```bash
# Check service health
make health

# View collection info
make info
```

4. **Load sample data**:
```bash
make load-sample
```

5. **Test search functionality**:
```bash
# Interactive search mode
make interactive

# Single query test
make search QUERY="machine learning"
```

### Alternative Local Development Setup

For development without Docker:

```bash
# Install dependencies
make dev-install

# Start only Qdrant via Docker
make dev-run

# In another terminal, run the service
QDRANT_HOST=localhost python main.py
```

## Testing Instructions

### Automated Tests

```bash
# Run comprehensive system test
make test

# Check service health
python src/test_client.py --service-url http://localhost:8000
```

### Manual Testing

```bash
# Interactive search mode
python src/test_client.py --interactive

# Single search query
python src/test_client.py --query "your search query"

# Add test document
curl -X POST "http://localhost:8000/add_document" \
     -H "Content-Type: application/json" \
     -d '{"text": "Test document", "metadata": {"category": "test"}}'
```

### Load Testing Data

```bash
# Load from JSON file
make load-json FILE=data/documents.json

# Load from CSV file  
make load-csv FILE=data/documents.csv COLUMN=text

# Load from text file
make load-txt FILE=data/document.txt
```

## Project Structure

```
qdrantragservice/
├── main.py                 # FastAPI application and RAG service logic
├── src/
│   ├── data_loader.py      # Data loading utilities for various formats
│   └── test_client.py      # Testing and interaction client
├── docker-compose.yaml     # Multi-service Docker configuration
├── Dockerfile             # RAG service container definition
├── Makefile               # Development and deployment commands
├── pyproject.toml         # Python project configuration
├── requirements.txt       # Python dependencies
├── .python-version        # Python version specification (3.13)
├── .gitignore            # Git ignore patterns
└── README.md             # This documentation
```

### Folder Descriptions

- **`/`** - Root directory containing main application file and configuration
- **`src/`** - Source code for utilities and testing tools
  - `data_loader.py` - Handles loading documents from JSON, CSV, and TXT files
  - `test_client.py` - Provides testing utilities and interactive search interface
- **Configuration files** - Docker, Python, and build configurations
- **`qdrant_storage/`** - Qdrant database storage (created at runtime)
- **`data/`** - Directory for input data files (created at runtime)

## API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **Service Health**: http://localhost:8000/health

## Additional Resources

- **Makefile Commands**: Run `make help` to see all available commands
- **Docker Logs**: Use `make logs` to view service logs
- **Collection Management**: Use `make clear-collection` to reset data
- **Development Setup**: See `make dev-install` and `make dev-run` for local development

For detailed API usage examples and advanced configuration options, refer to the interactive documentation at `/docs` when the service is running.