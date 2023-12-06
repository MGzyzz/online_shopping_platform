import io

import fastapi
from starlette.responses import StreamingResponse

from xml_generate import Offers, generate_xml
from fastapi.middleware.cors import CORSMiddleware


app = fastapi.FastAPI()

origins = ['http://localhost']
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post('/generate_xml', response_class=StreamingResponse)
async def generate_xml_endpoint(product_data: Offers):
    xml_data = await generate_xml(product_data)
    return StreamingResponse(io.StringIO(xml_data), media_type='application/xml')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=5050, reload=True)
