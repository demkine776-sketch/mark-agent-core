import os
import ast
import glob
import requests
import asyncio
import edge_tts

# Autonomous script for avatar video generation and delivery
def run_autonomous_task():
    try:
        # 1. Install dependencies
        os.system("pip install -q edge-tts requests")
        
        # 2. Generate voice
        text = "Hello Boss! My avatar system is now online and ready to create viral content for YouTube and Instagram."
        voice = "en-US-AriaNeural"
        asyncio.run(edge_tts.Communicate(text, voice).save("voice.mp3"))
        
        # 3. Prepare background (create color background if no image found)
        images = glob.glob("assets/**/*.jpg", recursive=True) + glob.glob("assets/**/*.png", recursive=True)
        bg_input = images[0] if images else "color=c=blue:s=1080x1920"
        
        # 4. Generate video with ffmpeg
        # Using -f lavfi for color if no image, else input image
        input_cmd = f"-i {bg_input}" if images else "-f lavfi -i color=c=blue:s=1080x1920"
        cmd = f"ffmpeg -y {input_cmd} -i voice.mp3 -vf 'zoompan=z='min(zoom+0.001,1.1)':d=125:s=1080x1920' -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest output.mp4"
        os.system(cmd)
        
        # 5. Send to Telegram
        token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        with open("output.mp4", "rb") as video:
            requests.post(f"https://api.telegram.org/bot{token}/sendVideo", 
                          data={"chat_id": chat_id}, 
                          files={"video": video})
                          
    except Exception as e:
        token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      data={"chat_id": chat_id, "text": f"Error: {str(e)}"})

if __name__ == "__main__":
    run_autonomous_task()
