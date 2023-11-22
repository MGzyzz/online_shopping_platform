import fastapi
from starlette import status
import dto
from adapters import SMSAdapter
import httpx

app = fastapi.FastAPI()

CORE_URL = 'http://core-app-1:8000'


@app.get('/user/{id_}')
def get_user(id_: int):
    resp = httpx.get(f'{CORE_URL}/api/user/{id_}')
    as_json = resp.json()
    print(as_json)
    return as_json.get('phone')


@app.post('/sms/send/')
async def send_sms(body: dto.SendSmsDto, ):
    phone = '77054779047'
    data = {'from': 'Info', 'to': phone, 'text': 'text'}
    body = dto.SendSmsDto(**data)
    await SMSAdapter().send(body)


    return fastapi.responses.Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app',  host='0.0.0.0', port=1026, reload=True)
