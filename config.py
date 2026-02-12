import os

# --- HARDWARE ---
MIC_INDEX = 4         # Check 'python -m speech_recognition' to confirm
CPU_THREADS = 4       # Optimization for Ryzen 3500U

# --- MODELS ---
EARS_MODEL = "base.en"       
BRAIN_ROUTER = "functiongemma" # The 270M Router (Reflexes)
# BRAIN_CHAT = "gemma3:1b"       # The 1B Speaker (Intellect)
BRAIN_CHAT = "gemini-3-flash-preview:cloud"       # The 1B Speaker (Intellect)
# BRAIN_DREAMER = "gemma3:1b"    # The Dreamer (Memory Sorting)
BRAIN_DREAMER = "gemini-3-flash-preview:cloud"    # The Dreamer (Memory Sorting)

# --- PATHS ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PIPER_PATH = os.path.join(PROJECT_ROOT, "modules/mouth/piper/piper")
VOICE_MODEL = os.path.join(PROJECT_ROOT, "modules/mouth/en_US-libritts_r-medium.onnx")
PING_SOUND = os.path.join(PROJECT_ROOT, "modules/mouth/pop.wav")
MEMORY_FILE = os.path.join(PROJECT_ROOT, "memory.md")
NOTES_DIR = os.path.expanduser("~/Documents/Jarvis_Notes")

# --- TUNING ---
ENERGY_THRESHOLD = 2500
PAUSE_THRESHOLD = 1.8 # Snappy response
# IDLE_TIMEOUT = 300    # 5 Minutes before dreaming
IDLE_TIMEOUT = 10    # 5 Minutes before dreaming
