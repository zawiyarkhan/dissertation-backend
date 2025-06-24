from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse



from app.models.blinkmodel import BlinkDetection
from app.services.blinkrateCounter_services import detect_blinks
from app.schemas.blink_schema import BlinkDetectionResponse



router = APIRouter(prefix="/blink")

@router.post("/upload", response_model=BlinkDetectionResponse)
def upload_voice_route(blink_file: UploadFile = File(...)):
    return detect_blinks(blink_file)