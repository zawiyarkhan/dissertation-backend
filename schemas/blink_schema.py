from pydantic import BaseModel
from typing import List

class BlinkDetectionResponse(BaseModel):
    blink_count: int
    blink_timestamps: List[float]
    video_duration_seconds: float
    blink_rate_per_minute: float
