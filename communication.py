import pywhatkit
from datetime import datetime, timedelta
from speech import speak, listen
import json

# Load contacts from JSON file
def load_contacts(filename='contact.json'):
    try:
        with open(filename, 'r') as f:
            contacts = json.load(f)
        return contacts
    except FileNotFoundError:
        print("Contact file not found!")
        return {}

# Extract contact name from user command
def extract_contact_name(command):
    words = command.lower().split()
    if "to" in words:
        to_index = words.index("to")
        if to_index + 1 < len(words):
            return words[to_index + 1]
    return None

# Send WhatsApp message using pywhatkit
def send_whatsapp_message(command, contacts):
    contact_name = extract_contact_name(command)
    if not contact_name or contact_name not in contacts:
        speak("Sorry, I don't have the phone number for that contact.")
        return

    speak(f"What message would you like to send to {contact_name}?")
    message = listen()

    number = contacts[contact_name]
    now = datetime.now() + timedelta(minutes=1)
    hour = now.hour
    minute = now.minute

    speak(f"Sending your message to {contact_name} on WhatsApp.")
    pywhatkit.sendwhatmsg(number, message, hour, minute)

# Example usage
if __name__ == "__main__":
    contacts = load_contacts()
    command = "send message to aman"  # Example command; in real use, get from speech input
    send_whatsapp_message(command, contacts)
# watts app message sending 
# import pywhatkit as kit
# import datetime

# def send_whatsapp_message(contact_name, message, contacts):
#     if contact_name not in contacts:
#         return f"Contact '{contact_name}' not found in contact list."
#     phone_number = contacts[contact_name]
#     try:
#         kit.sendwhatmsg_instantly(
#             phone_no=phone_number,
#             message=message,
#             wait_time=10,   # seconds before sending
#             tab_close=True,
#             close_time=5
#         )
#         return f"Message sent to {contact_name}: {message}"
#     except Exception as e:
#         return f"Failed to send message: {str(e)}"
