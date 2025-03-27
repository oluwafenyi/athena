from typing import List

from pydantic import BaseModel

from .speech_segment import SpeechSegment


class Transcription(BaseModel):
    language: str
    speech_segments: List[SpeechSegment]
