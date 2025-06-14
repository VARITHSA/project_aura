from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from controller.intent_voice_handler import IntentVoiceHandler
from controller.voice_control import VoiceHandler
from models.automation_email import AutomationEmail
from models.automation_google import GoogleBot
from models.automation_stackoverflow import StackOverflowFlowBot
from models.automation_system import SystemBot
from models.automation_weather import WeatherBot
from models.automation_wikipedia import WikipediaBot
from models.automation_youtube import YouTubeBot


class WorkflowManager:
    def __init__(self, voice_handler, intent_voice_handler):
        self.voice_handler = voice_handler
        self.intent_agent = intent_voice_handler
        
        options = Options()
        # Suppress warnings and errors
        options.add_argument("--log-level=3")  # Only show fatal errors
        options.add_argument("--silent")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
        options.add_argument("--disable-software-rasterizer")  # Disable software rasterizer
        options.add_argument("--disable-webgl")  # Disable WebGL
        options.add_argument("--disable-webgl2")  # Disable WebGL 2
        options.add_argument("--disable-notifications")  # Disable notifications
        options.add_argument("--start-maximized")
        
        # Suppress TensorFlow warnings
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        service = Service(executable_path="chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options)
        
        
        self.bots = {
            "youtube": {
                "bot": YouTubeBot(driver=self.driver),
                "tasks": {
                    "search": "search_video",
                    "play": "play_first_video",
                    "like": "like_video",
                    "dislike": "dislike_video",
                    "subscribe": "subscribe_channel",
                    "unsubscribe": "unsubscribe_channel",
                    "open": "open_youtube"
                }
            },
            "wikipedia": {
                "bot": WikipediaBot(driver=self.driver),
                "tasks": {
                    "search": "search_topic",
                    "open": "open_wiki"
                }
            },
            "google": {
                "bot": GoogleBot(driver=self.driver),
                "tasks": {
                    "search": "search",
                    "open": "start"
                }
            },
            "stackoverflow": {
                "bot": StackOverflowFlowBot(driver=self.driver),
                "tasks": {
                    "open": "open_stackoverflow",
                    "search": "search_query",
                    "top_result": "open_top_result",
                    "extract_answer": "extract_accepted_answer",
                    "save_answer": "save_answer_to_file",
                    "upvote": "upvote_question",
                    "profile": "go_to_user_profile",
                    "reset": "reset",
                    "quit": "quit"
                },
            },
            "weather":{
                "bot": WeatherBot(driver=self.driver),
                "tasks": {
                    "get_weather": "get_weather",
                    "quit": "quit"
                }
            },
            "email": {
                "bot": AutomationEmail(),
                "tasks": {
                    "send": "send_email"
                }
            },
            "system":{
                "bot": SystemBot(),
                "tasks": {
                "shutdown": "shutdown",
                "restart": "restart",
                "sleep": "sleep",
                "volume_up": "volume_up",
                "volume_down": "volume_down",
                "mute": "mute",
                "take_screenshot": "take_screenshot",
                "open_app": "open_app"
                }
            }
        }
        
    
    
    
    def shutdown(self):
        """Gracefully shutdown browser."""
        try:
            if self.driver:
                self.driver.quit()
                print("🛑 ChromeDriver closed successfully.")
        except Exception as e:
            print(f"❌ Error closing ChromeDriver: {e}")
    
    def execute_workflow(self, intent_data, text):
        intent = intent_data.get("intent")
        if not intent:
            print("❌ No intent found.")
            return

        if intent not in self.bots:
            print(f"❌ Unknown intent: {intent}")
            return

        bot_info = self.bots[intent]
        bot = bot_info["bot"]
        task_map = bot_info["tasks"]
        tasks = intent_data.get("tasks", {})

        print(f"🔧 Executing intent '{intent}' with tasks: {list(tasks.keys())}")

        for task, value in tasks.items():
            method_name = task_map.get(task)
            if not method_name:
                print(f"❌ Task '{task}' not defined in mapping.")
                continue

            method = getattr(bot, method_name, None)
            if not callable(method):
                print(f"❌ Method '{method_name}' not found in {bot.__class__.__name__}")
                continue

            try:
                print(f"🔍 Calling {method_name} in {bot.__class__.__name__} with value: {value}")
                if method.__code__.co_argcount > 1:
                    method(value)
                else:
                    method()

                voice = self.intent_agent.get_response(text)
                print(f"🗣️ AURA: {voice}")
                self.voice_handler.speak(voice)

                print(f"✅ Successfully executed: {method_name}")
            except Exception as e:
                print(f"❌ Error while executing '{method_name}': {e}")
                self.voice_handler.speak(f"Something went wrong with {method_name}.")

