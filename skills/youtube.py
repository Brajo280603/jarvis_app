from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url):
    video_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return video_id.group(1) if video_id else None

def get_transcript(url):
    try:
        vid = get_video_id(url)
        if not vid: return "Invalid YouTube URL."
        
        # Fetch transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(vid)
        
        # Combine text (First 2000 chars to save RAM)
        full_text = " ".join([t['text'] for t in transcript_list])
        return full_text[:2000] + "..." 
        
    except Exception as e:
        return f"Could not fetch transcript. Error: {str(e)}"