import os, glob, subprocess
from gtts import gTTS
import imageio_ffmpeg
from PIL import Image

if not glob.glob("assets/**/*.*", recursive=True):
    Image.new("RGB", (1080, 1920), (15, 35, 90)).save("bg.png")
    inp = ["-loop", "1", "-i", "bg.png"]
else:
    inp = ["-loop", "1", "-i", glob.glob("assets/**/*.*", recursive=True)[0]]

ff = imageio_ffmpeg.get_ffmpeg_exe()
gTTS("Hello Boss! Avatar system is online.", lang="en").save("v.mp3")
subprocess.run([ff, "-y", *inp, "-i", "v.mp3", "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "out.mp4"], check=True)
