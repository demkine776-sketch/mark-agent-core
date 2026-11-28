import os, glob, subprocess
from gtts import gTTS
import imageio_ffmpeg
from PIL import Image

# Ensure assets directory exists
os.makedirs("assets", exist_ok=True)

# Path to avatar
avatar_path = "assets/avatar.jpg"

# Create avatar if not exists
if not os.path.exists(avatar_path):
    img = Image.new("RGB", (1080, 1920), (100, 100, 100))
    img.save(avatar_path)

ff = imageio_ffmpeg.get_ffmpeg_exe()
gTTS("Hello Boss! Avatar system is online and moving.", lang="en").save("v.mp3")

# Zoompan filter: zoom in slowly
# d=250 (duration in frames), z='min(zoom+0.0015,1.2)'
zoompan_filter = "zoompan=z='min(zoom+0.0015,1.2)':d=250:s=1080x1920:fps=25"

subprocess.run([
    ff, "-y", 
    "-loop", "1", "-i", avatar_path, 
    "-i", "v.mp3", 
    "-vf", f"{zoompan_filter},format=yuv420p", 
    "-c:v", "libx264", "-pix_fmt", "yuv420p", 
    "-c:a", "aac", "-shortest", "out.mp4"
], check=True)
