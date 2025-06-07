from sqlalchemy import Column, Integer, Float, DateTime
from app.database import Base
from datetime import datetime

class VoiceData(Base):
    __tablename__ = "voice_data"

    id = Column(Integer, primary_key=True, index=True)
    shimmer = Column(Float, nullable=False)
    jitter = Column(Float, nullable=False)
    pitch = Column(Float, nullable=False)
    vocab_richness = Column(Float, nullable=False)
    sentence_length = Column(Float, nullable=False)
    speech_rate = Column(Float, nullable= False)
    timestamp = Column(DateTime, default=datetime.utcnow)