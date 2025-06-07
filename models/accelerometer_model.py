from sqlalchemy import Column, Integer, Float, DateTime
from app.database import Base
from datetime import datetime

class AccelerometerData(Base):
    __tablename__ = "accelerometer_data"

    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)