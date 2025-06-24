from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import json

class BlinkDetection(Base):
    __tablename__ = "blink_detections"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    blink_count = Column(Integer)
    blink_rate_per_minute = Column(Float)
    video_duration_seconds = Column(Float)
    blink_timestamps_json = Column(String)  # Store timestamps as JSON string

    def set_timestamps(self, timestamps: list):
        self.blink_timestamps_json = json.dumps(timestamps)

    def get_timestamps(self) -> list:
        return json.loads(self.blink_timestamps_json or "[]")
