import os
import ast
import requests
import glob
import subprocess

def run_task():
    try:
        # Установка зависимостей
        subprocess.check_call(["pip", "install", "-q", "edge-tts", "requests"])

        # Генерация озвучки
        text = "Hello Boss! My avatar system is now online and ready to create viral content for YouTube and Instagram."
        os.system(f'edge-tts --text "{text}" --voice en-US-AriaNeural --write-media voice.mp3')

        # Поиск фото или создание фона
        images = glob.glob("assets/**/*.jpg", recursive=True) + glob.glob("assets/**/*.png", recursive=True)
        img_path = images[0] if images else "background.png"
        if not images:
            os.system('ffmpeg -f lavfi -i color=c=blue:s=1080x1920:d=7 -t 7 background.png')

        # Сборка видео
        os.system('ffmpeg -loop 1 -i ' + img_path + ' -i voice.mp3 -vf "zoompan=z=\'min(zoom+0.001,1.1)\':d=125,format=yuv420p" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest -t 7 output.mp4 -y')

        # Отправка в Telegram
        token = os.environ['TELEGRAM_BOT_TOKEN']
        chat_id = os.environ['TELEGRAM_CHAT_ID']
        url = f"https://api.telegram.org/bot{token}/sendVideo"
        
        with open("output.mp4", "rb") as video:
            requests.post(url, data={"chat_id": chat_id}, files={"video": video})

    except Exception as e:
        token = os.environ['TELEGRAM_BOT_TOKEN']
        chat_id = os.environ['TELEGRAM_CHAT_ID']
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": f"Error: {str(e)}"})

if __name__ == "__main__":
    run_task()
