import os
import ffmpeg
import datetime
import argparse
from upload import upload_video


def merge_and_upload():
    parser = argparse.ArgumentParser(description='video-memory')
    parser.add_argument('--output', type=str, default='./data',
                        help='define snapshots output folder')
    args = parser.parse_args()
    now = datetime.datetime.now()
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
            .input(os.path.join(folder_path, '*.jpg'), pattern_type='glob', framerate=30)
            .output(output_path, pix_fmt='yuv420p', vcodec='libx265', s='1920x1080', preset='slow', crf=28)
            .run()
        )
        upload_video(output_path)
        # Delete remain photos
        for f in files:
            os.remove(os.path.join(folder_path, f))
