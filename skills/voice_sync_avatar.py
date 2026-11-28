import os
from pathlib import Path
import subprocess
from gradio_client import Client

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

if not audio_path:
    print("No audio found, generating voice.mp3 with edge-tts...")
    subprocess.run(['edge-tts', '--voice', 'ru-RU-SvetlanaNeural', '--text', 'Привет! Я твой цифровой аватар, и теперь я говорю как живой человек.', '--write-media', 'voice.mp3'], check=True)
    audio_path = "voice.mp3"

hf_token = os.environ.get("HUGGINGFACE_API_TOKEN")
spaces = [
    "TMElyralab/MuseTalk",
    "vinthony/SadTalker",
    "fffiloni/EchoMimic",
    "KwaiVGI/LivePortrait"
]

success = False
error_log = ""

for space in spaces:
    try:
        print(f"Trying to connect to Space: {space}...")
        client = Client(space, token=hf_token)
        api_info = client.view_api(return_format="dict")
        
        # Попытка найти подходящий эндпоинт
        endpoints = list(api_info.get('named_endpoints', {}).keys())
        api_name = endpoints[0] if endpoints else None
        
        # Вызов (упрощенно для примера, логика подбора может требовать уточнения API)
        result = client.predict(image_path, audio_path, api_name=api_name)
        
        video_path = result[0] if isinstance(result, (list, tuple)) else result
        if video_path and Path(video_path).exists():
            print(f"Success with space {space}!")
            vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p"
            subprocess.run(['ffmpeg', '-i', video_path, '-i', audio_path, '-vf', vf, '-c:v', 'libx264', '-c:a', 'aac', '-shortest', 'out.mp4', '-y'], check=True)
            success = True
            break
    except Exception as e:
        err_msg = f"Space {space} failed: {str(e)}"
        print(err_msg)
        error_log += err_msg + "\n"

if not success:
    print("All Hugging Face spaces failed. Falling back to zoompan.")
    with open("status.txt", "w") as f:
        f.write(f"Neural spaces failed:\n{error_log}")
        
    vf = (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        "setsar=1,"
        "zoompan=z='min(zoom+0.0015,1.2)':d=250:s=1080x1920:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',"
        "format=yuv420p"
    )
    cmd = ['ffmpeg', '-loop', '1', '-i', image_path, '-i', audio_path, '-vf', vf, '-shortest', '-c:v', 'libx264', '-c:a', 'aac', '-pix_fmt', 'yuv420p', 'out.mp4', '-y']
    subprocess.run(cmd, check=True)
    print("Fallback video generated.")
