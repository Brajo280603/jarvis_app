import sys
import os
import re  # <--- NEW IMPORT
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config

import subprocess
import shlex
import queue
import threading

class Mouth:
    def __init__(self):
        self.queue = queue.Queue()
        self.stop_flag = False
        threading.Thread(target=self._worker, daemon=True).start()

    def play_ping(self):
        if os.path.exists(config.PING_SOUND):
            subprocess.Popen(["aplay", "-q", config.PING_SOUND], stderr=subprocess.DEVNULL)

    def say(self, text):
        self.queue.put(text)

    def _worker(self):
        while not self.stop_flag:
            try:
                text = self.queue.get(timeout=1)
                
                # 1. Print formatted text (Keep the bold/stars for your eyes)
                print(f"\n🤖 Jarvis: {text}")
                
                # 2. Clean text for ears (Remove *, _, ` and #)
                spoken_text = re.sub(r'[*_`#]', '', text) 
                safe_text = shlex.quote(spoken_text)
                
                # 3. Speak the clean version
                cmd = (
                    f'echo {safe_text} | '
                    f'{config.PIPER_PATH} --model {config.VOICE_MODEL} --output-raw | '
                    f'aplay -r 22050 -f S16_LE -t raw -q'
                )
                subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL)
                
                # 4. Restore listening prompt
                print("🔴 Listening...", end="", flush=True)
                
                self.queue.task_done()
            except queue.Empty:
                continue