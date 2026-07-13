## 🌟 Aura: Your Personal Voice Assistant

Aura is a lightweight, Python-based voice assistant that listens, understands, and responds to your commands in real time.
It features wake-word activation, natural language understanding, and multi-functional commands — all packed into a modular design.

## 🚀 Features
🔊 Wake Word Detection
Powered by Picovoice Porcupine for hotword activation ("Hey Aura").
🗣 Speech Recognition
Converts your spoken words into text using SpeechRecognition.
💬 Natural Commands
Supports flexible phrasing and intent detection.
🎶 Entertainment
Play music/videos directly from YouTube.
🌤 Utilities
Get real-time weather updates.
Set and persist reminders (stored in schedules.json).
Get headlines updates.
Open websites and applications.
send wattsapp text messages.
🤖 Personality
Greets, introduces itself, tells jokes, and answers queries.
🗣 Text-to-Speech
Voice responses via TTS (bug fixed to handle multiple responses).

## 🛠️ Tech Stack
Language: Python 3
Libraries/Tools:
speechrecognition – speech-to-text
pyttsx3 – text-to-speech
pvporcupine – wake word detection
pyaudio – audio input/output
pywhatkit, requests – YouTube, weather, and other utilities
JSON – persistent reminders

## How to Run (for developers)
```bash
git clone https://github.com/adityasingh/aura-assistant.git
cd aura-assistant
pip install -r requirements.txt
python main.py
