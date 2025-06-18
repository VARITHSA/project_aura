import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from controller.intent_handler_v2 import IntentHandler_V2
from controller.intent_voice_handler import IntentVoiceHandler
from controller.voice_control import VoiceHandler
from controller.workflow_manager import WorkflowManager


def main():
    print("🔧 Initializing AURA components...")
    
    voice_handler = VoiceHandler()
    intent_classifier = IntentHandler_V2()
    intent_voice_handler = IntentVoiceHandler()
    workflow_manager = WorkflowManager(voice_handler, intent_voice_handler)
    
    init_message = "AURA is initializing..."
    print(f"💡 {init_message}")
    voice = intent_voice_handler.get_response(init_message)
    voice_handler.speak(voice)
    print(f"🗣️ {voice}")
    
    time.sleep(1)
    print("🟢 AURA is ready! Say or type your command (type 'exit' to quit).")

    while True:
        try:
            use_voice = input("🎤 Press [Enter] to use voice or type your command:").strip()
            if use_voice == "":
                audio = voice_handler.listen()
                if audio is None:
                    continue
                raw_text = voice_handler.transcribe(audio)
                if not raw_text:
                    continue
                text = voice_handler.correct_with_gpt(raw_text)
            else:
                text = use_voice.strip()
                
            if not text:
                print("⚠️ Empty input received.")
                continue
            if any(q in text.lower() for q in voice_handler.quit_words):
                voice_handler.speak("Goodbye!!!!!!")
                print("👋 Exiting AURA.")
                break
            print(f"🤖 Received: {text}")
            intent_data = intent_classifier.classify_intent(text)
            print(f"🤖 Intent: {intent_data['intent']}")
            
            workflow_manager.execute_workflow(intent_data,text)
            print("✅ Workflow executed successfully.")
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user.")
            break
        
        

    print("🛑 Shutting down AURA...")
        
        
        
        
        
        
    
    
    
if __name__ == "__main__":
    main()