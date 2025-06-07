from sqlalchemy.orm import Session
from app.models.accelerometer_model import AccelerometerData
from app.schemas.accelerometer_schema import AccelerometerCreate

def save_accelerometer_data(data: AccelerometerCreate, db: Session):
    db_data = AccelerometerData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return {"message": "Data stored", "id": db_data.id}
