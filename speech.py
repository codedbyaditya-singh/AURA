
import pyttsx3
import speech_recognition as sr
import string
import time
import re

# --- Text-to-Speech ---
def speak(text):
    """Speak text safely on macOS using fresh pyttsx3 instance each time."""
    print(f"aura sys : {text}")
    try:
        # Break long sentences into chunks to avoid cutting mid-way
        chunks = [c.strip() for c in re.split(r'(?<=[.!?])\s+', text) if c.strip()]
        if not chunks:
            chunks = [text]

        for chunk in chunks:
            engine = pyttsx3.init(driverName='nsss')  # macOS voice engine
            engine.setProperty('rate', 160)  # speech speed
            engine.say(chunk)
            engine.runAndWait()
            engine.stop()  # release audio device
            time.sleep(0.1)  # prevents overlapping with next speech
    except Exception as e:
        print(f"[TTS Error] {e}")
        def listen(timeout=6, phrase_time_limit=5):

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = r.recognize_google(audio)
            print(f"✅ Recognized: {text}")
            return text
        except sr.WaitTimeoutError:
            print("⏳ Listening timed out (no speech detected).")
            return ""
        except sr.UnknownValueError:
            print("🤔 Could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"⚠️ Could not request results from Google Speech Recognition service; {e}")
            return ""

# --- Command Cleaner ---
def clean_command(command):
    """Lowercase, strip punctuation, and clean user command."""
    command = command.lower().strip()
    return command.translate(str.maketrans('', '', string.punctuation))
