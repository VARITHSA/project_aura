# models/voice_handler.py
import speech_recognition as sr
import pyttsx3

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def speak(self, text):
        """Convert text to speech."""
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listen for a command from the microphone and return the recognized speech."""
        with sr.Microphone() as source:
            print("🎤 Listening... (Make sure to speak clearly)")
            self.speak("What do you want to play on YouTube?")
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio)
            print(f"🎧 You said: {command}")
            self.speak(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            self.speak("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            print("Speech service unavailable.")
            self.speak("Sorry, speech service is unavailable.")
            return None

    def test_microphone(self):
        """Test microphone to check if audio input is recognized."""
        with sr.Microphone() as source:
            print("🎤 Testing microphone... (Speak into the mic)")
            self.speak("Please say something to test the microphone.")
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = self.recognizer.listen(source)
            
        try:
            command = self.recognizer.recognize_google(audio)
            print(f"🎧 Microphone Test - You said: {command}")
            self.speak(f"Microphone Test - You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Microphone Test: Sorry, I didn't catch that.")
            self.speak("Microphone Test: Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            print("Microphone Test: Speech service unavailable.")
            self.speak("Microphone Test: Sorry, speech service is unavailable.")
            return None
