import os
from pathlib import Path
import subprocess

def find_image():
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

# Масштабирование 9:16 с обрезкой и плавный zoompan
vf = (
    "scale=1080:1920:force_original_aspect_ratio=increase,"
    "crop=1080:1920,"
    "setsar=1,"
    "zoompan=z='min(zoom+0.0015,1.2)':d=250:s=1080x1920:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',"
    "format=yuv420p"
)

cmd = [
    'ffmpeg', '-loop', '1', '-i', image_path,
    '-vf', vf,
    '-t', '10', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', 'out.mp4', '-y'
]

subprocess.run(cmd, check=True)
print("Video generated successfully.")
