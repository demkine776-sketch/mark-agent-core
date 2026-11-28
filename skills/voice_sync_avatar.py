import os
from pathlib import Path
import subprocess

def find_image():
    # Ищем в корне репозитория (текущая рабочая директория воркера)
    root_dir = Path('.').resolve()
    for file in root_dir.iterdir():
        if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            return str(file)
    return None

image_path = find_image()
if not image_path:
    print("Error: No image file found in root directory.")
    exit(1)

print(f"Using image: {image_path}")

# Пример команды ffmpeg с zoompan
# zoompan=z='min(zoom+0.0015,1.5)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'
cmd = [
    'ffmpeg', '-loop', '1', '-i', image_path,
    '-vf', "zoompan=z='min(zoom+0.0015,1.5)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',format=yuv420p",
    '-t', '10', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', 'out.mp4', '-y'
]

subprocess.run(cmd, check=True)
print("Video generated successfully.")
