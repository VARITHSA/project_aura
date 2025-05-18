import time

from controller.voice_control import VoiceHandler
from models.automation_bookMyshow import BookMyShowAutomator
from models.automation_wikipedia import WikipediaBot
from models.automation_youtube import YouTubeBot
from controller.intent_handler import IntentHandler

def get_user_confirmation(intent_data):
    """Get user confirmation for the identified intent"""
    intent = intent_data['intent']
    parameters = intent_data['parameters']
    
    print("\nIdentified Intent:")
    print(f"Action: {intent.upper()}")
    print(f"Parameters: {parameters if parameters else 'None'}")
    
    while True:
        response = input("\nIs this correct? (yes/no/retry): ").lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        elif response in ['retry', 'r']:
            return 'retry'
        else:
            print("Please answer with 'yes', 'no', or 'retry'")

class AutomationManager:
    def __init__(self):
        self.youtube_bot = None
        self.wiki_bot = None
        self.book_bot = None
        self.driver_path = "chromedriver.exe"
    
    def get_bot(self, intent):
        """Get or create the appropriate bot for the intent"""
        if intent == 'youtube':
            if not self.youtube_bot:
                self.youtube_bot = YouTubeBot()
            return self.youtube_bot
        elif intent == 'wikipedia':
            if not self.wiki_bot:
                self.wiki_bot = WikipediaBot()
            return self.wiki_bot
        elif intent == 'bookmyshow':
            if not self.book_bot:
                self.book_bot = BookMyShowAutomator(driver_path=self.driver_path)
            return self.book_bot
        return None
    
    def close_bot(self, intent):
        """Close the bot for the given intent"""
        try:
            if intent == 'youtube' and self.youtube_bot:
                self.youtube_bot.quit()
                self.youtube_bot = None
            elif intent == 'wikipedia' and self.wiki_bot:
                self.wiki_bot.quit()
                self.wiki_bot = None
            elif intent == 'bookmyshow' and self.book_bot:
                self.book_bot.close()
                self.book_bot = None
        except Exception as e:
            print(f"Error closing {intent} bot: {str(e)}")
    
    def close_all(self):
        """Close all bots"""
        self.close_bot('youtube')
        self.close_bot('wikipedia')
        self.close_bot('bookmyshow')

if __name__ == "__main__":
    # Initialize voice handler
    voice = VoiceHandler()
    
    # Initialize automation manager
    automation_manager = AutomationManager()
    
    # Initialize intent handler
    intent_handler = IntentHandler()
    
    try:
        while True:
            print("\nListening for command... (Say 'quit' to exit)")
            command = voice.listen()
            
            if not command:
                print("No command detected. Please try again.")
                continue
                
            if 'quit' in command.lower():
                print("Exiting...")
                break
            
            # Get intent classification
            intent_data = intent_handler.classify_intent(command)
            
            # Get user confirmation
            while True:
                confirmation = get_user_confirmation(intent_data)
                
                if confirmation == 'retry':
                    print("\nRetrying with different classification method...")
                    intent_data = intent_handler._fallback_classify(command)
                    continue
                    
                if confirmation:
                    # User confirmed, get the appropriate bot
                    intent = intent_data['intent']
                    bot = automation_manager.get_bot(intent)
                    
                    if bot:
                        # Update the intent handler with the current bot
                        intent_handler.initialize_automation_instances(
                            youtube_bot=automation_manager.youtube_bot,
                            wiki_bot=automation_manager.wiki_bot,
                            bookmyshow_bot=automation_manager.book_bot
                        )
                        
                        # Execute the intent
                        print("\nExecuting command...")
                        success = intent_handler.execute_intent(intent_data)
                        
                        if success:
                            print("Command executed successfully.")
                            # Close the bot after successful execution
                            automation_manager.close_bot(intent)
                        else:
                            print("Failed to execute command. Please try again.")
                    else:
                        print(f"Error: Could not initialize {intent} bot")
                    break
                else:
                    print("\nCommand rejected. Please try again with a different command.")
                    break
            
            # Add a small delay between commands
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    finally:
        # Clean up all bots
        automation_manager.close_all()
        print("Program terminated.")
