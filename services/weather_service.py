from typing import Optional

import requests

api_key: Optional[str] = None


def get_latitude_longitude(city: str, country: str) -> list:
    q = f'{city},{country}'
    get_latitude_longitude_url = f'https://api.openweathermap.org/geo/1.0/direct?q={q}&appid={api_key}'
    resp = requests.get(get_latitude_longitude_url)
    resp.raise_for_status()

    data = resp.json()
    latitude = data[0]['lat']
    longitude = data[0]['lon']
    lat_lon = [latitude, longitude]
    return lat_lon


def get_report(city: str, country: str, units: str) -> dict:
    latitude, longitude = get_latitude_longitude(city, country)

    get_weather_data = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units={units}"

    resp = requests.get(get_weather_data)
    resp.raise_for_status()

    data = resp.json()
    forcast = data['main']

    return forcast