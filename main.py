import json
from pathlib import Path

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from api import weather_api
from services import weather_service
from views import home

api = fastapi.FastAPI()


def configure():
    configure_routing()
    configure_api_keys()


def configure_api_keys():
    file = Path('settings_tem.json').absolute()
    if not file.exists():
        print(f"WARNING:{file} file not found, you cannot continue, please see settings_tem.json")
        raise Exception("settings.json file not found, you cannot continue, please see settings_tem.json")

    with open('settings_tem.json') as fin:
        settings = json.load(fin)
        weather_service.api_key = settings.get('api_key')


def configure_routing():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(home.router)
    api.include_router(weather_api.router)


if __name__ == "__main__":
    configure()
    uvicorn.run(api, port=8000, host="127.0.0.1")
else:
    configure()
