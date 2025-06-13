#!/usr/bin/env python3
"""
Simple script to test the Google Gemini API.
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        print("Please set GEMINI_API_KEY in your .env file")
        return
    
    try:
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # List available models
        print("\nAvailable models:")
        models = genai.list_models()
        for i, model in enumerate(models, 1):
            print(f"{i}. {model.name}")
            if i >= 10:  # Limit to first 10 models for brevity
                print("... and more")
                break
        
        # Get available model names
        available_models = [m.name for m in models]
        print(f"\nAvailable models (first 10): {', '.join(available_models[:10])}...")
        
        # We'll only use gemini-1.5-flash
        model_name = 'gemini-1.5-flash'
        
        # Check if the model is available
        if model_name not in available_models and f'models/{model_name}' not in available_models:
            print(f"\nError: {model_name} is not available. Available models:")
            for i, m in enumerate(available_models, 1):
                print(f"{i}. {m}")
            return
            
        print(f"\nUsing model: {model_name}")
            
        model = genai.GenerativeModel(model_name)
        
        # Generate content
        test_message = """You are a helpful AI assistant. Please respond to the following message:
        
        Tell me a short joke about programming and AI."""
        
        print("\nSending test message to the model...")
        response = model.generate_content(test_message)
        
        # Print the response
        print("\nResponse:")
        if hasattr(response, 'text'):
            print(response.text)
        elif hasattr(response, 'candidates') and response.candidates:
            # Handle different response formats
            for candidate in response.candidates:
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        print(part.text)
        else:
            print("Unexpected response format:", response)
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure your API key is valid and has access to the Gemini API")
        print("2. Check your internet connection")
        print("3. Make sure the model name is correct")
        print(f"4. Full error details: {str(e)}")

if __name__ == "__main__":
    main()
