from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os


from app.models.voice_model import VoiceData
from app.services.voice_services import upload_voice
from app.schemas.voice_schema import VoiceCreate



router = APIRouter(prefix="/voice")

@router.post("/upload", response_model=VoiceCreate)
def upload_voice_route(voice_file: UploadFile = File(...)):
    return upload_voice(voice_file)
