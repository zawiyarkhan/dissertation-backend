from pydantic import BaseModel
from datetime import datetime


class VoiceCreate(BaseModel):
    shimmer: float
    jitter: float
    pitch: float
    vocab_richness: float
    sentence_length: float
    speech_rate: float
    timestamp: datetime


#   id = Column(Integer, primary_key=True, index=True)
#     shimmer = Column(Float, nullable=False)
#     jitter = Column(Float, nullable=False)
#     pitch = Column(Float, nullable=False)
#     vocab_richness = Column(Float, nullable=False)
#     sentence_length = Column(Float, nullable=False)
#     speech_rate = Column(Float, nullable= False)
#     timestamp = Column(DateTime, default=datetime.utcnow)