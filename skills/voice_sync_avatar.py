import os, asyncio, edge_tts, subprocess
from supabase import create_client

# Конфигурация
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def generate_audio(text, output_file):
    communicate = edge_tts.Communicate(text, "ru-RU-SvetlanaNeural")
    await communicate.save(output_file)

def run_lipsync(video_path, audio_path, output_path):
    # Упрощенный липсинк через FFmpeg (наложение аудио на видео)
    cmd = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest {output_path}"
    subprocess.run(cmd, shell=True, check=True)

async def main():
    text = "Привет! Я твой автономный ИИ-ассистент. Система обновлена, и теперь я работаю полностью на автопилоте"
    await generate_audio(text, "voice.mp3")
    
    # Скачивание видео из Supabase
    with open("input.mp4", "wb") as f:
        f.write(supabase.storage.from_("avatars").download("avatar_1.mp4"))
    
    run_lipsync("input.mp4", "voice.mp3", "test_voice_1.mp4")
    
    # Загрузка в Supabase
    with open("test_voice_1.mp4", "rb") as f:
        supabase.storage.from_("avatars").upload("test_voice_1.mp4", f.read())
    
    print("https://demkine776-sketch.supabase.co/storage/v1/object/public/avatars/test_voice_1.mp4")

if __name__ == "__main__":
    asyncio.run(main())
