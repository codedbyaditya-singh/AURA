import struct
import pyaudio
import pvporcupine
import time
from speech import speak, listen
from command import process_command
import logging
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
ACCESS_KEY = "UouZt6E2Y1tBY9WAVRFJkb4CkEXPBLf3/ryoeWWJx2EZyopL11RybA=="
WAKEWORD_PATH = "wakeword/HEY-AURA_en_mac_v3_0_0-2/HEY-AURA_en_mac_v3_0_0.ppn"
def listen_for_wakeword():
    speak("Hello Aditya, I'm AURA. Say 'Hey Aura' to wake me up.")

    while True:  
        try:
            # Initialize Porcupine & mic
            porcupine = pvporcupine.create(
                access_key=ACCESS_KEY,
                keyword_paths=[WAKEWORD_PATH]
            )

            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length
            )

            wake_word_detected = False

            while True:
                try:
                    pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                    result = porcupine.process(pcm)
                    if result >= 0:  # Wake word detected
                        speak("I am listening...")
                        time.sleep(0.5)
                        wake_word_detected = True
                        break  # exit wake-word loop
                except Exception as e:
                    print("⚠️ Wake word loop error:", e)

        except KeyboardInterrupt:
            print("\nStopping assistant...")
            break
 
        finally:
            audio_stream.stop_stream()
            audio_stream.close()
            pa.terminate()
            porcupine.delete()
            time.sleep(0.3)  
        if wake_word_detected:
            handle_command()

def handle_command():
    """Listens for and processes a voice command after wake word."""
    try:
        command = listen(timeout=6, phrase_time_limit=8)
        if not command:
            speak("I didn’t catch that. Please try again.")
            return
        command_lower = command.lower().strip()
        if command_lower.startswith("hey aura"):
            command_lower = command_lower.replace("hey aura", "", 1).strip()
        if command_lower:
            process_command(command_lower)
    except Exception as e:
        speak("Sorry, something went wrong.")
        print("⚠️ Command handling error:", e)
if __name__ == "__main__":
    listen_for_wakeword()
