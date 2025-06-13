# Client-Server Implementation

This directory contains the client and server implementations for the MCP (Model Control Protocol) system, providing both SSE (Server-Sent Events) and stdio-based communication channels.

## Project Structure

```
client-server/
├── client-sse.py     # SSE client implementation
├── client-stdio.py   # stdio client implementation
├── server.py         # Main server implementation
├── requirements.txt  # Project dependencies
```

## Prerequisites

- Python 3.8+
- UV package manager (for virtual environment)
- Dependencies listed in the root `requirements.txt`

## Setup

1. From the project root, create and activate the virtual environment (if not already done):
   ```bash
   # In the project root directory
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install dependencies from the root directory
   uv pip install -r ../requirements.txt
   ```
   
   Note: The virtual environment should be created in the project root directory, not in this folder.

## Available Clients

### SSE Client (`client-sse.py`)
- Uses Server-Sent Events for communication
- Suitable for web-based clients
- Supports real-time updates

### Stdio Client (`client-stdio.py`)
- Uses standard input/output for communication
- Suitable for command-line interfaces
- Simpler setup for local development

## Running the Application

1. Start the server:
   ```bash
   python server.py
   ```

2. In a separate terminal, run either client:
   ```bash
   # For SSE client
   python client-sse.py
   
   # For stdio client
   python client-stdio.py
   ```

## Development

- The server implements the MCP protocol
- Clients connect to the server using either SSE or stdio
- New tools can be added by implementing the appropriate handlers in the server

## Dependencies

- `uv`: Fast Python package installer and resolver
- Other dependencies are listed in `requirements.txt`

## License

[Specify your license here]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request