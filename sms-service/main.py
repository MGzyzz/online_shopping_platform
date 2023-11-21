import os
import fastapi
from starlette import status
from tortoise import Tortoise, ConfigurationError
import dto
from adapters import SMSAdapter
import httpx

app = fastapi.FastAPI()

DATABASE_URL = os.environ.get('DATABASE_URL')

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default",
        }
    },
}


@app.on_event
async def init():
    try:
        await Tortoise.init(
        config=TORTOISE_ORM
        )
        await Tortoise.generate_schemas()
    except ConfigurationError as e:
        print(f"Error initializing Tortoise: {e}")


@app.on_event('shutdown')
async def shutdown():
    await Tortoise.close_connections()


CORE_URL = 'http://core-app-1:8000'


@app.get('/user/{id_}')
def get_user(id_: int):
    resp = httpx.get(f'{CORE_URL}/api/user/{id_}')
    as_json = resp.json()
    print(as_json)
    return as_json


@app.post('/sms/send')
async def send_sms(body: dto.SendSmsDto):
    await SMSAdapter().send(body)
    
    return fastapi.responses.Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app',  host='0.0.0.0', port=1026, reload=True)
