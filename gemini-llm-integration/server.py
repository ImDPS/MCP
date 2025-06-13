import os
import json
import sys
import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../.env")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Create an MCP server
logger.info("Initializing MCP server...")
try:
    mcp = FastMCP(
        name="Company Knowledge Base Server",
        host="0.0.0.0",
        port=8050,
    )
    logger.info("MCP server initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize MCP server: {e}")
    raise


def load_knowledge_base():
    """Load and cache the knowledge base."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        kb_path = os.path.join(current_dir, "knowledge_base.json")
        
        logger.info(f"Loading knowledge base from: {kb_path}")
        
        if not os.path.exists(kb_path):
            # Create a sample knowledge base if it doesn't exist
            sample_kb = {
                "qa_pairs": [
                    {
                        "question": "What is the company's vacation policy?",
                        "answer": "Employees receive 15 days of paid vacation per year for the first 2 years, 20 days after 2 years of service, and 25 days after 5 years. Vacation days must be approved by your manager in advance."
                    },
                    {
                        "question": "What is the remote work policy?",
                        "answer": "Employees can work remotely up to 3 days per week with manager approval. Full remote work is available for senior employees and special circumstances. All remote workers must maintain core hours of 10 AM - 3 PM EST."
                    },
                    {
                        "question": "What benefits does the company offer?",
                        "answer": "We offer comprehensive health insurance (medical, dental, vision), 401k with 4% company match, life insurance, disability insurance, flexible spending accounts, employee assistance program, and professional development stipend of $2000 per year."
                    },
                    {
                        "question": "How many sick days do employees get?",
                        "answer": "Employees receive 10 paid sick days per year. Unused sick days can be carried over up to a maximum of 20 days. Extended sick leave may be available under FMLA."
                    },
                    {
                        "question": "What is the dress code?",
                        "answer": "We have a business casual dress code. On Fridays, casual dress is acceptable. For client meetings, business professional attire is required."
                    }
                ]
            }
            
            with open(kb_path, 'w') as f:
                json.dump(sample_kb, f, indent=2)
            logger.info("Created sample knowledge base")
        
        with open(kb_path, 'r') as f:
            return json.load(f)
            
    except Exception as e:
        logger.error(f"Error loading knowledge base: {e}")
        return {"qa_pairs": []}


# Load knowledge base at startup
KNOWLEDGE_BASE = load_knowledge_base()

# Initialize Gemini client for semantic search
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    logger.info("Gemini client initialized for semantic search")
else:
    gemini_client = None
    logger.warning("GEMINI_API_KEY not found - falling back to keyword search")


@mcp.tool()
async def get_knowledge_base(query: str) -> str:
    """Search and retrieve information from the company knowledge base using LLM-powered semantic search.
    
    This tool uses advanced AI to understand your question and find the most relevant information
    from company policies, benefits, and procedures stored in the knowledge base.
    
    Use this for any questions about:
    - Vacation and time-off policies
    - Remote work policies  
    - Employee benefits
    - Sick leave policies
    - Dress codes
    - Training and development
    - HR procedures
    - Safety policies
    - Any other company policies or procedures
    
    Args:
        query: The user's question about company policies or information
    
    Returns:
        The most relevant information from the knowledge base based on semantic understanding
    """
    logger.info(f"get_knowledge_base called with query: {query}")
    
    try:
        if not KNOWLEDGE_BASE.get('qa_pairs'):
            return "Knowledge base is empty or not available."
        
        # Use LLM-powered semantic search if available
        if gemini_client:
            return await _semantic_search(query)
        else:
            # Fallback to keyword search
            return _keyword_search(query)
            
    except Exception as e:
        error_msg = f"Error accessing knowledge base: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


async def _semantic_search(query: str) -> str:
    """Use Gemini LLM for semantic search through the knowledge base."""
    try:
        # Prepare the knowledge base content for the LLM
        kb_content = []
        for i, qa in enumerate(KNOWLEDGE_BASE.get('qa_pairs', []), 1):
            kb_content.append(f"{i}. Q: {qa.get('question', '')}\n   A: {qa.get('answer', '')}")
        
        kb_text = "\n\n".join(kb_content)
        
        # Create a semantic search prompt
        search_prompt = f"""You are a helpful company knowledge base assistant. A user has asked a question, and you need to find the most relevant information from our company knowledge base.

