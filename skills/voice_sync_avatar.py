import os
import glob
import subprocess
import ast
import requests

os.system("pip install -q gTTS requests")

from gtts import gTTS

def main():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    try:
        # 1. Озвучка gTTS
        audio_path = "voice.mp3"
        tts = gTTS("Hello Boss! Avatar system is online.", lang="en")
        tts.save(audio_path)
        
        # 2. Поиск фото или генерация фона
        output_video = "output.mp4"
        images = glob.glob("assets/**/*.*", recursive=True)
        valid_images = [img for img in images if img.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        
        if valid_images:
            img_path = valid_images[0]
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", img_path,
                "-i", audio_path,
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                "-c:v", "libx264",
                "-tune", "stillimage",
                "-c:a", "aac",
                "-pix_fmt", "yuv420p",
                "-shortest",
                output_video
            ]
        else:
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", "color=c=blue:s=1080x1920:d=10",
                "-i", audio_path,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-pix_fmt", "yuv420p",
                "-shortest",
                output_video
            ]
        
        subprocess.run(cmd, check=True)
        
        # 3. Отправка видео в Telegram
        if bot_token and chat_id:
            with open(output_video, "rb") as video_file:
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendVideo",
                    data={"chat_id": chat_id, "caption": "🤖 Avatar System Online!"},
                    files={"video": video_file}
                )
    except Exception as e:
        error_text = f"Voice sync error: {str(e)}"
        if bot_token and chat_id:
            try:
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    data={"chat_id": chat_id, "text": error_text}
                )
            except Exception:
                pass

if __name__ == "__main__":
    # Проверка ast.parse
    with open(__file__, "r", encoding="utf-8") as f:
        ast.parse(f.read())
    main()
