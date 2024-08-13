from dataclasses import dataclass, asdict


@dataclass
class SpeechSegment:
    identifier: int
    start: float
    end: float
    text: str

    def as_dict(self) -> dict:
        return asdict(self)
