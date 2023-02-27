#!/usr/bin/python3
import os
import requests
import time
import datetime
import ffmpeg
import argparse
from dotenv import load_dotenv
from upload import upload_video

load_dotenv()

camera_snapshot_url = os.getenv('CAMERA_SNAPSHOT_URL')
parser = argparse.ArgumentParser(description='video-memory')
parser.add_argument('--output', type=str, default='./data',
                    help='define snapshots output folder')
args = parser.parse_args()
if not os.path.exists(args.output):
    os.makedirs(args.output)
else:
    now = datetime.datetime.now()

    response = requests.get(camera_snapshot_url, stream=True)
    if response.status_code == 200:
        # Format "YYYY-MM-DD-HH-MM-SS.jpg"
        filename = now.strftime('%Y-%m-%d-%H-%M-%S.jpg')
        filepath = os.path.join(
            args.output, now.strftime('%d-%m-%Y'), filename)

        # Create date args.output
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))

        # Save file
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print('Zapisałem plik ', filename)
        # Wait 30s
    else:
        print('Error fetching snapshot.')

    # Merge photos
    if now.hour == 23 and now.minute == 59 and now.second >= 0:
        # Prepare args.output_path
        folder_path = os.path.join(args.output, now.strftime('%d-%m-%Y'))
        files = os.listdir(folder_path)
        files = [f for f in files if f.endswith('.jpg')]
        files.sort()

        output_path = os.path.join(now.strftime('%d-%m-%Y') + '.mp4')
        if os.path.exists(output_path):
            print('File exists.')
        else:
            # ffmpeg, h.265 fullHD 30fps
            (
                ffmpeg
                .input(os.path.join(args.output_path, '*.jpg'), pattern_type='glob', framerate=30)
                .output(output_path, pix_fmt='yuv420p', vcodec='libx265', s='1920x1080', preset='slow', crf=28)
                .run()
            )
            upload_video(output_path)
            # Delete remain photos
            for f in files:
                os.remove(os.path.join(folder_path, f))
