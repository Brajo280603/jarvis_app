import sys
import os
# Add Project Root to Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config

import speech_recognition as sr
from faster_whisper import WhisperModel
import time
import queue
import threading
from ctypes import *
from contextlib import contextmanager

# --- THE CTYPES SILENCER (The "Silver Bullet") ---
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass # Do nothing, effectively silencing the error

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def no_alsa_err():
    try:
        asound = cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(c_error_handler)
        yield
        asound.snd_lib_error_set_handler(None)
    except:
        yield
# ------------------------------------------------

class Ears:
    def __init__(self, output_queue):
        self.output_queue = output_queue
        self.audio_queue = queue.Queue()
        self.stop_flag = False
        
        print(f"⏳ Loading Ears ({config.EARS_MODEL})...")
        try:
            self.model = WhisperModel(config.EARS_MODEL, device="auto", compute_type="int8", cpu_threads=config.CPU_THREADS)
        except:
            self.model = WhisperModel(config.EARS_MODEL, device="cpu", compute_type="int8", cpu_threads=config.CPU_THREADS)

        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = config.ENERGY_THRESHOLD
        self.recognizer.pause_threshold = config.PAUSE_THRESHOLD
        self.recognizer.dynamic_energy_threshold = False
        
        # We wrap the Microphone initialization with the silencer
        print("🎤 Initializing Microphone...")
        with no_alsa_err():
            self.mic = sr.Microphone(device_index=config.MIC_INDEX, sample_rate=44100)

    def start(self):
        threading.Thread(target=self._listen_worker, daemon=True).start()
        threading.Thread(target=self._transcribe_worker, daemon=True).start()
        print("✅ Ears Active")

    def _listen_worker(self):
        print("🔴 Listening...", end="", flush=True)
        with self.mic as source:
            while not self.stop_flag:
                try:
                    # We also silence the 'listen' loop just in case
                    with no_alsa_err():
                        audio = self.recognizer.listen(source, timeout=None)
                    self.audio_queue.put(audio)
                    print("\r⏳ Processing...", end="", flush=True)
                except: continue

    def _transcribe_worker(self):
        while not self.stop_flag:
            try:
                audio = self.audio_queue.get(timeout=1)
            except queue.Empty: continue

            temp_wav = f"temp_{int(time.time())}.wav"
            try:
                with open(temp_wav, "wb") as f: f.write(audio.get_wav_data())
                
                segments, _ = self.model.transcribe(
                    temp_wav, beam_size=1, language="en", vad_filter=False
                )
                text = " ".join([s.text for s in segments]).strip()
                
                if len(text) > 2:
                    # Print the User text cleanly
                    print(f"\r👤 You: {text}")
                    self.output_queue.put(text)
                    # We DO NOT print "Listening..." here anymore.
                    # We let the Mouth handle the UI update after it speaks.
            except Exception as e:
                print(e)
            finally:
                if os.path.exists(temp_wav): os.remove(temp_wav)