import os
import requests
import sys

def send_to_telegram(video_path):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendVideo"
    
    with open(video_path, "rb") as video:
        files = {"video": video}
        data = {"chat_id": chat_id, "caption": "Ваш сгенерированный аватар"}
        response = requests.post(url, files=files, data=data)
        return response.json()

# Логика генерации видео здесь (упрощенно)
# ...
# После генерации:
# send_to_telegram("output.mp4")
