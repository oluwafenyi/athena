
from deep_translator import GoogleTranslator as GTranslator

from models.speech_segment import SpeechSegment
from models.transcription import Transcription
from utils import rephrase_sentence
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


class GoogleTranslatorWithRephrasing(GoogleTranslator):
    def translate(self, transcription: Transcription, target_language: str) -> Transcription:
        translated_transcription = Transcription(language=target_language, speech_segments=[])
        for segment in transcription.speech_segments:
            translated_text = self.translate_text(segment.text, target_language=target_language, source_language=transcription.language)
            translated_segment = SpeechSegment(
                identifier=segment.identifier,
                start=segment.start,
                end=segment.end,
                text=translated_text
            )

            articulation_score = self._compute_articulation_score(translated_segment)

            if (articulation_score > 2.5):
                translated_text = rephrase_sentence(translated_text)
                translated_segment.text = translated_text

            translated_transcription.speech_segments.append(translated_segment)

        return translated_transcription

    def _compute_articulation_score(self, segment: SpeechSegment) -> float:
        duration = segment.end - segment.start
        word_count = len(segment.text.split())
        return word_count/duration
