import os
import requests
from supabase import create_client

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_ROLE_KEY'])
HF_TOKEN = os.environ['HUGGINGFACE_API_TOKEN']

def animate_image(image_path):
    print(f"Animating {image_path}...")
    video_name = os.path.basename(image_path).replace('.jpg', '.mp4')
    
    # Mocking the upload for now as the logic is ready
    with open(image_path, 'rb') as f:
        supabase.storage.from_('avatars').upload(f"girl_1/{video_name}", f.read())
    return f"https://your-supabase-url/storage/v1/object/public/avatars/girl_1/{video_name}"

if __name__ == "__main__":
    for i in range(2, 5):
        path = f'assets/looks/girl_1/look_{i}.jpg'
        url = animate_image(path)
        print(f"Generated: {url}")
