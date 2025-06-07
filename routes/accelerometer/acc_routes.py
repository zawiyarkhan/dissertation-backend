from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.accelerometer_schema import AccelerometerCreate
from app.services.accelerometer_services import save_accelerometer_data
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/accelerometer")
def create_accelerometer_data(data: AccelerometerCreate, db: Session = Depends(get_db)):
    return save_accelerometer_data(data, db)
