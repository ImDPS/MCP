# Gemini LLM Integration with Semantic Search

This project implements a powerful client-server application that integrates Google's Gemini LLM for natural language understanding and semantic search capabilities. The system provides intelligent responses to queries about company policies, benefits, and procedures using an extensible knowledge base.

## Features

- **Semantic Search**: Uses Gemini 1.5 Flash for understanding natural language queries
- **Interactive & Batch Modes**: Run single queries or batch process multiple questions
- **Comprehensive Knowledge Base**: Covers HR policies, benefits, and company procedures
- **Robust Error Handling**: Graceful fallbacks and clear error messages
- **Clean Interface**: Simple command-line interface for easy interaction

## Project Structure

```
gemini-llm-integration/
├── client-simple.py    # Enhanced client with interactive and batch modes
├── knowledge_base.json # Comprehensive company knowledge base (Q&A format)
├── server.py          # Server with semantic search capabilities
└── README.md          # This documentation
```

## Prerequisites

- Python 3.11+
- UV package manager (recommended)
- Google Gemini API key
- Required Python packages (installed via requirements.txt)

## Setup

1. **Set up the virtual environment**:
   ```bash
   # From the project root
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   # Install core requirements
   uv pip install -r ../requirements.txt
   
   # Install development tools (optional)
   uv pip install black isort mypy pytest
   ```

3. **Configure environment variables**:
   Create a `.env` file in the project root with your Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Running the Application

1. **Start the server** in one terminal:
   ```bash
   python server.py
   ```
   The server will initialize and be ready to accept connections.

2. **Run the client** in another terminal:
   
   **Interactive mode** (for live queries):
   ```bash
   python client-simple.py --interactive
   ```
   
   **Batch mode** (for predefined queries):
   ```bash
   python client-simple.py
   ```

## Usage Examples

### Interactive Mode
```
> What is the dress code?
[System] Searching knowledge base...

Here's what I found in the company knowledge base:

Q: What is the dress code?
A: We have a business casual dress code. On Fridays, casual dress is acceptable. For client meetings, business professional attire is required.
```

### Batch Mode
Edit the `test_queries` list in `client-simple.py` to include your questions, then run:
```bash
python client-simple.py
```

## Extending the Knowledge Base

1. Edit `knowledge_base.json` to add or modify Q&A pairs
2. The system will automatically pick up changes when the server restarts
3. Follow the existing JSON structure for consistency

## Troubleshooting

- **API Key Issues**: Ensure your `GEMINI_API_KEY` is set in the `.env` file
- **Connection Errors**: Make sure the server is running before starting the client
- **Module Not Found**: Verify all dependencies are installed in your virtual environment

## License

This project is licensed under the MIT License - see the LICENSE file for details.
   python server.py
   ```

2. In a separate terminal, run the client:
   ```bash
   python client-simple.py
   ```

## Usage

The client provides a simple interface to interact with the Gemini LLM through the server. You can ask questions or make requests in natural language.

## Configuration

- Update `server.py` to modify server settings
- Update `client-simple.py` to change client behavior
- Add or modify tools in the server implementation as needed

## Troubleshooting

- Ensure your API key is correctly set in the `.env` file
- Check that the server is running before starting the client
- Verify that all dependencies are installed in the virtual environment
