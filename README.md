# MCP Project with Gemini Integration

This project implements a Model Control Protocol (MCP) server with Google Gemini LLM integration, providing a flexible framework for building AI-powered applications.

## Project Structure

```
.
├── .venv/                   # Virtual environment (gitignored)
├── client-server/           # MCP client and server implementation
│   ├── client-sse.py        # SSE client
│   ├── client-stdio.py      # stdio client
│   └── server.py            # MCP server
├── gemini-llm-integration/  # Gemini LLM integration
│   ├── client-simple.py     # Simple Gemini client
│   ├── server.py            # Gemini server implementation
│   └── data/                # Knowledge base and data files
├── .env                     # Environment variables
├── .env.example            # Example environment variables
├── requirements.txt         # Project dependencies
└── test_gemini.py          # Test script for Gemini API
```

## Prerequisites

- Python 3.8+
- UV package manager (`pip install uv`)
- Google Gemini API key (for Gemini integration)

## Setup

1. Clone the repository and navigate to the project directory.

2. Create and activate a virtual environment:
   ```bash
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and update with your API keys:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Running the Project

### MCP Server

1. Start the MCP server:
   ```bash
   cd client-server
   python server.py
   ```

2. In a separate terminal, run a client:
   ```bash
   # For SSE client
   python client-sse.py
   
   # For stdio client
   python client-stdio.py
   ```

### Gemini Integration

1. Start the Gemini server:
   ```bash
   cd gemini-llm-integration
   python server.py
   ```

2. Run the Gemini client:
   ```bash
   python client-simple.py
   ```

## Development

- Format code:
  ```bash
  black .
  isort .
  ```

- Run tests:
  ```bash
  pytest
  ```

- Type checking:
  ```bash
  mypy .
  ```

## License

[Specify your license here]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
