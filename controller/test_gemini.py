import os
from dotenv import load_dotenv
import google.generativeai as genai
import time
from datetime import datetime, timedelta

def test_gemini_setup():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env file")
        print("Please make sure you have created a .env file with your API key")
        return False
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # List available models
        print("Available models:")
        for m in genai.list_models():
            if 'flash' in m.name:  # Only show flash models which are more efficient
                print(f"- {m.name}")
        
        # Use gemini-1.5-flash model (more efficient for free tier)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Try a simple test prompt with minimal tokens
        response = model.generate_content(
            "Say 'Hello' if you can read this.",
            generation_config={
                'temperature': 0.1,
                'max_output_tokens': 10
            }
        )
        
        if response and response.text:
            print("\n✅ Success! Gemini API is working correctly")
            print("Test response:", response.text)
            return True
        else:
            print("\n❌ Error: No response from Gemini API")
            return False
            
    except Exception as e:
        print("\n❌ Error testing Gemini API:", str(e))
        if "quota" in str(e).lower():
            print("\nYou've hit the free tier quota limits. Please:")
            print("1. Wait a few minutes before trying again")
            print("2. Consider using the keyword matching fallback more often")
            print("3. Visit https://ai.google.dev/gemini-api/docs/rate-limits for more info")
        return False

if __name__ == "__main__":
    print("Testing Gemini API setup...")
    test_gemini_setup() 