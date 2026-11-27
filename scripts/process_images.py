import os
from PIL import Image

def split_image(input_path, output_dir):
    img = Image.open(input_path)
    width, height = img.size
    part_width = width // 3
    for i in range(3):
        part = img.crop((i * part_width, 0, (i + 1) * part_width, height))
        part.save(os.path.join(output_dir, f'look_{i+2}.jpg'))

if __name__ == "__main__":
    os.makedirs('assets/looks/girl_1', exist_ok=True)
    split_image('1795788674324.jpg', 'assets/looks/girl_1')
