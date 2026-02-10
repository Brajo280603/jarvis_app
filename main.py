# main.py
import queue
import time
import sys
import config

# 1. Cleaner Imports (Thanks to __init__.py)
from modules import Ears, Mouth, Brain, MemoryManager 

def main():
    # 2. Initialization
    print("⏳ Initializing Jarvis...")
    cmd_queue = queue.Queue()
    
    # Initialize Modules
    ears = Ears(cmd_queue)
    mouth = Mouth()
    mem = MemoryManager()

    brain = Brain(mem)
    
    # 3. Start Background Threads
    ears.start()        # Starts Mic + Whisper
    mem.start_dreaming() # Starts Dream Protocol
    
    print("\n🚀 JARVIS 3.0 ONLINE")
    print(f"   [Brain]: {config.BRAIN_CHAT} | [Router]: {config.BRAIN_ROUTER}")
    
    # 4. Main Event Loop
    while True:
        try:
            # Wait for text from Ears
            text = cmd_queue.get()
            
            # --- UPDATED SHUTDOWN LOGIC ---
            exit_phrases = ["shut down", "power off", "goodbye", "good bye", "bye jarvis"]
            
            if any(phrase in text.lower() for phrase in exit_phrases):
                mouth.say("Goodbye, sir. Systems offline.")
                # Give it 2 seconds to finish speaking before killing the process
                time.sleep(3) 
                break
            # ------------------------------
            
            # Acknowledge
            # mouth.play_ping()
            
            # Think (Brain uses Router + Chat)
            # Note: We pass 'mem' so the Brain can read/write memory
            response = brain.think(text)
            
            # Speak
            if response:
                mouth.say(response)
                
        except KeyboardInterrupt:
            print("\n👋 Force Quit.")
            break
        except Exception as e:
            print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    main()