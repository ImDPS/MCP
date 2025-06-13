import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from google import genai
from google.genai import types
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables
load_dotenv("../.env")

# Validate API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please check your .env file.")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


class GeminiMCPClient:
    """Enhanced Gemini MCP Client with improved error handling and structure."""
    
    def __init__(self, server_script_path: str = "server.py", server_env: Optional[Dict[str, str]] = None):
        """Initialize the client with server configuration.
        
        Args:
            server_script_path: Path to the MCP server script
            server_env: Environment variables to pass to the server
        """
        self.server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
            env=server_env or {}
        )
        
    def format_tools_for_gemini(self, mcp_tools) -> List[types.Tool]:
        """Format MCP tools for Gemini API with improved schema handling.
        
        Args:
            mcp_tools: The result from session.list_tools()
            
        Returns:
            List of tools formatted for Gemini
        """
        tools = []
        for tool in mcp_tools.tools:
            try:
                # Clean up the input schema by removing unsupported properties
                parameters = {
                    k: v for k, v in tool.inputSchema.items()
                    if k not in ["additionalProperties", "$schema"]
                } if hasattr(tool, 'inputSchema') and tool.inputSchema else {"type": "object"}
                
                # Create tool in Gemini format
                gemini_tool = types.Tool(
                    function_declarations=[{
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": parameters
                    }]
                )
                
                tools.append(gemini_tool)
                print(f"Formatted tool: {tool.name}")
                
            except Exception as e:
                print(f"Warning: Failed to format tool {tool.name}: {e}")
                continue
                
        return tools

    async def process_query(self, session: ClientSession, query: str, model: str = "gemini-1.5-flash") -> str:
        """Process a query using Gemini and available MCP tools.

        Args:
            session: Active MCP session
            query: The user query
            model: Gemini model to use

        Returns:
            The response from Gemini or tool execution
        """
        try:
            # Get available tools
            mcp_tools = await session.list_tools()
            tools = self.format_tools_for_gemini(mcp_tools)
            
            print(f"\nProcessing query: {query}")
            
            # Enhanced prompt to encourage tool usage
            enhanced_query = f"""
You have access to company knowledge base tools. Please use the available tools to search for information about: {query}

Available tools can help you find information about:
- Company policies (vacation, remote work, dress code)
- Employee benefits
- Sick leave policies
- Any other company-related information

Please use the appropriate tool to search for this information rather than saying you don't have access to it.

User question: {query}
"""
            
            # Generate response from Gemini
            response = client.models.generate_content(
                model=model,
                contents=enhanced_query,
                config=types.GenerateContentConfig(
                    temperature=0,
                    tools=tools,
                    tool_config={'function_calling_config': {'mode': 'AUTO'}},
                ),
            )
            
            # Process the response
            if not response.candidates:
                return "Error: No response candidates from Gemini"
                
            candidate = response.candidates[0]
            
            # Check for function call
            if (candidate.content.parts and 
                hasattr(candidate.content.parts[0], 'function_call') and
                candidate.content.parts[0].function_call):
                
                function_call = candidate.content.parts[0].function_call
                
                if function_call.name:
                    print(f"Executing function: {function_call.name}")
                    print(f"Arguments: {dict(function_call.args)}")
                    
                    try:
                        # Call the MCP tool
                        result = await session.call_tool(
                            function_call.name, 
                            arguments=dict(function_call.args)
                        )
                        
                        # Format and return the result
                        return self._format_tool_result(result)
                        
                    except Exception as e:
                        return f"Error executing tool {function_call.name}: {str(e)}"
            
            # If no function call, return direct text response
            if candidate.content.parts:
                text_parts = [part.text for part in candidate.content.parts if hasattr(part, 'text')]
                if text_parts:
                    return '\n'.join(text_parts)
            
            # Fallback to response.text if available
            if hasattr(response, 'text') and response.text:
                return response.text
                
            return "No meaningful response generated"
            
        except Exception as e:
            return f"Error processing query: {str(e)}"

    def _format_tool_result(self, result) -> str:
        """Format tool execution result for display.
        
        Args:
            result: The result from MCP tool execution
            
        Returns:
            Formatted result string
        """
        try:
            if hasattr(result, 'content') and result.content:
                content_text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                
                # Try to parse and format as JSON
                try:
                    parsed_json = json.loads(content_text)
                    return json.dumps(parsed_json, indent=2)
                except json.JSONDecodeError:
                    # Return as plain text if not valid JSON
                    return content_text
            
            return str(result)
            
        except Exception as e:
            return f"Error formatting result: {str(e)}"

    async def run_interactive_session(self):
        """Run an interactive session with the MCP server."""
        print("=== Gemini MCP Interactive Client ===")
        print("Type 'quit' or 'exit' to end the session")
        print("Connecting to MCP server...")
        
        try:
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # List available tools
                    mcp_tools = await session.list_tools()
                    print(f"\nConnected! Available tools ({len(mcp_tools.tools)}):")
                    for tool in mcp_tools.tools:
                        print(f"  - {tool.name}: {tool.description}")
                    
                    print("\nReady for queries!")
                    
                    while True:
                        try:
                            query = input("\n> ").strip()
                            
                            if query.lower() in ['quit', 'exit', 'q']:
                                break
                            
                            if not query:
                                continue
                            
                            print("\n" + "="*50)
                            response = await self.process_query(session, query)
                            print("Response:")
                            print(response)
                            print("="*50)
                            
                        except KeyboardInterrupt:
                            print("\nUse 'quit' to exit gracefully.")
                            continue
                        except Exception as e:
                            print(f"Error: {e}")
                            continue
                            
        except Exception as e:
            print(f"Failed to connect to MCP server: {e}")
            print("Please ensure the server script exists and dependencies are installed.")

    async def run_batch_queries(self, queries: List[str]):
        """Run a batch of predefined queries.
        
        Args:
            queries: List of queries to process
        """
        print("=== Gemini MCP Batch Client ===")
        print("Connecting to MCP server...")
        
        try:
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # List available tools
                    mcp_tools = await session.list_tools()
                    print(f"\nConnected! Available tools: {[tool.name for tool in mcp_tools.tools]}")
                    
                    # Process each query
                    for i, query in enumerate(queries, 1):
                        print(f"\n{'='*60}")
                        print(f"Query {i}/{len(queries)}: {query}")
                        print("-" * 60)
                        
                        try:
                            response = await self.process_query(session, query)
                            print("Response:")
                            print(response)
                            
                            # Small delay between queries
                            if i < len(queries):
                                await asyncio.sleep(1)
                                
                        except Exception as e:
                            print(f"Error processing query {i}: {e}")
                            continue
                            
        except Exception as e:
            print(f"Failed to connect to MCP server: {e}")


async def main():
    """Main entry point with multiple operation modes."""
    import sys
    
    # Initialize client
    client_instance = GeminiMCPClient("server.py")
    
    # Improved test queries that are more explicit
    test_queries = [
        "dress code?"
    ]
    
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
            # Interactive mode
            await client_instance.run_interactive_session()
        else:
            # Batch mode with test queries
            await client_instance.run_batch_queries(test_queries)
            
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())