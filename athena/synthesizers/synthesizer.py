import abc

from models.transcription import Transcription


class Synthesizer(abc.ABC):
    """
    Synthesizes transcriptions to audio
    """
    @abc.abstractmethod
    def synthesize(self, transcription: Transcription, language: str) -> bytes:
        ...
