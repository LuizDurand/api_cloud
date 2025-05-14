# app/app.py
import time
from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
from app.core.database import engine, Base
from app.routers.routs import router as app_router

app = FastAPI()
app.include_router(app_router)

@app.on_event("startup")
def on_startup():
    # tenta conectar até 5 vezes, esperando 2s entre cada
    for i in range(5):
        try:
            conn = engine.connect()
            conn.close()
            break
        except OperationalError:
            time.sleep(2)
    # só então cria as tabelas
    Base.metadata.create_all(bind=engine)
