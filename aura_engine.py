from controller.intent_handler_v2 import IntentHandler_V2
from controller.intent_voice_handler import IntentVoiceHandler
from controller.voice_control import VoiceHandler
from controller.workflow_manager import WorkflowManager


class AuraEngine:
    def __init__(self):
        print("🔧 Initializing AURA components...")
        self.voice_handler = VoiceHandler()
        self.intent_classifier = IntentHandler_V2()
        self.intent_voice_handler = IntentVoiceHandler()
        self.workflow_manager = WorkflowManager(self.voice_handler, self.intent_voice_handler)
        
    def process_command(self, command: str) -> str:
        if not command:
            return "⚠️ Empty command received."
        
        if command.lower() in ["exit", "quit", "stop"]:
            self.voice_handler.speak("Goodbye!")
            return "👋 Exiting AURA."
        
        print(f"🧠 Detected command: {command}")
        intent_data = self.intent_classifier.classify_intent(command)
        print(f"🧩 Intent Data: {intent_data}")
        try:
            self.workflow_manager.execute_workflow(intent_data, command)
            return "✅ Workflow executed successfully."
        except Exception as e:
            print(f"❌ Error: {e}")
            self.voice_handler.speak("An error occurred while processing your request.")
            return f"❌ Error: {str(e)}"