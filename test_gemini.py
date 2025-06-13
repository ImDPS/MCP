#!/usr/bin/env python3
"""
Test script for Google Gemini API using gemini-1.5-flash model.
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional, Dict, Any

def setup_gemini() -> Optional[genai.GenerativeModel]:
    """Initialize and configure the Gemini model.
    
    Returns:
        Configured GenerativeModel instance or None if setup fails.
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in environment variables")
        print("ℹ️  Please set GEMINI_API_KEY in your .env file")
        return None
    
    try:
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Model configuration
        model_name = 'gemini-1.5-flash'
        print(f"\n🚀 Initializing {model_name}...")
        
        # Create model with safety settings and generation config
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
        
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Test the connection with a simple prompt
        response = model.generate_content("Say 'Hello, Gemini is working!'")
        if not response.text:
            print("❌ Failed to get response from the model")
            return None
            
        print("✅ Successfully connected to Gemini API")
        print(f"🤖 Model: {model_name} is ready!")
        return model
        
    except Exception as e:
        print(f"\n❌ Error initializing Gemini: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Verify your API key is correct and has access to the Gemini API")
        print("2. Check your internet connection")
        print("3. Make sure the model name is correct")
        print(f"4. Full error: {str(e)}")
        return None

def test_chat(model: genai.GenerativeModel, message: str) -> None:
    """Test chat functionality with the model.
    
    Args:
        model: Initialized GenerativeModel instance
        message: The message to send to the model
    """
    try:
        print(f"\n💬 You: {message}")
        print("\n🔄 Generating response...")
        
        # Start a chat session
        chat = model.start_chat(history=[])
        response = chat.send_message(message)
        
        print("\n🤖 Gemini:")
        if hasattr(response, 'text'):
            print(response.text)
        elif hasattr(response, 'candidates') and response.candidates:
            for candidate in response.candidates:
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        print(part.text)
        else:
            print("Received an unexpected response format.")
            print("Raw response:", response)
            
    except Exception as e:
        print(f"\n❌ Error during chat: {e}")

def main():
    """Main function to run the Gemini test."""
    # Initialize the model
    model = setup_gemini()
    if not model:
        return
    
    print("\n" + "="*50)
    print("🌟 Gemini 1.5 Flash Test Console")
    print("Type 'exit' or 'quit' to end the session")
    print("="*50 + "\n")
    
    # Interactive chat loop
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ('exit', 'quit'):
                print("\n👋 Goodbye!")
                break
                
            if user_input:
                test_chat(model, user_input)
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
