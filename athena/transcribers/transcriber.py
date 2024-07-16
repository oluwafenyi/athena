import abc

from models.transcription import Transcription


class Transcriber(abc.ABC):
    """
    Transcribes audio in source language to English text
    """
    @abc.abstractmethod
    def transcribe(self, audio_stream:bytes, source_language: str) -> Transcription:
        ...
