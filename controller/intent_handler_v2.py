import os

import google.generativeai as genai
from dotenv import load_dotenv

from controller.api_usage_limiter import GeminiUsageLimiter


class IntentHandler_V2:
    def __init__(self):
        self.usage_limiter = GeminiUsageLimiter()
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.supported_intents = ["youtube", "wikipedia"] 
        
        
        
    def classify_intent(self, user_input: str) -> str:
        """Classify the intent of the transcribed text using Gemini API."""
        prompt = f"""
        You are the best intent classifier in the world. You can classify the intent of a user's input into one of the following categories and also retrive the relevant tasks from the given input and classify them into the relevant categories:
        {','.join(self.supported_intents)}.
        Return a JSON object in the following format:
        {{
          "intent": "<intent name>",
          "task": "<what the user wants to do>"
        }}

        Examples:
        "Open YouTube and search for senorita" →
        {{
          "intent": "youtube",
          "task": "senorita"
        }}

        "Tell me about the Eiffel Tower from Wikipedia" →
        {{
          "intent": "wikipedia",
          "task": "Eiffel Tower"
        }}

        "What's the weather in Bangalore?" →
        {{
          "intent": "weather",
          "task": "Bangalore"
        }}

        Now classify:
        "{user_input}" →
        """
        try:
            if self.usage_limiter.can_make_call():
              response = self.model.generate_content(prompt)
              text = response.text.strip()
              if text.startswith("```"):
                  text = text.strip("`").split("\n", 1)[-1].strip()
              return eval(text)
            else:
              print("❌ Gemini call skipped to stay within free tier.")
        except Exception as e:
            return {"intent": "error", "task": str(e)} 