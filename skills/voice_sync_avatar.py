import os, glob, subprocess
from gtts import gTTS
import imageio_ffmpeg

token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
chat_id = os.environ.get("TELEGRAM_CHAT_ID") or os.environ.get("CHAT_ID") or ""

try:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    gTTS("Hello Boss! Avatar pipeline is live.", lang="en").save("voice.mp3")
    imgs = glob.glob("assets/**/*.jpg", recursive=True) + glob.glob("assets/**/*.png", recursive=True)
    inp = ["-loop", "1", "-i", imgs[0]] if imgs else ["-f", "lavfi", "-i", "color=c=blue:s=1080x1920:r=25"]
    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" if imgs else "format=yuv420p"
    subprocess.run([ffmpeg, "-y", *inp, "-i", "voice.mp3", "-vf", vf, "-c:v", "libx264", "-c:a", "aac", "-shortest", "output.mp4"], check=True)
    subprocess.run(["curl", "-s", "-X", "POST", f"https://api.telegram.org/bot{token}/sendVideo", "-F", f"chat_id={chat_id}", "-F", "video=@output.mp4"], check=True)
except Exception as e:
    if token and chat_id:
        subprocess.run(["curl", "-s", "-X", "POST", f"https://api.telegram.org/bot{token}/sendMessage", "-d", f"chat_id={chat_id}", "--data-urlencode", f"text=Err: {e}"])
    raise
