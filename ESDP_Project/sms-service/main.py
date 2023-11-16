import fastapi
from starlette import status

import dto
from adapters import SMSAdapter


app = fastapi.FastAPI()


@app.post('/sms/send')
async def send_sms(body: dto.SendSmsDto):
    await SMSAdapter().send(body)
    
    return fastapi.responses.Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run('main:app', host='0.0.0.0', port=1026, reload=True)
