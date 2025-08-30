from datetime import datetime

LOG_FILE = "conversation_log.txt"

def log_conversation(user_intent: str, action_performed: str):
    today_str = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%H:%M:%S")

    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    date_header = f"=== Date: {today_str} ===\n"
    if date_header not in lines:
        if lines and not lines[-1].endswith("\n\n"):
            lines.append("\n")
        lines.append(date_header)
        lines.append(f"{'Time':<10} | {'User Intent':<30} | {'Action Performed'}\n")
        lines.append("-" * 70 + "\n")
    entry_line = f"{timestamp:<10} | {user_intent:<30} | {action_performed}\n"
    lines.append(entry_line)

    with open(LOG_FILE, "w") as f:
        f.writelines(lines)
