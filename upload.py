
import vimeo
import os
from dotenv import load_dotenv
from weather import weather_description

load_dotenv()
vimeo_token = os.getenv('VIMEO_TOKEN')
description = weather_description()

def text_without_extension(text):
    return text[:-4]

def upload_video(output_path):
    print('Sending to vimeo', output_path)
    client = vimeo.VimeoClient(token=vimeo_token)
    client.upload(output_path, data={
    'name': text_without_extension(output_path),
    'description': description
})