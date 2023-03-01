from PIL import Image, ImageFile
import os
import argparse
parser = argparse.ArgumentParser(description='image-scaler')
parser.add_argument('--source', type=str,
                    help='snapshots folder')
args = parser.parse_args()

folder = args.source

max_width = 1920
max_height = 1080

ImageFile.LOAD_TRUNCATED_IMAGES = True
for filename in os.listdir(folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image = Image.open(os.path.join(folder, filename))
        width, height = image.size
        scale = min(max_width / width, max_height / height)
        new_image = image.resize(
            (int(width * scale), int(height * scale)), Image.ANTIALIAS)
        new_image.save(os.path.join(folder, filename))
