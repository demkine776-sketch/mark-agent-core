import os, glob, requests
os.system("pip install -q gTTS requests")
from gtts import gTTS

try:
    gTTS("Hello Boss! My avatar system is now online and ready to create viral content.", lang="en").save("voice.mp3")
    imgs = glob.glob("assets/**/*.jpg", recursive=True) + glob.glob("assets/**/*.png", recursive=True)
    if imgs:
        cmd = f'ffmpeg -y -loop 1 -i "{imgs[0]}" -i voice.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" -c:v libx264 -c:a aac -shortest output.mp4'
    else:
        cmd = 'ffmpeg -y -f lavfi -i color=c=blue:s=1080x1920:r=25 -i voice.mp3 -vf "format=yuv420p" -c:v libx264 -c:a aac -shortest output.mp4'
    os.system(cmd)
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    with open("output.mp4", "rb") as f:
        r = requests.post(f"https://api.telegram.org/bot{token}/sendVideo", data={"chat_id": chat_id, "caption": "Готово, Босс! Первый тестовый ролик с аватаром."}, files={"video": f})
    print("TG response:", r.status_code, r.text)
except Exception as e:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if token and chat_id:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": f"Ошибка сборки: {e}"})
    raise
    
