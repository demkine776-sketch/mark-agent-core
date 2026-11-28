import os
import asyncio
import requests
import subprocess

os.system("pip install -q edge-tts gTTS requests")

async def generate_audio(text, output_file="voice.mp3"):
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
        await communicate.save(output_file)
        if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
            raise Exception("edge-tts generated empty file")
    except Exception as e:
        print(f"edge-tts failed ({e}), falling back to gTTS...")
        from gtts import gTTS
        tts = gTTS(text=text, lang='en', tld='com')
        tts.save(output_file)

def run_lipsync(video_path, audio_path, output_path):
    cmd = f"ffmpeg -y -i {video_path} -i {audio_path} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest {output_path}"
    subprocess.run(cmd, shell=True, check=True)

async def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    try:
        text = "Hello Boss! Voice sync avatar is active."
        await generate_audio(text, "voice.mp3")
        
        images = os.popen("find . -name '*.mp4' -o -name '*.jpg'").read().splitlines()
        if not images:
            cmd = f"ffmpeg -y -f lavfi -i color=c=blue:s=1080x1920 -i voice.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest output.mp4"
            os.system(cmd)
            video_file = "output.mp4"
        else:
            video_file = images[0]
            run_lipsync(video_file, "voice.mp3", "output.mp4")
            video_file = "output.mp4"
            
        if token and chat_id:
            with open("output.mp4", "rb") as video:
                requests.post(
                    f"https://api.telegram.org/bot{token}/sendVideo",
                    data={"chat_id": chat_id, "caption": "Sync avatar video ready"},
                    files={"video": video}
                )
    except Exception as e:
        if token and chat_id:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data={"chat_id": chat_id, "text": f"Error in voice_sync_avatar: {str(e)}"}
            )

if __name__ == "__main__":
    asyncio.run(main())
