
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def weather_description():
    def get_wind_direction(degrees):
        directions = {
            "północny": (0, 22.5),
            "północno-wschodni": (22.5, 67.5),
            "wschodni": (67.5, 112.5),
            "południowo-wschodni": (112.5, 157.5),
            "południowy": (157.5, 202.5),
            "południowo-zachodni": (202.5, 247.5),
            "zachodni": (247.5, 292.5),
            "północno-zachodni": (292.5, 337.5),
            "północny": (337.5, 360.0)
        }
        for direction, (lower, upper) in directions.items():
            if degrees >= lower and degrees < upper:
                return f"{direction}"
    # OpenWeatherMap request
    api_key = os.getenv('OPEN_WEATHER_API_KEY')
    lat = os.getenv('LOCATION_LATITUDE')
    lon = os.getenv('LOCATION_LONGITUDE')
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&lang=pl&units=metric&appid={api_key}'
    response = requests.get(url)
    data = json.loads(response.text)
    if data['cod'] != 200:
        print('Error fetching from OpenWeatherAPI')
        exit()

    # Fetching data
    sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
    sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    wind_speed = data['wind']['speed']
    wind_direction = get_wind_direction(data["wind"]["deg"])

    rain = 0
    snow = 0
    if 'rain' in data:
        rain = data['rain']['3h']
    if 'snow' in data:
        snow = data['snow']['3h']
    conditions = data['weather'][0]['description']

    # Saving file to one variable
    now = datetime.now()
    result = f'Dzisiaj ({now.strftime("%d.%m.%Y")}) jest ({conditions.lower()}) a wschód słońca był o godzinie {sunrise}, a zachód o godzinie {sunset}. Minimalna temperatura wyniosła {temp_min} °C, a maksymalna {temp_max} °C. Prędkość wiatru wyniosła {wind_speed} m/s, kierunek {wind_direction}°.'
    if rain > 0:
        result += f' Ilość opadów deszczu w ciągu ostatnich 3 godzin to {rain} mm.'
    if snow > 0:
        result += f' Ilość opadów śniegu w ciągu ostatnich 3 godzin to {snow} mm.'
    if rain == 0 and snow == 0:
        result += ' Nie było opadów deszczu ani śniegu.'
    return result
