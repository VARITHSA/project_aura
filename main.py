from models.automation_youtube import YouTubeBot
import time
from controller.voice_control import VoiceHandler
# --- Run Script ---
if __name__ == "__main__":
    bot = YouTubeBot()
    voice = VoiceHandler()
    # search_element = input("what do u want to search?")
    try:
       voice.test_microphone()
       bot.open_youtube()
       query = voice.listen()
       if query:
           bot.search_video(query )
           bot.play_first_video()
           bot.skip_ad_if_present()


    # try:
    #     bot.open_youtube()
    #     bot.search_video(search_element)
    #     bot.play_first_video()
    #     bot.skip_ad_if_present()
    #     time.sleep(30)  # Let video play
    finally:
        input("Press Enter to close browser...")
        bot.quit()
