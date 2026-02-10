import os
import datetime
import config

def add_note(content):
    if not os.path.exists(config.NOTES_DIR):
        os.makedirs(config.NOTES_DIR)
    
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filepath = os.path.join(config.NOTES_DIR, f"{date_str}.md")
    time_str = datetime.datetime.now().strftime("%H:%M")
    
    entry = f"\n- **{time_str}**: {content}"
    
    with open(filepath, "a") as f:
        f.write(entry)
    return "Note saved."