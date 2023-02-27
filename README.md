# video memory

Create timelaps from IP camera's snapshots, get some weather info and post it on Vimeo.

## Requirements 

```bash
python 3.x
```
## Installation

```py
pip3 install -r requirements.txt
```
Add `.env` file to root of your project with values:
```
OPEN_WEATHER_API_KEY  =  "your_api_key"
CAMERA_SNAPSHOT_URL  =  "your_camera_url"
# Vimeo token (read/write)
VIMEO_TOKEN  =  "vimeo_token"
# LOCATION OF CAMERA
LOCATION_LATITUDE  =  "10.00"
LOCATION_LONGITUDE  =  "10.00"
```
## Usage example
| Argument | Description | Required | Default |
|--|--|--|--|
| `-h`, `--help` | Show help message and exit  | No | N/A
| `--output` | Define snapshots output | No | `./data`

Add script to crontab to execute every one minute with ``$ crontab -e``.
Add following code (execute python code every 60 seconds)
```
 * * * * * /usr/bin/python /path/to/project/video-memory/script.py
```
At the end of a day, it will merge all snapshots into single video and post it on Vimeo.
