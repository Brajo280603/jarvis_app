import subprocess

APPS = {
    "firefox": "firefox", "browser": "firefox",
    "chrome": "google-chrome", "code": "code",
    "vscode": "code", "terminal": "gnome-terminal",
    "files": "nautilus", "spotify": "spotify"
}

def set_volume(level):
    """Sets system volume (0-100%)"""
    try:
        cmd = f"pactl set-sink-volume @DEFAULT_SINK@ {level}%"
        subprocess.run(cmd.split(), stderr=subprocess.DEVNULL)
        return f"Volume set to {level}%."
    except:
        return "Failed to set volume."

def set_brightness(level):
    """Sets screen brightness (0-100%) using brightnessctl"""
    try:
        # brightnessctl handles the math automatically
        cmd = f"brightnessctl s {level}%"
        subprocess.run(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"Brightness set to {level}%."
    except:
        return "Failed to set brightness. Is brightnessctl installed?"

def launch_app(app_name):
    """Launches a Linux application"""
    key = app_name.lower().strip()
    if key in APPS:
        subprocess.Popen(APPS[key], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        return f"Opening {key}."
    return f"I don't know the app {app_name}."