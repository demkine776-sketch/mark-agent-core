import os, asyncio, edge_tts, subprocess, requests

# Конфигурация
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

async def generate_audio(text, output_file):
    communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
    await communicate.save(output_file)

def run_ffmpeg(video_path, audio_path, output_path):
    # Наложение аудио на видео
    cmd = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest {output_path}"
    subprocess.run(cmd, shell=True, check=True)

def send_to_telegram(video_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    with open(video_path, "rb") as f:
        files = {"video": f}
        data = {"chat_id": TELEGRAM_CHAT_ID, "caption": "Готовое видео с аватаром"}
        requests.post(url, files=files, data=data)

async def main():
    text = "Hello! I am your autonomous AI assistant. The system is updated, and I am now working on full autopilot."
    await generate_audio(text, "voice.mp3")
    
    # Предполагаем, что avatar_1.mp4 уже есть в папке воркера или скачан ранее
    run_ffmpeg("avatar_1.mp4", "voice.mp3", "output.mp4")
    
    send_to_telegram("output.mp4")

if __name__ == "__main__":
    asyncio.run(main())
