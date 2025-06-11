import os
import queue
import sys
import threading
import time

import numpy as np
import pyttsx3
import sounddevice as sd
from faster_whisper import WhisperModel
from scipy.io import wavfile


class VoiceHandler:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.model = WhisperModel("base", device="cuda", compute_type="float16")
        self.engine.setProperty('rate', 200)  
        self.sample_rate = 16000
        self.record_seconds = 5
        self.quit_words = ["exit", "quit", "stop"]
        self.running = True
    
    
    
    def transcribe(self,audio):
        """function to transcribe the audio using Whisper model"""
        try:
            segments, _ = self.model.transcribe(audio, language="en", beam_size=1, vad_filter = True)
            text = " ".join([segment.text for segment in segments]).lower().strip()
            
            if not text:
                print("No speech detected.")
                return None
            print(f"Transcribed text: {text}")
            if any(word in text for word in self.quit_words):
                print("Exiting AURA...")
                self.engine.say("Exiting AURA...")
                print("Goodbye!")
                self.engine.say("Goodbye!")
                self.engine.runAndWait()
                sys.exit()
                return None
            return text
        except Exception as e:
            print(f"Error in transcription: {e}")
            return None
        
    def model_speak_init(self):
        """function to speak AURA initialization"""
        self.engine.say("Hey! I am AURA, your personal assistant. How can I help you today?")
        self.engine.runAndWait()
        
    
    def listen(self):
        """function to listen to the user's voice """
        self.engine.say("AURA is listening...")
        self.engine.runAndWait()
        print("Listening...")
        audio_data = sd.rec(int(self.sample_rate * self.record_seconds),samplerate=self.sample_rate, channels=1, dtype='float32')    
        sd.wait()  # Wait until recording is finished
        audio_data = audio_data.flatten()   
        audio = np.squeeze(audio_data)
        return audio
    
    def speak(self, text):
        """function to speak the text using pyttsx3"""
        if not text:
            print("No text to speak.")
            return
        self.engine.say(text)
        self.engine.runAndWait()
        print(f"AURA says: {text}")