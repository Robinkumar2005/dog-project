from pydantic import BaseModel
from typing import Optional

class PredictionResult(BaseModel):
    breed: str
    confidence: float
    dog_info: Optional[dict]
    processing_time: float

