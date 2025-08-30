import json
import threading
from datetime import datetime
import dateparser
import logging
from speech import speak

logging.basicConfig(level=logging.DEBUG)

REMINDER_FILE = "schedules.json"

def load_schedules():
    try:
        with open(REMINDER_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_schedules(schedules):
    with open(REMINDER_FILE, 'w') as file:
        json.dump(schedules, file, indent=4)

def trigger_reminder(task):
    logging.info(f"Triggering reminder: {task}")
    speak(f"Reminder! {task}")
    # Remove triggered reminder from schedules file
    schedules = load_schedules()
    updated = [entry for entry in schedules if entry["task"] != task]
    save_schedules(updated)

def schedule_reminder(time_str, task):
    reminder_time = dateparser.parse(time_str)
    if reminder_time is None:
        speak("I couldn't understand the time. Please try again.")
        return False

    now = datetime.now()
    delay = (reminder_time - now).total_seconds()

    if delay <= 0:
        speak("The time you provided is already past.")
        return False

    # Save the reminder
    schedules = load_schedules()
    schedules.append({"time": reminder_time.strftime('%Y-%m-%d %H:%M:%S'), "task": task})
    save_schedules(schedules)

    # Schedule it with threading.Timer
    timer = threading.Timer(delay, trigger_reminder, args=[task])
    timer.daemon = True
    timer.start()

    speak(f"Okay, I will remind you to {task} at {reminder_time.strftime('%I:%M %p')}.")
    return True

def schedule_saved_reminders():
    schedules = load_schedules()
    now = datetime.now()

    for entry in schedules:
        try:
            reminder_time = datetime.strptime(entry["time"], '%Y-%m-%d %H:%M:%S')
            task = entry["task"]
            delay = (reminder_time - now).total_seconds()

            if delay > 0:
                timer = threading.Timer(delay, trigger_reminder, args=[task])
                timer.daemon = True
                timer.start()
                logging.info(f"Scheduled saved reminder: {task} at {reminder_time}")
        except Exception as e:
            logging.error(f"Error scheduling saved reminder: {entry} -> {e}")
