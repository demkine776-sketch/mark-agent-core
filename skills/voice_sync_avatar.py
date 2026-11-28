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
# Здесь будет логика ffmpeg с zoompan, использующая image_path
