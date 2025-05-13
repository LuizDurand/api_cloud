# app/app.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.routers import routs as app_router

# Cria tabelas automaticamente
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
app.include_router(app_router.router)
