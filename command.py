import time
import random
import webbrowser
from datetime import datetime
from intent_classifier import IntentClassifier
from speech import speak
from communication import send_whatsapp_message, load_contacts
import action_function   # the file where your functions are
from action_function import handle_reminder_command 
from history_saving import log_conversation


contacts = load_contacts('contact.json')

greeting_responses = [
    "I'm fine, nice to meet you!",
    "Feeling very technological today!",
    "I'm doing great — thanks for asking!",
    "All systems are running smoothly!",
    "I'm good! Ready to help you out."
]

bye_responses = [
    "Goodbye! Have a great day.",
    "See you later!",
    "Talk to you soon!",
    "Bye for now!",
    "Take care!"
]

classifier = IntentClassifier()

def process_command(command):
    intent = classifier.predict(command.lower())
    command_lower = command.lower()
    response = ""
    action_summary = ""  
    site, url = action_function.open_website_if_command(command_lower)
    if site:
        speak(f"Opening {site.capitalize()}")
        webbrowser.open(url)
        return True

    if intent == "intro":
        speak("My name is Aura, I am an AI voice assistant built by Aditya.")
        action_summary = response
        speak(response)
    elif intent == "greeting":
        action_summary ="Greeted the user"
        speak(random.choice(greeting_responses))
    elif "search for" in command_lower:
        query = command_lower.split("search for", 1)[1].strip()
        response = f"searching for {query}"
        action_summary = "Searched Google for '{query}'"
        speak(response)
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif any(command_lower.startswith(q) for q in ["who is", "what is", "where is", "tell me about", "define", "explain"]):
        responce = "Searching Wikkipidea"
        action_summary = f"Searched wikkipidea for '{command}' "
        speak("searchig in wikkipidea")
        answer = action_function.search_wikipedia(command)
        response = answer
        speak(answer)
    elif "open spotify" in command_lower:
        responce = "Openened spotify"
        action_summary =responce
        speak("Opening Spotify")
        action_function.open_spotify()
    elif intent == "tell_date":
        today = datetime.now().strftime("%B %d, %Y")
        action_summary = "Told the current date"
        speak(f"Today's date is {today}.")
    elif intent == "joke":
        joke = action_function.fetch_joke()
        action_summary = "Told the joke"
        speak(joke)
    elif intent == "play_song":
        song = command_lower.split("play", 1)[1].replace("song", "").strip()
        if song:
            action_summary = f"Played song '{song}' on youtube"
            speak(f"Playing {song} on YouTube")
            time.sleep(1.5)
            try:
                import pywhatkit
                pywhatkit.playonyt(song)
            except Exception:
                webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")
        else:
            action_summary = "User didn't specify a song to play / random song played"
            speak("Please tell me the song name after saying play.")
    elif intent == "weather":
        city = None
        for keyword in ["in", "at", "for"]:
            if keyword in command_lower:
                parts = command_lower.split(keyword)
                if len(parts) > 1:
                    city = parts[1].strip()
                    break
        if city:
            weather = action_function.get_weather(city)
            action_summary = f"Provided weather info for '{city}' "
            speak(weather)
        else:
            action_summary = "Asked user to specify city name to tell weather"
            speak("Please tell me the city name like 'weather in Delhi'.") 
    elif intent == "news":
     from news_fetcher import fetch_news
     headlines = fetch_news()
     if not headlines or "Failed" in headlines[0] or "Sorry" in headlines[0]:
        action_summary = "Failed to fetch news"
        speak("Sorry, I couldn't fetch the news right now.")
        print("News fetch issue:", headlines)
     else:
        action_summary = "provided top news headlines from Gnews API"
        speak("Here are the top news headlines for today.")
        for headline in headlines:
            # print("News headline:", headline)
            speak(headline)
    elif intent == "set_reminder":
        status = handle_reminder_command()
        if status == "done":
         action_summary = f"Reminder set: {command}"
         log_conversation(command, action_summary)
        return True
    elif intent == "send_message":
        send_whatsapp_message(command, contacts)
        responce ="Sent a WhatsApp message"
        action_summary = f"Sent WhatsApp message '{command}' "
    elif intent == "bye":
        speak(random.choice(bye_responses))
        return False
    else:
        speak("You said: " + command)
    # Log user command and action summary, except for intents that already logged and returned
    if intent not in ["set_reminder", "bye"]:
       log_conversation(command, action_summary)
    return True
