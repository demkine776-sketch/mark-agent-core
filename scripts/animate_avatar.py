import os
from supabase import create_client
from PIL import Image
import requests

# Инициализация Supabase
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_ROLE_KEY'])

def ensure_bucket_exists(bucket_name):
    try:
        supabase.storage.get_bucket(bucket_name)
    except:
        supabase.storage.create_bucket(bucket_name, {"public": True})

def animate_and_upload():
    ensure_bucket_exists('avatars')
    # Логика анимации (заглушка для примера)
    # ...
    # Проверка файла
    file_path = 'assets/looks/girl_1/look_1.mp4'
    if os.path.exists(file_path) and os.path.getsize(file_path) > 100 * 1024:
        with open(file_path, 'rb') as f:
            supabase.storage.from_('avatars').upload(path='look_1.mp4', file=f, file_options={"content-type": "video/mp4"})
    else:
        raise Exception("Invalid or small video file")

if __name__ == "__main__":
    animate_and_upload()
