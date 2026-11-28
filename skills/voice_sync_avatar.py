import os
from pathlib import Path
import subprocess
from gradio_client import Client
from gtts import gTTS

def find_image():
    root_dir = Path('.').resolve()
    for file in root_dir.iterdir():
        if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            return str(file)
    return None

def find_audio():
    root_dir = Path('.').resolve()
    for file in root_dir.iterdir():
        if file.is_file() and file.suffix.lower() in ['.mp3', '.wav']:
            return str(file)
    return None

image_path = find_image()
audio_path = find_audio()

if not image_path:
    print("Error: No image file found.")
    exit(1)

# Генерация аудио, если не найдено
if not audio_path:
    print("No audio found, generating voice.mp3 with gTTS...")
    tts = gTTS(text="Привет! Я твой цифровой аватар, и теперь я умею говорить как живой человек.", lang='ru')
    tts.save("voice.mp3")
    audio_path = "voice.mp3"

success = False
try:
    print("Attempting Lip-Sync with SadTalker...")
    client = Client("vinthony/SadTalker")
    result = client.predict(
        source_image=image_path,
        driven_audio=audio_path,
        preprocess="full",
        still_mode=True,
        use_enhancer=False,
        batch_size=1,
        size=512,
        pose_style=0,
        facerender="facevid2vid",
        exp_scale=1.0,
        use_ref_video=False,
        ref_video=None,
        ref_info=None,
        use_idle_mode=False,
        length_of_audio=0,
        api_name="/test"
    )
    video_path = result[0]
    
    # Обработка видео под 1080x1920 и наложение аудио
    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p"
    subprocess.run(['ffmpeg', '-i', video_path, '-i', audio_path, '-vf', vf, '-c:v', 'libx264', '-c:a', 'aac', '-shortest', 'out.mp4', '-y'], check=True)
    success = True
    print("Lip-Sync completed successfully.")
except Exception as e:
    print(f"Lip-Sync failed: {e}. Falling back to zoompan.")

if not success:
    print("Generating fallback video with zoompan...")
    vf = (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        "setsar=1,"
        "zoompan=z='min(zoom+0.0015,1.2)':d=250:s=1080x1920:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',"
        "format=yuv420p"
    )
    # Длительность берется из аудиофайла
    cmd = ['ffmpeg', '-loop', '1', '-i', image_path, '-i', audio_path, '-vf', vf, '-shortest', '-c:v', 'libx264', '-c:a', 'aac', '-pix_fmt', 'yuv420p', 'out.mp4', '-y']
    subprocess.run(cmd, check=True)
    print("Fallback video generated.")
