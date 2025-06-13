# Project Structure

```
MCP/
├── .venv/                   # Virtual environment (gitignored)
├── .git/                    # Git repository
├── .env                     # Environment variables
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
│
├── gemini-llm-integration/ # Google Gemini LLM integration
│   ├── __pycache__/        # Python bytecode cache
│   ├── client-simple.py    # Enhanced Gemini client with interactive and batch modes
│   ├── knowledge_base.json # Comprehensive company knowledge base
│   ├── server.py           # Enhanced server with semantic search capabilities
│   └── README.md           # Gemini integration documentation
│
├── plan/                  # Project planning and documentation
│   └── project_structure.md # This file
│
├── test_gemini.py         # Test script for Gemini API
├── requirements.txt        # Project dependencies
└── README.md              # Main project documentation
```

## Key Components

### Gemini LLM Integration
- **Enhanced Client (`client-simple.py`)**
  - Interactive and batch query modes
  - Robust error handling and tool integration
  - Automatic function calling with Gemini
  - Clean user interface

- **Server (`server.py`)**
  - Semantic search using Gemini 1.5 Flash
  - Fallback to keyword search
  - Comprehensive knowledge base covering HR policies, benefits, and procedures
  - Structured error handling and logging

- **Knowledge Base (`knowledge_base.json`)**
  - Organized Q&A format
  - Covers policies, benefits, and procedures
  - Easily extensible structure

### Development
- Uses UV for package management
- Includes development tools (black, isort, mypy, pytest)
- Follows Python best practices
- Comprehensive logging and error handling

## Environment Setup

1. Create and activate virtual environment:
   ```bash
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```
