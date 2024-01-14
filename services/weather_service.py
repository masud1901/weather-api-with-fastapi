from typing import Optional, Tuple
import httpx
from fastapi import HTTPException
from httpx import Response

from infrastructure import weather_cache

import requests

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


def validate_units(
        city: str, country: str, units: str
) -> Tuple[str, str, str]:
    city = city.lower().strip()

    if not country:
        country = 'BGD'

    if len(country) not in (2, 3):
        error = f'Invalid country code: {country}. It must be a two or three-letter abbreviation.'
        raise ValidationError(status_code=400, error_msg=error)

    valid_units = {'standard', 'metric', 'imperial'}
    if units:
        units = units.strip().lower()
        if units not in valid_units:
            error = f"Invalid units '{units}'. It must be one of {valid_units}."
            raise ValidationError(status_code=400, error_msg=error)

    return city, country, units
