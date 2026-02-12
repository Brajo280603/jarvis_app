from ytmusicapi import YTMusic
import subprocess
import os

SOCKET_PATH = "/tmp/mpv_socket"

def _send_command(command):
    """Sends a command to the running MPV instance via socket."""
    try:
        # echo 'cycle pause' | socat - /tmp/mpv_socket
        cmd = f"echo '{command}' | socat - {SOCKET_PATH}"
        subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def play(query):
    """Searches and plays music with IPC socket enabled."""
    try:
        print(f"\n🎵 Searching for: {query}", flush=True)
        yt = YTMusic()
        results = yt.search(query, filter="songs")
        
        if not results: return "I couldn't find that song."

        track = results[0]
        video_id = track['videoId']
        title = track['title']
        url = f"https://music.youtube.com/watch?v={video_id}"

        # 1. Kill old player
        subprocess.run(["pkill", "mpv"], stderr=subprocess.DEVNULL)
        
        # 2. Start new player with Socket Control
        # --input-ipc-server: Allows us to send commands later
        cmd = [
            "mpv", 
            "--no-video", 
            f"--input-ipc-server={SOCKET_PATH}", 
            url
        ]
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        return f"Playing **{title}**."
    except Exception as e:
        return f"Error: {e}"

def pause():
    """Toggles Play/Pause."""
    _send_command("cycle pause")
    return "Music paused/resumed."

def stop():
    """Stops the music completely."""
    # We use pkill for a hard stop, simpler than socket for quitting
    subprocess.run(["pkill", "mpv"], stderr=subprocess.DEVNULL)
    # Also clean up the socket file
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
    return "Music stopped."