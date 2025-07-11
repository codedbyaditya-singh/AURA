import pyttsx3
import speech_recognition as sr
import string

# for text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen(timeout=6, phrase_time_limit=5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        return r.recognize_google(audio)

def clean_command(command):
    command = command.lower().strip()
    return command.translate(str.maketrans('', '', string.punctuation))
