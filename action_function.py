import webbrowser
import subprocess
import requests
from datetime import datetime
import wikipedia
import random
import re

site_urls = {
    "google": "https://google.com",
    "youtube": "https://youtube.com",
    "twitter": "https://twitter.com",
    "linkedin": "https://linkedin.com",
    "facebook": "https://facebook.com" ,
    "github": "https://github.com",
}

def open_website_if_command(command):
    command_lower = command.lower()
    for site, url in site_urls.items():
        if f"open {site}" in command_lower or command_lower.strip() == site:
            return site, url
    return None, None

def open_spotify():
    subprocess.call(["open", "-a", "Spotify"])

def get_weather(city):
    api_key = "api_key"  
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    try:
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            return f"Sorry, I couldn't find weather for '{city}'."

        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        wind = data["current"]["wind_kph"]
        return f"The weather in {city.title()} is {condition}, {temp}°C, with wind speed of {wind} kph."
    except Exception as e:
        print("[ERROR in get_weather]", e)
        return "Sorry, I couldn't fetch the weather right now."

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError:
        return "Your query is too broad. Try something more specific."
    except wikipedia.exceptions.PageError:
        return "Sorry, I could not find anything on that topic."
    except Exception:
        return "Something went wrong while fetching the result."

def fetch_joke():
    try:
        res = requests.get("https://v2.jokeapi.dev/joke/Any?type=single")
        joke = res.json().get("joke")
        return joke
    except Exception:
        return "Sorry, I couldn't fetch a joke right now."

import requests
from speech import speak  
API_KEY = "9177de90b115d557de48231a1daf6e28"  
BASE_URL = f"https://gnews.io/api/v4/top-headlines?lang=en&token={API_KEY}"

def fetch_news(query):
    try:
        response = requests.get(BASE_URL)
        data = response.json()
        if "articles" not in data:
            speak["Sorry, couldn't fetch the news at the moment."]
        
        headlines = []
        for article in data["articles"][:5]:
            headlines.append(article["title"])
        return headlines
    except Exception as e:
        speak[f"Failed to fetch news: {e}"]
    
    import re
from reminder_func import schedule_reminder
from speech import speak , listen

def handle_reminder_command():
   
    # Step 1: Ask for the task
    speak("What should I remind you about?")
    task = listen().lower().strip()

    if not task:
        speak("I didn't catch that. Please try again later.")
        return

    # Step 2: Ask for the time
    speak("When should I remind you?")
    time_response = listen().lower().strip()

    if not time_response:
        speak("I didn't hear the time. Please try again later.")
        return

    # Extract time info
    time_match = re.search(
        r"(in \d+ (seconds?|minutes?|hours?)|after \d+ (seconds?|minutes?|hours?)|"
        r"at \d{1,2}(:\d{2})? ?(am|pm)?|tomorrow|next \w+|on \w+ \d+)",
        time_response,
    )

    if not time_match:
        speak("Sorry, I couldn't understand the time. Try saying like 'after 5 minutes' or 'at 6 pm'.")
        return

    time_str = time_match.group(0)

    # Step 3: Schedule
    success = schedule_reminder(time_str, task)
    if success:
        speak(f"Okay, I’ll remind you to {task} {time_str}.")
    else:
        speak("Something went wrong. I couldn't set the reminder.")
