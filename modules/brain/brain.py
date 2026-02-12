import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config

import ollama
# Make sure 'search' is imported
from skills import system, notes, search, youtube, music

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
                tools=config.TOOLS_SCHEMA
            )
            
            # Check for Tool Calls
            if response.message.tool_calls:
                for tool in response.message.tool_calls:
                    fn = tool.function.name
                    args = tool.function.arguments
                    print(f"⚙️ Calling: {fn} ({args})", flush=True)
                    
                    if fn == 'set_volume': return system.set_volume(args['level'])
                    elif fn == 'set_brightness': return system.set_brightness(args['level'])
                    elif fn == 'launch_app': return system.launch_app(args['app_name'])
                    elif fn == 'add_note': return notes.add_note(args['content'])
                    elif fn == 'summarize_video':
                        transcript = youtube.get_transcript(args['url'])
                        return self.chat(f"Summarize this: {transcript}")
                    
                    # --- SEARCH HANDLER ---
                    elif fn == 'search_web':
                        # 1. Execute Search
                        result = search.search_web(args['query'])
                        
                        # 2. Feed result back to Brain
                        return self.chat(f"SYSTEM: Using these search results, answer the user: {result}")
                    # ----------------------

                    elif fn == 'play_song':
                        # Execute the play function
                        result = music.play(args['query'])
                        # Tell the user what is playing
                        return self.chat(f"SYSTEM: The music has started. Tell the user: {result}")

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