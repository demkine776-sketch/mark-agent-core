import os
import ast
import glob
import requests
import asyncio

def generate_voice(text, output_file="voice.mp3"):
    os.system("pip install -q edge-tts gTTS requests")
    try:
        import edge_tts
        voice = "en-US-AriaNeural"
        asyncio.run(edge_tts.Communicate(text, voice).save(output_file))
        if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
            raise Exception("edge-tts generated empty file")
    except Exception as e:
        print(f"edge-tts failed ({e}), falling back to gTTS...")
        from gtts import gTTS
        tts = gTTS(text=text, lang='en', tld='com')
        tts.save(output_file)

def run_autonomous_task():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    try:
        text = "Hello Boss! My avatar system is now online and ready to create viral content for YouTube and Instagram."
        generate_voice(text, "voice.mp3")
        
        images = glob.glob("assets/**/*.jpg", recursive=True) + glob.glob("assets/**/*.png", recursive=True)
        bg_input = images[0] if images else ""
        
        if bg_input:
            input_cmd = f"-loop 1 -i {bg_input}"
        else:
            input_cmd = "-f lavfi -i color=c=blue:s=1080x1920"
            
        cmd = f"ffmpeg -y {input_cmd} -i voice.mp3 -vf \"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0015,1.15)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920\" -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest output.mp4"
        os.system(cmd)
        
        if not os.path.exists("output.mp4"):
            raise Exception("FFmpeg failed to generate output.mp4")
            
        with open("output.mp4", "rb") as video:
            r = requests.post(
                f"https://api.telegram.org/bot{token}/sendVideo", 
                data={"chat_id": chat_id, "caption": "🎬 Тестовый ролик аватара готов!"}, 
                files={"video": video}
            )
            r.raise_for_status()
            
    except Exception as e:
        if token and chat_id:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage", 
                data={"chat_id": chat_id, "text": f"⚠️ Ошибка сборки/отправки: {str(e)}"}
            )

if __name__ == "__main__":
    run_autonomous_task()
