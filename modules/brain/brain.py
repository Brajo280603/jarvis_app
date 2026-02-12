import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config

import ollama
# Import the Registry instead of individual skills
from skills import registry 

class Brain:
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.router_model = config.BRAIN_ROUTER
        self.chat_model = config.BRAIN_CHAT

    def think(self, text):
        self.memory.update_interaction()
        
        # 1. ROUTER (Reflexes)
        try:
            response = ollama.chat(
                model=self.router_model,
                messages=[{'role': 'user', 'content': text}],
                # Pass schema from Registry
                tools=registry.TOOLS_SCHEMA
            )
            
            # Check for Tool Calls
            if response.message.tool_calls:
                for tool in response.message.tool_calls:
                    fn_name = tool.function.name
                    args = tool.function.arguments
                    print(f"⚙️ Calling: {fn_name} ({args})", flush=True)
                    
                    # --- DYNAMIC DISPATCH LOGIC ---
                    if fn_name in registry.TOOLS_MAP:
                        # 1. Get the function object
                        func = registry.TOOLS_MAP[fn_name]
                        
                        # 2. Run it (unpack args automatically)
                        result = func(**args)
                        
                        # 3. Handle specific return types
                        # (YouTube and Search need their output summarized by the Chat Brain)
                        if fn_name in ['summarize_video', 'search_web']:
                            return self.chat(f"SYSTEM: Using this data, answer the user: {result}")
                        
                        # (Music is a fire-and-forget action, just tell the user)
                        elif fn_name == 'play_song':
                            return self.chat(f"SYSTEM: Music started. Tell user: {result}")
                            
                        # (System commands just return a status string)
                        else:
                            return str(result)
                    
                    else:
                        print(f"❌ Error: Tool '{fn_name}' not found in registry.")

        except Exception as e: 
            print(f"Router Error: {e}", flush=True)

        # 2. SPEAKER (Chat)
        return self.chat(text)

    def chat(self, text):
        self.memory.add_turn('user', text)
        res = ollama.chat(model=self.chat_model, messages=self.memory.get_context())
        reply = res['message']['content']
        self.memory.add_turn('assistant', reply)
        return reply