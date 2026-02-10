import sys
import os
import json
import threading
import time
import ollama

# Add Project Root to Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config

class MemoryManager:
    def __init__(self):
        self.short_term = []
        self.lock = threading.Lock()
        self.last_interaction = time.time()
        self.memory_file = os.path.join(config.PROJECT_ROOT, "memory.json")
        
        # Initialize Memory File if missing
        if not os.path.exists(self.memory_file):
            self._save_memory({
                "profile": {}, 
                "preferences": {}, 
                "interests": [], 
                "projects": []
            })

    def _load_memory(self):
        """Reads the JSON memory file."""
        try:
            with open(self.memory_file, "r") as f:
                return json.load(f)
        except:
            return {}

    def _save_memory(self, data):
        """Overwrites the JSON memory file."""
        with open(self.memory_file, "w") as f:
            json.dump(data, f, indent=2)

    def update_interaction(self):
        self.last_interaction = time.time()

    def add_turn(self, role, content):
        with self.lock:
            self.short_term.append({'role': role, 'content': content})
            if len(self.short_term) > 10: self.short_term.pop(0)

    def get_context(self):
        """Injects JSON memory as a string into the System Prompt."""
        data = self._load_memory()
        # Convert JSON to a readable string for the LLM
        memory_str = json.dumps(data, indent=2)
        
        sys_prompt = (
            f"SYSTEM: You are Jarvis. Here is what you know about the user:\n{memory_str}\n"
            "Use this information to personalize answers. Keep responses concise."
        )
        with self.lock:
            return [{'role': 'system', 'content': sys_prompt}] + self.short_term

    def start_dreaming(self):
        threading.Thread(target=self._dream_loop, daemon=True).start()

    def _dream_loop(self):
        print("💤 Dream Protocol Active (JSON Mode)")
        while True:
            time.sleep(60)
            if time.time() - self.last_interaction > config.IDLE_TIMEOUT:
                if len(self.short_term) > 0:
                    print("\n💤 Jarvis is dreaming (Consolidating Memory)...")
                    self._consolidate_memory()

    def _consolidate_memory(self):
        # 1. Get current state
        current_memory = self._load_memory()
        
        with self.lock:
            chat_log = "\n".join([f"{m['role']}: {m['content']}" for m in self.short_term])
            self.short_term = [] # Wipe RAM

        # 2. The "Librarian" Prompt
        # We ask the LLM to act as a JSON merger
        prompt = f"""
        You are a Database Manager. 
        Task: Update the User Profile JSON based on the recent chat.
        
        Rules:
        1. Merge new facts into the existing JSON.
        2. DEDUPLICATE lists (e.g. if "Python" exists, don't add it again).
        3. Update fields if they changed (e.g. Age 22 -> 23).
        4. Return ONLY valid JSON. No markdown formatting.
        
        EXISTING JSON:
        {json.dumps(current_memory)}
        
        RECENT CHAT:
        {chat_log}
        """

        try:
            # 3. Generate the Update
            response = ollama.chat(
                model=config.BRAIN_DREAMER, 
                messages=[{'role': 'user', 'content': prompt}]
            )
            raw_json = response['message']['content']
            
            # 4. Clean the output (LLMs sometimes wrap in ```json ... ```)
            if "```" in raw_json:
                raw_json = raw_json.split("```json")[-1].split("```")[0].strip()
            
            # 5. Save the new state
            new_data = json.loads(raw_json)
            self._save_memory(new_data)
            print("💾 Memory Updated & Deduplicated.")
            
        except json.JSONDecodeError:
            print("⚠️ Memory Error: LLM produced invalid JSON. Skipping update.")
        except Exception as e:
            print(f"⚠️ Memory Error: {e}")