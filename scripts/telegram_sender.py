import os, json, urllib.request, requests

def send_video_to_telegram(video_path, caption):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendVideo"
    
    with open(video_path, 'rb') as video_file:
        files = {'video': video_file}
        data = {'chat_id': chat_id, 'caption': caption}
        response = requests.post(url, data=data, files=files)
        return response.json()
