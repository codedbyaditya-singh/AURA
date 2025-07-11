from speech import speak, listen
from command import process_command

speak("Hello Aditya I'm AURA, how can I help you")

while True:
    try:
        command = listen()
        if "hello aura" in command.lower():
            speak("I am listening...")
            command = listen()

        if not process_command(command):
            break

    except Exception as e:
        speak("Sorry, something went wrong.")
        print("⚠️ Error:", e)
