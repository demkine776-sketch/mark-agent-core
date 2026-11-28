import os, glob, subprocess
from gtts import gTTS
import imageio_ffmpeg

t = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
c = (os.environ.get("TELEGRAM_CHAT_ID") or os.environ.get("CHAT_ID") or "").strip()
ff = imageio_ffmpeg.get_ffmpeg_exe()
gTTS("Hello Boss! Avatar system is online.", lang="en").save("v.mp3")
imgs = glob.glob("assets/**/*.*", recursive=True)
inp = ["-loop", "1", "-i", imgs[0]] if imgs else ["-f", "lavfi", "-i", "color=c=blue:s=1080x1920:r=25"]
vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" if imgs else "format=yuv420p"
subprocess.run([ff, "-y", *inp, "-i", "v.mp3", "-vf", vf, "-c:v", "libx264", "-c:a", "aac", "-shortest", "out.mp4"], check=True)
url = "https://" + "api.telegram.org/bot" + t + "/sendVideo"
subprocess.run(["curl", "-s", "-X", "POST", url, "-F", f"chat_id={c}", "-F", "video=@out.mp4"], check=True)