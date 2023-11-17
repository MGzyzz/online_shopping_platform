import os

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from starlette import status
from dotenv import load_dotenv
import dto
from adapters import SMSAdapter


load_dotenv()
app = fastapi.FastAPI()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Item(Base):

    __tablename__ = 'accounts_user'
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/items/{item_id}')
async def read_item(item_id: int, db: Session = Depends(get_db)):

    query = text('SELECT id, phone FROM accounts_user WHERE id = :item_id')
    result = db.execute(query, {'item_id': item_id})
    item = result.fetchone()

    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')

    return {'id': item.id, "phone": item.phone}


@app.post('/sms/send')
async def send_sms(body: dto.SendSmsDto):
    await SMSAdapter().send(body)
    
    return fastapi.responses.Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app',  host='0.0.0.0', port=1026, reload=True)
