# main.py
from fastapi import FastAPI
from app.database import engine, Base
from app.api import register_routes

app = FastAPI()
Base.metadata.create_all(bind=engine)

register_routes(app)
