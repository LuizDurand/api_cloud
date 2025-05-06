# app/app.py
from fastapi import FastAPI
from app.routers import routs as app_router

app = FastAPI()
app.include_router(app_router.router)
