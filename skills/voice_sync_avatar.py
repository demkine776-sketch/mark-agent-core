import os
import subprocess
from pathlib import Path
from gradio_client import Client, handle_file
from huggingface_hub import HfApi

def generate_voice():
    subprocess.run(["edge-tts", "--voice", "ru-RU-SvetlanaNeural", "--rate=+5%", "--text", "Привет! Я твой цифровой аватар. Теперь у меня живой голос, естественная мимика и движение губ в такт каждому слову.", "--write-media", "voice.mp3"], check=True)
    if Path("voice.mp3").stat().st_size > 5000:
        return "voice.mp3"
    return None

def run_avatar():
    img_path = next(Path('.').glob('*.[jp][pn]g'), None)
    if not img_path: return
    audio_path = generate_voice()
    if not audio_path: return

    hf_token = os.environ.get("HUGGINGFACE_API_TOKEN")
    errors = []
    
    # Strategy A & B: Specific Spaces
    spaces = ["vinthony/SadTalker", "OpenTalker/SadTalker"]
    
    for space in spaces:
        try:
            client = Client(space, token=hf_token)
            res = client.predict(source_image=handle_file(str(img_path)), driven_audio=handle_file(audio_path), preprocess="crop", still_mode=True, use_enhancer=False, batch_size=1, size_of_image=256, pose_style=0, api_name="/test")
            video_path = res if isinstance(res, str) else res.get('video')
            if video_path:
                subprocess.run(["ffmpeg", "-y", "-i", video_path, "-i", audio_path, "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "out.mp4"], check=True)
                with open("status.txt", "w") as f: f.write(f"SUCCESS: animated via {space}")
                return
        except Exception as e: errors.append(f"{space}: {str(e)}")

    # Fallback
    with open("status.txt", "w") as f: f.write("FALLBACK: " + " | ".join(errors))
    subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", str(img_path), "-i", audio_path, "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "out.mp4"], check=True)

if __name__ == "__main__": run_avatar()
