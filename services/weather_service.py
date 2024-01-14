from typing import Optional, Tuple
import httpx
from fastapi import HTTPException
from httpx import Response

from infrastructure import weather_cache

import requests

from models.valiadating_data import validate_units
from models.validation_error import ValidationError

api_key: Optional[str] = None


async def get_latitude_longitude(city: str, country: str) -> list:
    try:
        q = f'{city},{country}'
        get_latitude_longitude_url = f'https://api.openweathermap.org/geo/1.0/direct?q={q}&appid={api_key}'
        async with httpx.AsyncClient() as client:
            resp: Response = await client.get(get_latitude_longitude_url)

        resp.raise_for_status()
        data = resp.json()
        latitude = data[0]['lat']
        longitude = data[0]['lon']
        lat_lon = [latitude, longitude]
        return lat_lon
    except (IndexError, KeyError) as e:
        raise HTTPException(status_code=400, detail="Please enter valid City name and Country.")


async def get_report(city: str, country: str, units: str) -> dict:

    try:
        city, country, units = validate_units(city, country, units)
        forecast = weather_cache.get_weather(city, country, units)
        if not forecast:
            latitude, longitude = await get_latitude_longitude(city, country)

            get_weather_data = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units={units}"

            async with httpx.AsyncClient() as client:
                resp: Response = await client.get(get_weather_data)
                resp.raise_for_status()

                data = resp.json()
                forecast = data['main']
                weather_cache.set_weather(city, country, units, forecast)

        return forecast
    except (httpx.HTTPError, ValidationError, KeyError) as e:
        raise HTTPException(status_code=500, detail=str(e))

