import os, glob, subprocess
from gtts import gTTS
import imageio_ffmpeg
from PIL import Image

# Создаем директорию assets, если её нет
os.makedirs("assets", exist_ok=True)

# Ищем аватар, если нет - создаем заглушку (в реальности здесь должен быть портрет)
avatar_path = "assets/avatar.jpg"
if not os.path.exists(avatar_path):
    Image.new("RGB", (1080, 1920), (100, 50, 50)).save(avatar_path)

inp = ["-loop", "1", "-i", avatar_path]

ff = imageio_ffmpeg.get_ffmpeg_exe()
gTTS("Hello Boss! Avatar system is online and moving.", lang="en").save("v.mp3")

# Zoompan фильтр для "живого" эффекта
# zoom=min(zoom+0.001,1.1) - плавное приближение
zoompan = "zoompan=z='min(zoom+0.001,1.1)':d=125:s=1080x1920:fps=25"
vf = f"{zoompan},format=yuv420p"

subprocess.run([ff, "-y", *inp, "-i", "v.mp3", "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "out.mp4"], check=True)
