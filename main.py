
import sys
import time

from controller.intent_handler_v2 import IntentHandler_V2
from controller.voice_control import VoiceHandler
from models.automation_wikipedia import WikipediaBot
from models.automation_youtube import YouTubeBot
from controller.intent_voice_handler import IntentVoiceHandler

class WorkFlowManager:
    def __init__(self):
        self.youtube_bot = YouTubeBot()
        self.wikipedia_bot = WikipediaBot()
        self.voice_handler = VoiceHandler()
        self.intent_agent = IntentVoiceHandler()
        
    def youtube_workflow(self, task:dict,text:str):
        
        if "search" in task:
            search_query = task["search"]
            voice = self.intent_agent.get_response(text)
            self.voice_handler.speak(voice)
            print(voice)
            self.youtube_bot.search_video(search_query)
        
        if "play" in task:
            video_name = task["play"]
            voice = self.intent_agent.get_response(text)
            self.voice_handler.speak(voice)
            print(voice)
            self.youtube_bot.play_video(video_name)
        
        if task.get("like"):
            voice = self.intent_agent.get_response(text)
            self.voice_handler.speak(voice)
            print(voice)
            self.youtube_bot.like_video()
        if task.get("dislike"):
            voice = self.intent_agent.get_response(text)
            self.voice_handler.speak(voice)
            print(voice)
            self.youtube_bot.dislike_video()
        if task.get("subscribe"):
            channel_name = task["subscribe"]
            voice = self.intent_agent.get_response(text)
            self.voice_handler.speak(voice)
            print(voice)
            self.youtube_bot.subscribe_channel(channel_name)
        if task.get("unsubscribe"):
            channel_name = task["unsubscribe"]
            voice = self.intent_agent.get_response(text)
            self.voice_handler.speak(voice)
            print(voice)
            self.youtube_bot.unsubscribe_channel(channel_name)
        if task.get("stop"):
            voice = self.intent_agent.get_response(text)
            self.voice_handler.speak(voice)
            print(voice)
            self.youtube_bot.stop_video()
        if task.get("skip_ad"):
            voice = self.intent_agent.get_response(text)
            self.voice_handler.speak(voice)
            print(voice)
            self.youtube_bot.skip_ad()
       
            
        
        
        
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
    print("Welcome to the Voice-Controlled Automation System!")
    
    
    while True:
        text = workflow_manager.voice_handler.listen()
        if text is None:
            continue
        text = workflow_manager.voice_handler.transcribe_audio(text)
        if text is None:
            continue
        voice = intent_voice_handler.get_response(text)
        workflow_manager.voice_handler.speak(voice)
        print(voice)

        print(f"Transcribed text: {text}")
        intent_data = intent_handler.classify_intent(text)
        voice = intent_voice_handler.get_response(intent_data)
        workflow_manager.voice_handler.speak(voice)
        print(f"Intent data: {intent_data}")
        if intent_data == "youtube":
            workflow_manager.youtube_workflow(intent_data, text)
        # text = input("Enter your command: ")   
        # print(f"Transcribed text: {text}")   
        # intent_data = intent_handler.classify_intent(text)
        # intent_response = intent_voice_handler.get_response(text)
        # print(f"Intent data: {intent_data}")
        # print(f"Intent response: {intent_response}")
        # if not intent_data:
        #     continue
        
        # intent = intent_data.get("intent")
        # task = intent_data.get("task")
        
        # if intent == "youtube":
        #     workflow_manager.youtube_workflow(task)
        # elif intent == "wikipedia":
        #     workflow_manager.wikipedia_workflow(task)
        # else:
        #     workflow_manager.voice_handler.speak("Sorry, I can't help with that.")
   
