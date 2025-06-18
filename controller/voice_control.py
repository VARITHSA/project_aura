import os
import sys
import time
from io import BytesIO

import noisereduce as nr
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
        self.record_seconds = 5
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
        audio = audio / np.max(np.abs(audio))
        
        audio = nr.reduce_noise(y=audio, sr = self.sample_rate)

        return audio

    def transcribe(self, audio):
        try:
            # Convert to in-memory WAV
            audio_int16 = np.int16(audio * 32767)
            buffer = BytesIO()
            wavfile.write(buffer, self.sample_rate, audio_int16)
            buffer.seek(0)

            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=("audio.wav", buffer, "audio/wav"),
                response_format="verbose_json",
                language="en"
            )
            text = transcription.text.strip().lower()
            print(f"📝 Transcribed: {text}")
            return text
        except Exception as e:
            print("❌ Transcription failed:", e)
            return None
        
        
    def correct_with_gpt(self, raw_text):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a transcription corrector. Improve clarity and fix mistakes."},
                    {"role": "user", "content": f"The transcribed text is: {raw_text}"}
                ]
            )
            corrected = response.choices[0].message.content.strip()
            print(f"🧠 Corrected by GPT-4o: {corrected}")
            return corrected
        except Exception as e:
            print("⚠️ GPT-4o correction failed:", e)
            return raw_text
        
        
        
    def run(self):
        while self.running:
            audio = self.listen()
            if audio is None:
                continue
            
            raw_text = self.transcribe(audio)
            if raw_text:
                corrected_text = self.correct_with_gpt(raw_text)
                self.speak(f'you said:{corrected_text}')


# Run it
