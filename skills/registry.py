from skills import system, notes, youtube, search, music

# 1. The Mapping (Name -> Function)
# This is how the Brain knows which Python function to run.
TOOLS_MAP = {
    'set_volume': system.set_volume,
    'set_brightness': system.set_brightness,
    'launch_app': system.launch_app,
    'add_note': notes.add_note,
    'summarize_video': youtube.get_transcript, # Note: We map get_transcript directly
    'search_web': search.search_web,
    'play_song': music.play,
    'pause_music': music.pause,
    'resume_music': music.pause,  
    'stop_music': music.stop,
}

# 2. The Definition (Schema for Ollama)
# This tells the LLM *how* to use the tools.
TOOLS_SCHEMA = [
    {
        'type': 'function',
        'function': {
            'name': 'set_volume',
            'description': 'Set volume percentage',
            'parameters': {'type': 'object', 'properties': {'level': {'type': 'integer'}}, 'required': ['level']}
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'set_brightness',
            'description': 'Set screen brightness percentage',
            'parameters': {'type': 'object', 'properties': {'level': {'type': 'integer'}}, 'required': ['level']}
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'launch_app',
            'description': 'Launch an app',
            'parameters': {'type': 'object', 'properties': {'app_name': {'type': 'string'}}, 'required': ['app_name']}
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'add_note',
            'description': 'Save a note',
            'parameters': {'type': 'object', 'properties': {'content': {'type': 'string'}}, 'required': ['content']}
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'summarize_video',
            'description': 'Summarize YouTube video',
            'parameters': {'type': 'object', 'properties': {'url': {'type': 'string'}}, 'required': ['url']}
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'search_web',
            'description': 'Search the internet for current events',
            'parameters': {'type': 'object', 'properties': {'query': {'type': 'string'}}, 'required': ['query']}
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'play_song',
            'description': 'Play a song on Youtube Music',
            'parameters': {'type': 'object', 'properties': {'query': {'type': 'string'}}, 'required': ['query']}
        }
    },
    # --- NEW PAUSE TOOL ---
    {
        'type': 'function',
        'function': {
            'name': 'pause_music',
            'description': 'Pause the currently playing music',
            'parameters': {'type': 'object', 'properties': {}, 'required': []} # No args needed
        }
    },
    # --- NEW RESUME TOOL ---
    {
        'type': 'function',
        'function': {
            'name': 'resume_music',
            'description': 'Resume the currently playing music',
            'parameters': {'type': 'object', 'properties': {}, 'required': []} # No args needed
        }
    },
    
    # --- NEW STOP TOOL ---
    {
        'type': 'function',
        'function': {
            'name': 'stop_music',
            'description': 'Stop the music player',
            'parameters': {'type': 'object', 'properties': {}, 'required': []} # No args needed
        }
    }
]