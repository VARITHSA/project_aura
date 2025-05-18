import pyttsx3
import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import os
import time


class VoiceHandler:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.model = whisper.load_model("base")
        
    def speak(self, text): 
        ''' convert text ---> speech'''
        self.engine.say(text)
        self.engine.runAndWait()
        
    def record_audio(self, filename="input.wav", duration=5, fs=16000):
        """Record audio from the microphone and save it as a WAV file."""
        print("🎤 Listening... (Speak clearly)")
        self.speak("What do you want to search?")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished
        write(filename, fs, recording)
        print("✅ Recording saved as", filename)
        
    def listen(self):
        """Record and transcribe audio using Whisper."""
        self.record_audio()
        print("🧠 Transcribing using Whisper...")
        result = self.model.transcribe("input.wav")
        command = result["text"].strip()
        if command:
            print(f"🎧 You said: {command}")
            self.speak(f"You said: {command}")
            return command
        else:
            print("😕 Didn't catch that.")
            self.speak("Sorry, I didn't catch that.")
            return None
    
    
    def test_microphone(self):
        """Test microphone with Whisper transcription."""
        self.speak("Testing microphone. Please say something.")
        self.record_audio("mic_test.wav")
        print("🧠 Transcribing microphone test...")
        result = self.model.transcribe("mic_test.wav")
        command = result["text"].strip()
        if command:
            print(f"🎧 Microphone Test - You said: {command}")
            self.speak(f"Microphone Test - You said: {command}")
            return command
        else:
            print("😕 Microphone Test: Didn't catch that.")
            self.speak("Microphone Test: Sorry, I didn't catch that.")
            return None
    
    