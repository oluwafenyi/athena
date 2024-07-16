
from deep_translator import GoogleTranslator as GTranslator

from models.speech_segment import SpeechSegment
from models.transcription import Transcription
from .translator import Translator


class GoogleTranslator(Translator):
    def translate(self, transcription: Transcription, target_language: str) -> Transcription:
        return Transcription(
            language=target_language,
            speech_segments=[SpeechSegment(
                identifier=segment.identifier,
                start=segment.start,
                end=segment.end,
                text=self.translate_text(segment.text, target_language=target_language, source_language=transcription.language)
            ) for segment in transcription.speech_segments]
        )

    def translate_text(self, source_text: str, target_language: str, source_language: str="auto") -> str:
        translated = GTranslator(source_language, target=target_language).translate(source_text)
        return translated
