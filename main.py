# main.py
from fastapi import FastAPI
from app.routes import router as api_router
from app.database import engine, Base
from app.models import user

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(api_router)