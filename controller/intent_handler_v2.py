import json
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
        
    def classify_intent(self, user_input):
      prompt = f"""
    You are a precise intent and task classifier.

    Step 1: Classify the user input into one of the following intents:
    {', '.join(self.supported_intents)}.

    Step 2: Extract task-action pairs depending on the intent.

    For the 'youtube' intent, support tasks like:
    - "search": <video name or topic>
    - "play": <video name or topic>
    - "like": true
    - "dislike": true
    - "subscribe": <channel name or true>
    - "unsubscribe": <channel name or true>

    Return a JSON object in this format:
    {{
      "intent": "<intent name>",
      "tasks": {{
        "search": "<query>",
        "like": true,
        ...
      }}
    }}

    Only include keys that are relevant. Examples:

    "Search for Alan Walker and like the video" →
    {{
      "intent": "youtube",
      "tasks": {{
        "search": "Alan Walker",
        "like": true
      }}
    }}

    "Play MrBeast and subscribe" →
    {{
      "intent": "youtube",
      "tasks": {{
        "play": "MrBeast",
        "subscribe": "MrBeast"
      }}
    }}

    "Search cooking tutorials and dislike the video" →
    {{
      "intent": "youtube",
      "tasks": {{
        "search": "cooking tutorials",
        "dislike": true
      }}
    }}

    "Search for lo-fi music and like the top video" →
    {{
      "intent": "youtube",
      "tasks": {{
        "search": "lo-fi music",
        "like": true
      }}
    }}

    Now classify:
    "{user_input}" →
    """
      try:
        if self.usage_limiter.can_make_call():
            response = self.model.generate_content(prompt)
            self.usage_limiter.record_call()
            text = response.text.strip()
            if text.startswith("```"):
                text = text.strip("`").split("\n", 1)[-1].strip()
            return json.loads(text)
        else:
            print("❌ Gemini call skipped to stay within free tier.")
      except Exception as e:
        return {"intent": "error", "tasks": {"error":str(e)}}
      