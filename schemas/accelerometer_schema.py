from pydantic import BaseModel
from datetime import datetime

class AccelerometerCreate(BaseModel):
    x: float
    y: float
    z: float
    timestamp: datetime
