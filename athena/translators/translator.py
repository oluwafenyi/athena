import abc

from models.transcription import Transcription


class Translator(abc.ABC):
    """
    Translates transcription to target language
    """
    @abc.abstractmethod
    def translate(self, transcription: Transcription, target_language: str) -> Transcription:
        ...

    """
    Translates text from source language to target language
    """
    @abc.abstractmethod
    def translate_text(self, source_text: str, target_language: str, source_language: str="auto") -> str:
        ...