User Question: "{query}"

Company Knowledge Base:
{kb_text}

Instructions:
1. Analyze the user's question to understand what they're looking for
2. Find the most relevant Q&A pair(s) that answer their question
3. If you find relevant information, return it in this format:
   "Here's what I found in the company knowledge base:
   
   Q: [Question]
   A: [Answer]"
   
4. If you find multiple relevant items, include all of them
5. If no information directly answers their question, say "I couldn't find specific information about that in our knowledge base. Here are some related topics that might help:" and list the closest matches
6. Always be helpful and professional
7. Don't make up information that's not in the knowledge base

Please provide your response now."""

        # Call Gemini for semantic search
        response = gemini_client.models.generate_content(
            model="gemini-1.5-flash",
            contents=search_prompt,
            config={
                "temperature": 0.1,  # Low temperature for consistent, factual responses
                "max_output_tokens": 1024
            }
        )
        
        if response and hasattr(response, 'text') and response.text:
            logger.info("Semantic search completed successfully")
            return response.text.strip()
        else:
            logger.warning("No response from Gemini, falling back to keyword search")
            return _keyword_search(query)
            
    except Exception as e:
        logger.error(f"Error in semantic search: {e}")
        return _keyword_search(query)


def _keyword_search(query: str) -> str:
    """Fallback keyword-based search method."""
    logger.info("Using keyword search fallback")
    
    query_lower = query.lower()
    relevant_answers = []
    
    # Enhanced keyword list
    query_keywords = [
        'vacation', 'remote', 'benefit', 'sick', 'dress', 'policy', 'time off', 'leave', 'work',
        'health', 'insurance', '401k', 'retirement', 'training', 'development', 'expense',
        'travel', 'equipment', 'harassment', 'safety', 'overtime', 'referral', 'social media',
        'flexible', 'schedule', 'mental health', 'probation', 'review', 'performance'
    ]
    
    # Search through Q&A pairs for relevant information
    for qa in KNOWLEDGE_BASE.get('qa_pairs', []):
        question = qa.get('question', '').lower()
        answer = qa.get('answer', '').lower()
        
        # Check if any query keywords match with question or answer content
        for keyword in query_keywords:
            if keyword in query_lower and (keyword in question or keyword in answer):
                relevant_answers.append(f"Q: {qa.get('question', '')}\nA: {qa.get('answer', '')}")
                break
    
    if relevant_answers:
        result = "Here's what I found in the company knowledge base:\n\n" + \
                "\n\n".join(relevant_answers)
        logger.info("Found relevant information using keyword search")
        return result
    else:
        # If no specific match, return limited information
        formatted_info = "I couldn't find specific information about that query. Here are some available topics:\n\n"
        
        for i, qa in enumerate(KNOWLEDGE_BASE.get('qa_pairs', [])[:5], 1):  # Limit to first 5
            question = qa.get('question', '')
            formatted_info += f"{i}. {question}\n"
        
        formatted_info += f"\nTotal topics available: {len(KNOWLEDGE_BASE.get('qa_pairs', []))}"
        logger.info("No specific match found, returning topic list")
        return formatted_info


# Run the server
if __name__ == "__main__":
    logger.info("Starting MCP server with stdio transport...")
    try:
        mcp.run(transport="stdio")
        logger.info("MCP server is running and ready to accept connections")
    except Exception as e:
        logger.error(f"Error running MCP server: {e}")
        raise