from fastapi import FastAPI
from app.routes.accelerometer.acc_routes import router as acc_routes
from app.routes.auth.auth_routes import router as auth_routes
from app.routes.voice.voice_routes import router as voice_routes


def register_routes(app:FastAPI):
    app.include_router(acc_routes)
    app.include_router(voice_routes)
    app.include_router(auth_routes)