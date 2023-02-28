#!/usr/bin/python3
import os
import requests
import datetime
import ffmpeg
import argparse
import subprocess
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
        print('File saved ', filename)
        # Wait 30s
    else:
        print('Error fetching snapshot.')

    # Merge photos
    if now.hour == 23 and now.minute >= 58 and now.second >= 0:
        folder_path = os.path.join(args.output, now.strftime('%d-%m-%Y'))
        subprocess.run(["python3", "compiler.py", '--source',
                        folder_path, '--remove_snapshots'])
