import fastapi
import uvicorn

api = fastapi.FastApi()


@api.get("/")
def index():
    return "Hello Weather App!"


if __name__ == "__main__":
    uvicorn.run(api, port=8000, host="127.0.0.1")
