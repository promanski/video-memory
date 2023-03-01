#!/usr/bin/python3
import os
import requests
import datetime
import ffmpeg
import argparse
import subprocess
from PIL import Image
from dotenv import load_dotenv


parser = argparse.ArgumentParser(description='video-memory')
parser.add_argument('--folder', type=str,
                    help='snapshots folder')
args = parser.parse_args()

folder = args.folder  # podaj ścieżkę do folderu z plikami jpg
for file in os.listdir(folder):  # iteruj po wszystkich plikach w folderze
    if file.endswith(".jpg"):  # sprawdź, czy plik ma rozszerzenie jpg
        try:
            # otwórz plik jako obraz
            img = Image.open(os.path.join(folder, file))
            img.verify()  # sprawdź, czy obraz jest poprawny i nieuszkodzony
            print(file + " jest poprawnym plikiem jpg")
        except Exception as e:
            print(file + " jest niepoprawnym lub uszkodzonym plikiem jpg")
            os.remove(os.path.join(folder, file))
            print(e)  # wyświetl błąd
