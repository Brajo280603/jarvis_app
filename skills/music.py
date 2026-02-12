from ytmusicapi import YTMusic
import subprocess
import os

def play(query):
    """
    Searches YouTube Music and plays the first result using mpv.
    """
    try:
        print(f"\n🎵 Searching for: {query}", flush=True)
        yt = YTMusic()
        
        # 1. Search for Songs only
        results = yt.search(query, filter="songs")
        
        if not results:
            return "I couldn't find that song."

        # 2. Extract Data
        track = results[0]
        video_id = track['videoId']
        title = track['title']
        artist = track['artists'][0]['name']
        url = f"https://music.youtube.com/watch?v={video_id}"

        # 3. Kill any existing music (Simple Logic)
        # We run 'pkill mpv' to stop the previous song before starting a new one
        subprocess.run(["pkill", "mpv"], stderr=subprocess.DEVNULL)

        # 4. Spawn MPV in the Background
        # --no-video: Audio only (saves massive CPU/RAM)
        cmd = ["mpv", "--no-video", url]
        
        # We use Popen so Jarvis DOES NOT freeze while the song plays
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        return f"Playing **{title}** by **{artist}**."

    except Exception as e:
        print(f"❌ Music Error: {e}", flush=True)
        return "Failed to play music."