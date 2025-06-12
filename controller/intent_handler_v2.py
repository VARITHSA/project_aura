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
    
    ***Note: if the query is a video name, use the "play" task. If it is a channel name, use the "subscribe" or "unsubscribe" task.***
    _if the query is to play something, include search in tasks included play task._
    
    
    For the 'stackoverflow' intent, support tasks like:
    - "search": <query>
    - "extract_answer": true
    - "save_answer": true
    - "upvote": true
    - "open_profile": true
    - "reset": true
    
    For the 'wikipedia' intent, support tasks like:
    - "search": <topic>
    - "read_summary": true
    - "speak_summary": true
    
    
    For the 'weather' intent, support tasks like:
    - "get_weather": <location>
    
    For the 'google' intent, support tasks like:
    - "search": <query> 
    
    "if a query is has words like :
     - "look for details about" or asking general information about a topic, classify the intent as 'google' and use the "search" task.
     - "look for a definition of" or asking a definition of a word, classify the intent as 'google' and use the "search" task.
    - "find" or "search" for a specific topic, classify the intent as 'google' and use the "search" task. 
    - "open" a specific website, classify the intent as 'google' and use the "open" task.
    
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
    "Get weather in Bangalore" →
    {{
      "intent": "weather",
      "tasks": {{
        "get_weather": "Bangalore"
      }}
    }}
    "Search machine learning on Wikipedia" →
    {{
      "intent": "wikipedia",
      "tasks": {{
        "search": "machine learning",
        "read_summary": true
     }}
    }}
    "Find how to merge dicts in Python and extract answer" →
    {{
      "intent": "stackoverflow",
      "tasks": {{
        "search": "how to merge dicts in Python",
        "extract_answer": true
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
      