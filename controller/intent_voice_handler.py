import os
import sys

import google.generativeai as genai
from dotenv import load_dotenv

from controller.voice_control import VoiceHandler


class IntentVoiceHandler:
    def __init__(self):
        self.voice_handler = VoiceHandler()
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY_v2")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY_v2 environment variable is not set.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    
    def get_response(self, user_input):
        prompt = f"""
        You are a smart and professional voice assistant. Understand the intent and respond accordingly.
        
        
        Respond with a concise and relevant answer.
        
        Examples:
        - if asked about your name, respond with "Hello! I am AURA"
        - if asked about your purpose, respond with "I am AURA, your personal assistant. I can help you with various tasks like searching for videos, checking the weather, and more."
        - if asked about your capabilities, respond with "I can help you with tasks like searching for videos, checking the weather, and more."
        - if said with "hey Aura" respond with the current state of aura and then say  iam listening....
        - if greeted(hi,hello), respond with hello! I am AURA, your personal assistant. How can I help you today?
        - if asked about the weather, respond with the current weather in the user's location.  
        - if asked to search for a video, respond with "Searching for <video name> on YouTube."
        - if asked to search for a topic, respond with "Searching for <topic> on Wikipedia."    
        - if asked to play a video, respond with "Playing <video name> on YouTube."
        - if asked to stop, respond with "Exiting AURA. Goodbye!"
        - if asked to skip an ad, respond with "Skipping the ad."
        - if asked to like a video, respond with "Liking the video."
        - if asked to dislike a video, respond with "Disliking the video."
        - if the code is struck, respond with "Sorry, I am unable to process your request at the moment. Please try again later."
        
        Also be and sound natural and friendly in your responses.
        User input: "{user_input}"
        AURA:
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()