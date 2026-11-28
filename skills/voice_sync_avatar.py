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

if not audio_path:
    print("No audio found, generating voice.mp3 with gTTS...")
    tts = gTTS(text="Привет! Я твой цифровой аватар, и теперь я умею говорить как живой человек.", lang='ru')
    tts.save("voice.mp3")
    audio_path = "voice.mp3"

hf_token = os.environ.get("HUGGINGFACE_API_TOKEN")
spaces = [
    "KwaiVGI/LivePortrait",
    "TMElyralab/MuseTalk",
    "fffiloni/EchoMimic",
    "vinthony/SadTalker"
]

success = False
error_log = ""

for space in spaces:
    try:
        print(f"Trying to connect to Space: {space}...")
        client = Client(space, token=hf_token)
        
        # Автоматический просмотр API для выбора метода
        api_info = client.view_api(return_format="dict")
        print(f"API info for {space}: {list(api_info.get('named_endpoints', {}).keys())}")
        
        # Попытка вызвать первый доступный эндпоинт или стандартный
        endpoints = list(api_info.get('named_endpoints', {}).keys())
        api_name = endpoints[0] if endpoints else None
        
        # Пробуем предсказание в зависимости от пространства
        if "LivePortrait" in space:
            result = client.predict(
                source_image=image_path,
                driving_video=audio_path, # Если ожидает видео или аудио
                api_name=api_name
            )
        elif "SadTalker" in space:
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
                api_name=api_name if api_name else "/test"
            )
        else:
            # Универсальный вызов по аналогии
            result = client.predict(
                image=image_path,
                audio=audio_path,
                api_name=api_name
            )

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
