from dataclasses import dataclass


@dataclass
class SpeechSegment:
    identifier: int
    start: float
    end: float
    text: str
