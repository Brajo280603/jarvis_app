# JARVIS 3.0: Dual-Brain Desktop Assistant

JARVIS is a fully local, offline, voice-activated AI desktop assistant. Unlike wrapper apps that rely on cloud APIs, Jarvis runs entirely on your own hardware, ensuring absolute privacy, zero subscription fees, and deep system-level integration.

The core innovation of this project is its Dual-Brain Architecture, which splits tasks between a hyper-fast, specialized routing model and a deeper conversational reasoning model to achieve sub-second latency on standard hardware.

---

## Key Features

* 100% Offline & Local: Powered by Ollama, running open-source models directly on your hardware. No internet required for core functions.
* Dual-Brain Routing: 
  * The Reflexes: Uses FunctionGemma to instantly parse commands and trigger OS tools (latency < 200ms).
  * The Intellect: Uses Gemma 3 (1B) for natural language understanding, context retention, and conversational replies.
* JIT Parameter Injection: Securely handles volatile system data (like clipboard contents) using dynamic token swapping, preventing context-window bloat and LLM hallucinations.
* The Dream Protocol (Memory): An asynchronous background ETL pipeline that activates during system idle time to extract, deduplicate, and persist facts from short-term RAM into a long-term Markdown knowledge base.
* Voice Pipeline: Integrated STT and TTS for a hands-free experience.

## Technology Stack

* Language: Python 3.10+
* LLM Engine: Ollama
* Routing Model: functiongemma:270m
* Conversational Model: gemma3:1b
* Speech-to-Text (Ears): faster-whisper (base.en, int8 optimized)
* Text-to-Speech (Mouth): piper-tts (en_US-libritts_r-medium)
* Audio & OS Control: mpv, socat, pyperclip, asteval

---

## Implemented Skills

1. System Clipboard Integration: Reads and manipulates the system clipboard on demand using token injection (<<CLIPBOARD>>).
2. Safe Code Runner: Executes mathematical operations and sandboxed logic locally without risking system integrity.
3. YouTube Music Daemon: A background music controller utilizing an IPC socket (mpv + socat) for seamless play, pause, and stop controls via voice.
4. Automated WhatsApp: Browser-based automation for sending instant messages to predefined contacts.
5. Persistent Note-Taking: Appends timestamped thoughts and logs to local Markdown files.

---

## Installation & Setup

### Prerequisites
You must be running a Linux environment (Debian/Ubuntu recommended) and have Ollama installed and running.

1. Install System Dependencies:
   ```bash
   sudo apt update
   sudo apt install socat mpv xclip xdotool
