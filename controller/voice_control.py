import os
import sys
import time
from io import BytesIO

import numpy as np
import openai
import pyttsx3
import sounddevice as sd
from dotenv import load_dotenv
from openai import OpenAI
from scipy.io import wavfile


class VoiceHandler:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if not self.client.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        
        
        # TTS engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 200)
        self.engine.setProperty('volume', 1.0)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

        # Audio settings
        self.sample_rate = 16000
        self.record_seconds = 3
        self.quit_words = ["exit", "quit", "stop"]
        self.running = True
        self.threshold = 0.01  # basic silence threshold

    def model_speak_init(self):
        self.speak("Hey! I am AURA, your personal assistant. How can I help you today?")

    def speak(self, text):
        if not text:
            return
        print(f"AURA says: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        print("🎙️ AURA is listening...")
        self.speak("AURA is listening...")
        audio_data = sd.rec(int(self.sample_rate * self.record_seconds),
                            samplerate=self.sample_rate, channels=1, dtype='float32')
        sd.wait()

        # Flatten and trim silence
        audio = np.squeeze(audio_data)
        energy = np.abs(audio)
        if np.max(energy) < self.threshold:
            print("⚠️ No speech detected (too silent).")
            return None

        return audio

    def transcribe(self, audio):
        try:
            # Convert to in-memory WAV
            audio_int16 = np.int16(audio * 32767)
            buffer = BytesIO()
            wavfile.write(buffer, 16000, audio_int16)
            buffer.seek(0)

            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=("audio.wav", buffer, "audio/wav"),
                response_format="text",
                language="en"
            )
            text = transcription.strip().lower()
            print(f"📝 Transcribed: {text}")
            return text
        except Exception as e:
            print("❌ Transcription failed:", e)
            return None

    def run(self):
        self.model_speak_init()
        while self.running:
            audio = self.listen()
            text = self.transcribe(audio)
            if text:
                self.speak(f"You said: {text}")


# Run it
if __name__ == "__main__":
    aura = VoiceHandler()
    aura.run()
