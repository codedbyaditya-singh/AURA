import webbrowser
import time
import subprocess
import requests
from datetime import datetime
from geopy.geocoders import Nominatim
from speech import speak

try:
    import pywhatkit
    pywhatkit_available = True
except ImportError:
    pywhatkit_available = False

def open_spotify():
    subprocess.call(["open", "-a", "Spotify"])

def get_weather(city):
    try:
        geolocator = Nominatim(user_agent="aura_weather")
        location = geolocator.geocode(city)

        if not location:
            return f"Sorry, I couldn't find the city '{city}'."

        lat, lon = location.latitude, location.longitude
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

        response = requests.get(url)
        data = response.json()
        weather = data["current_weather"]
        temp = weather["temperature"]
        wind = weather["windspeed"]
        return f"The current temperature in {city} is {temp} degrees Celsius with wind speed of {wind} km/h."
    except:
        return "Sorry, I couldn't fetch the weather right now."


def process_command(command):
    command = command.lower()

    if "what's your name" in command or "introduce yourself" in command:
        speak("My name is Aura, I am an AI voice assistant built by Aditya.")

    elif "how are you?" in command or "you feeling" in command:
        speak("I am fine, nice to meet you. Feeling very technological.")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open twitter" in command:
        speak("Opening Twitter")
        webbrowser.open("https://twitter.com")

    elif "open spotify" in command:
        speak("Opening Spotify")
        open_spotify()

    elif "date" in command:
        today = datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}.")

    elif "joke" in command:
        res = requests.get("https://v2.jokeapi.dev/joke/Any?type=single")
        joke = res.json().get("joke")
        speak(joke)

    elif "play" in command or "in youtube" in command:
        song = command.split("play", 1)[1].replace("song", "").strip()
        if song:
            speak(f"Playing {song} on YouTube")
            time.sleep(1.5)
            if pywhatkit_available:
                try:
                    pywhatkit.playonyt(song)
                except:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")
            else:
                webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")
        else:
            speak("Please tell me the song name after saying play.")

    elif "search for" in command:
        query = command.split("search for", 1)[1]
        speak(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        
    
    elif "weather in" in command or "weather" in command:
        city = command.split("weather in", 1)[1].strip()
        weather_report = get_weather(city)
        print(weather_report)
        speak(weather_report)

    elif "goodbye" in command or "ok for now" in command:
        speak("Goodbye...")
        return False

    else:
        speak("You said: " + command)

    return True
