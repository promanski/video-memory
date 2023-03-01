import os
import ffmpeg
import datetime
import argparse
from upload import upload_video

parser = argparse.ArgumentParser(description='ffmpeg compiler, manage files')
parser.add_argument('-s', '--source', type=str, default='./data',
                    help='source snapshots folder')
parser.add_argument('-u', '--upload', action='store_true',
                    help='upload video to vimeo')
parser.add_argument('-rs', '--remove_snapshots', action='store_true',
                    help='remove snapshots after merge')
parser.add_argument('-rv', '--remove_video', action='store_true',
                    help='remove video after snapshots merge')
args = parser.parse_args()
now = datetime.datetime.now()
folder_path = args.source
if os.path.exists(folder_path):
    files = os.listdir(folder_path)
    files = [f for f in files if f.endswith('.jpg')]
    files.sort()

    output_path = os.path.join(folder_path + '.mp4')
    if os.path.exists(output_path):
        print('File exists.')
    else:
        # ffmpeg, h.265 fullHD 30fps
        (
            ffmpeg
            .input(os.path.join(folder_path, '*.jpg'), pattern_type='glob', framerate=30)
            .output(output_path, pix_fmt='yuv420p', vcodec='libx265', bitrate='10MB', s='1920x1080', preset='fast', crf=21)
            .run()
        )
    if args.upload:
        upload_video(output_path)
    if args.remove_snapshots:
        for f in files:
            os.remove(os.path.join(folder_path, f))
    if args.remove_video:
        os.remove(output_path)
else:
    print('Folder does not exists')
    exit
