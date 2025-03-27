
from pydantic import BaseModel


class SpeechSegment(BaseModel):
    identifier: int
    start: float
    end: float
    text: str
