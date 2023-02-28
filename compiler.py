import os
import ffmpeg
import datetime
import argparse
from upload import upload_video

parser = argparse.ArgumentParser(description='video-memory')
parser.add_argument('--source', type=str, default='./data',
                    help='define snapshots folder')
parser.add_argument('--remove_snapshots', type=bool, default=False,
                    help='remove snapshots after upload')
args = parser.parse_args()
now = datetime.datetime.now()
folder_path = args.source
if os.path.exists(folder_path):
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
            .input(os.path.join(folder_path, '*.jpg'), pattern_type='glob', framerate=30)
            .output(output_path, pix_fmt='yuv420p', vcodec='libx265', s='1920x1080', preset='slow', crf=28)
            .run()
        )
        upload_video(output_path)
        # Delete remain photos
    if args.remove_snapshots:
        for f in files:
            os.remove(os.path.join(folder_path, f))
else:
    print('Folder does not exists')
    exit
