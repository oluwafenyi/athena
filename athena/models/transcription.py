from typing import List
from dataclasses import dataclass

from .speech_segment import SpeechSegment


@dataclass(frozen=True)
class Transcription:
    language: str
    speech_segments: List[SpeechSegment]
