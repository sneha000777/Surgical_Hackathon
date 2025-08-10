# core/speech_engine.py
import edge_tts
import asyncio
import speech_recognition as sr

class SpeechEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    async def speak(self, text):
        communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
        await communicate.save("response.mp3")
        import os
        os.system("start response.mp3")  # Use 'afplay' on Mac or 'mpg123' on Linux

    def listen(self):
        with sr.Microphone() as source:
            print("Listening for 'confirm'...")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.lower()
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"Error with Google Speech Recognition: {e}")
                return ""
