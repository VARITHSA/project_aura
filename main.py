
import sys
import time

from controller.intent_handler_v2 import IntentHandler_V2
from controller.voice_control import VoiceHandler
from models.automation_wikipedia import WikipediaBot
from models.automation_youtube import YouTubeBot


class WorkFlowManager:
    def __init__(self):
        self.youtube_bot = YouTubeBot()
        self.wikipedia_bot = WikipediaBot()
        self.voice_handler = VoiceHandler()
        
    def youtube_workflow(self, task):
        self.voice_handler.speak("Opening YouTube...")
        print("Opening YouTube...")
        self.youtube_bot.open_youtube()
        self.voice_handler.speak(f"Searching for {task} on YouTube...")
        print(f"Searching for {task} on YouTube...")
        self.youtube_bot.search_video(task)
        self.youtube_bot.play_first_video()
        self.voice_handler.speak("looking for ads to skip...")
        print("looking for ads to skip...")
        self.youtube_bot.skip_ad_if_present()
        self.voice_handler.speak("Enjoy your video!")
        
    def wikipedia_workflow(self, task):
        self.voice_handler.speak("Opening Wikipedia...")
        print("Opening Wikipedia...")
        self.wikipedia_bot.open_wiki()
        self.voice_handler.speak(f"Searching for {task} on Wikipedia...")
        print(f"Searching for {task} on Wikipedia...")
        self.wikipedia_bot.search_topic(task)
        self.voice_handler.speak("Done! You can ask me anything else.")
 

 
 
 
if __name__ == "__main__":
    workflow_manager = WorkFlowManager()
    intent_handler = IntentHandler_V2()
    
    workflow_manager.voice_handler.model_speak_init()
    
    while True:
        audio = workflow_manager.voice_handler.listen()
        workflow_manager.voice_handler.speak("Processing your request...")
        print("Processing your request...")
        time.sleep(1)      
        text = workflow_manager.voice_handler.transcribe_audio(audio)
        print(f"Transcribed text: {text}")
        workflow_manager.voice_handler.speak("Classifying your intent...")      
        intent_data = intent_handler.classify_intent(text)
        if not intent_data:
            continue
        
        intent = intent_data.get("intent")
        task = intent_data.get("task")
        
        if intent == "youtube":
            workflow_manager.youtube_workflow(task)
        elif intent == "wikipedia":
            workflow_manager.wikipedia_workflow(task)
        else:
            workflow_manager.voice_handler.speak("Sorry, I can't help with that.")
   
