
import sys
import time

from controller.intent_handler_v2 import IntentHandler_V2
from controller.intent_voice_handler import IntentVoiceHandler
from controller.voice_control import VoiceHandler
from models.automation_wikipedia import WikipediaBot
from models.automation_youtube import YouTubeBot


class WorkFlowManager:
    def __init__(self):
        self.youtube_bot = YouTubeBot()
        self.wikipedia_bot = WikipediaBot()
        self.voice_handler = VoiceHandler()
        self.intent_agent = IntentVoiceHandler()
        
   
    def youtube_workflow(self, intent_data, text):
        if not intent_data.get("intent"):
            print("No intent found in the input.")
        if intent_data.get("intent") != "youtube":
            print("❌ Invalid intent. This function only handles YouTube tasks.")
            return
        tasks = intent_data.get("tasks", {})
        ordered_tasks = ["search", "play", "like", "dislike", "subscribe", "unsubscribe"]
        print(tasks)
        for task in ordered_tasks:
            if task in tasks:
                val = tasks[task]
                
                if task == "search":
                    voice = self.intent_agent.get_response(text)
                    self.youtube_bot.open_youtube()
                    self.voice_handler.speak(voice)
                    print(voice)
                    self.youtube_bot.search_video(val)
                elif task == "play":
                    voice = self.intent_agent.get_response(text)
                    self.voice_handler.speak(voice)
                    print(voice)
                    self.youtube_bot.play_first_video()
                elif task == "like":
                    voice = self.intent_agent.get_response(text)
                    self.voice_handler.speak(voice)
                    print(voice)
                    self.youtube_bot.like_video()
                elif task == "dislike":
                    voice = self.intent_agent.get_response(text)
                    self.voice_handler.speak(voice)
                    print(voice)
                    self.youtube_bot.dislike_video()
                elif task == "subscribe":
                    voice = self.intent_agent.get_response(text)
                    self.voice_handler.speak(voice)
                    print(voice)
                    self.youtube_bot.subscribe_channel()
                elif task == "unsubscribe":
                    voice = self.intent_agent.get_response(text)
                    self.voice_handler.speak(voice)
                    print(voice)
                    self.youtube_bot.unsubscribe_channel()
                else:
                    print(f"❌ Invalid task: {task}. Supported tasks are: {', '.join(ordered_tasks)}")
                    time.sleep(2)
                    self.voice_handler.speak(f"❌ Invalid task: {task}. Supported tasks are: {', '.join(ordered_tasks)}")
                
        
            
    
    def wikipedia_workflow(self, task: dict, text: str):
        self.wikipedia_bot.initialize_driver()
        if "search" in task:
            topic = task["search"]
            voice = self.intent_agent.get_response(text)
            self.voice_handler.speak(voice)
            print(voice)
            self.wikipedia_bot.search_topic(topic)
   
            
        
        
        
    # def wikipedia_workflow(self, task):
    #     self.voice_handler.speak("Opening Wikipedia...")
    #     print("Opening Wikipedia...")
    #     self.wikipedia_bot.open_wiki()
    #     self.voice_handler.speak(f"Searching for {task} on Wikipedia...")
    #     print(f"Searching for {task} on Wikipedia...")
    #     self.wikipedia_bot.search_topic(task)
    #     self.voice_handler.speak("Done! You can ask me anything else.")
 

 
 
 
if __name__ == "__main__":
    intent_handler = IntentHandler_V2()
    intent_voice_handler = IntentVoiceHandler()
    workflow_manager = WorkFlowManager()
    vh = VoiceHandler()
    print("Welcome to the Voice-Controlled Automation System!")
    # vh = VoiceHandler()
    # vh.speak("Hey! I am AURA, your personal assistant. How can I help you today?")
    # while True:
    #     audio = vh.listen()
    #     text = vh.transcribe(audio)
    #     if text is None:
    #         continue
    #     if not vh.running:
    #         break
    vh.model_speak_init()
    print("AURA is listening...")
    while True:
        # audio = vh.listen()
        # text = vh.transcribe(audio)
        # if text is None:
        #     continue
        # if not vh.running:
        #     break
        # print(f"Transcribed text: {text}")
        # voice = intent_voice_handler.get_response(text)
        # vh.speak(voice)
        text = input("Enter your command: ")
        intent_data = intent_handler.classify_intent(text)
        print(f"Intent data: {intent_data}")
        if intent_data.get("intent") == "youtube":
            workflow_manager.youtube_workflow(intent_data, text)
            
            
            
            
            
            
            
            
            
            
            
            
            
   
        
   
