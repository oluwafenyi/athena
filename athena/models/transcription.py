from typing import List
from dataclasses import dataclass, asdict

from .speech_segment import SpeechSegment


@dataclass(frozen=True)
class Transcription:
    language: str
    speech_segments: List[SpeechSegment]

    def as_dict(self) -> dict:
        return asdict(self)
