import google.generativeai as genai
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

class IntentHandler:
    def __init__(self):
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        genai.configure(api_key=api_key)
        
        # Use the free model with lower token usage
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Rate limiting setup (free tier limits)
        self.requests_per_minute = 30  # Reduced from 60 to stay within limits
        self.requests_per_day = 1000   # Free tier daily limit
        self.request_timestamps = []
        self.daily_requests = 0
        self.last_reset = datetime.now()
        
        # Define available intents and their corresponding keywords
        self.intent_patterns = {
            'youtube': ['youtube', 'play', 'search', 'video'],
            'wikipedia': ['wikipedia', 'search', 'lookup', 'find'],
            'bookmyshow': ['bookmyshow', 'movie', 'book', 'ticket', 'cinema'],
            'unknown': []
        }
        
        # Store automation instances
        self.automation_instances = {}
        
    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits for the free API"""
        current_time = datetime.now()
        
        # Reset daily counter if it's a new day
        if current_time.date() > self.last_reset.date():
            self.daily_requests = 0
            self.last_reset = current_time
        
        # Check daily limit
        if self.daily_requests >= self.requests_per_day:
            print("Daily request limit reached. Please try again tomorrow.")
            return False
        
        # Remove timestamps older than 1 minute
        self.request_timestamps = [ts for ts in self.request_timestamps 
                                 if current_time - ts < timedelta(minutes=1)]
        
        # Check per-minute limit
        if len(self.request_timestamps) >= self.requests_per_minute:
            print("Rate limit reached. Please wait a moment before trying again.")
            return False
        
        # Add current request
        self.request_timestamps.append(current_time)
        self.daily_requests += 1
        return True
        
    def _get_intent_prompt(self, command: str) -> str:
        """Create a prompt for Gemini to identify the intent"""
        return f"""Analyze command and respond with intent and parameters only.
Command: "{command}"
Format: Intent: [youtube/wikipedia/bookmyshow]
Parameters: [search terms]"""
    
    def classify_intent(self, command: str) -> Dict[str, Any]:
        """Use Gemini to classify the intent from the command"""
        try:
            # First try simple keyword matching
            command_lower = command.lower()
            for intent, keywords in self.intent_patterns.items():
                if any(keyword in command_lower for keyword in keywords):
                    # Extract parameters by removing intent keywords
                    parameters = command_lower
                    for keyword in keywords:
                        parameters = parameters.replace(keyword, '')
                    parameters = parameters.strip()
                    
                    if intent != 'unknown':
                        return {
                            'intent': intent,
                            'parameters': parameters if parameters else None,
                            'original_command': command
                        }
            
            # Only use Gemini if keyword matching fails and we're within rate limits
            if not self._check_rate_limit():
                return self._fallback_classify(command)
            
            prompt = self._get_intent_prompt(command)
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.1,
                    'max_output_tokens': 30,  # Reduced token usage
                }
            )
            
            # Parse the response
            response_text = response.text.strip()
            intent = None
            parameters = None
            
            for line in response_text.split('\n'):
                line = line.strip()
                if line.startswith('Intent:'):
                    intent = line.replace('Intent:', '').strip().lower()
                elif line.startswith('Parameters:'):
                    parameters = line.replace('Parameters:', '').strip()
            
            # Validate intent
            if intent not in self.intent_patterns:
                intent = 'unknown'
            
            return {
                'intent': intent,
                'parameters': parameters,
                'original_command': command
            }
            
        except Exception as e:
            print(f"Error classifying intent: {str(e)}")
            return self._fallback_classify(command)
    
    def _fallback_classify(self, command: str) -> Dict[str, Any]:
        """Fallback classification using simple keyword matching"""
        command_lower = command.lower()
        for intent, keywords in self.intent_patterns.items():
            if any(keyword in command_lower for keyword in keywords):
                parameters = command_lower
                for keyword in keywords:
                    parameters = parameters.replace(keyword, '')
                parameters = parameters.strip()
                
                return {
                    'intent': intent,
                    'parameters': parameters if parameters else None,
                    'original_command': command
                }
        
        return {
            'intent': 'unknown',
            'parameters': None,
            'original_command': command
        }
    
    def initialize_automation_instances(self, youtube_bot=None, wiki_bot=None, bookmyshow_bot=None):
        """Initialize automation instances that will be used for different intents"""
        self.automation_instances = {
            'youtube': youtube_bot,
            'wikipedia': wiki_bot,
            'bookmyshow': bookmyshow_bot
        }
    
    def execute_intent(self, intent_data: Dict[str, Any]) -> bool:
        """Execute the appropriate automation based on the identified intent"""
        intent = intent_data['intent']
        parameters = intent_data['parameters']
        
        if intent == 'unknown':
            print("Sorry, I couldn't understand the intent of your command.")
            return False
            
        automation = self.automation_instances.get(intent)
        if not automation:
            print(f"Automation for intent '{intent}' is not initialized.")
            return False
            
        try:
            if intent == 'youtube':
                automation.open_youtube()
                if parameters:
                    automation.search_video(parameters)
                    automation.play_first_video()
                    automation.skip_ad_if_present()
                    
            elif intent == 'wikipedia':
                automation.open_weki()
                if parameters:
                    automation.search_topic(parameters)
                    
            elif intent == 'bookmyshow':
                automation.open_site()
                # For BookMyShow, we might need more specific parameters
                # This is a basic implementation
                if parameters:
                    # Assuming parameters contains city and movie name
                    # You might want to parse this more specifically
                    automation.select_city("Bengaluru")  # Default city
                    automation.search_movie(parameters)
                    automation.click_first_result()
                    
            return True
            
        except Exception as e:
            print(f"Error executing intent {intent}: {str(e)}")
            return False
            
    def process_command(self, command: str) -> bool:
        """Process a voice command by classifying intent and executing it"""
        intent_data = self.classify_intent(command)
        return self.execute_intent(intent_data) 