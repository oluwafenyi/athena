
import gtts

from models.transcription import Transcription
from .synthesizer import Synthesizer


class GoogleTTSSynthesizer(Synthesizer):

    def synthesize(self, transcription: Transcription, language: str) -> bytes:
        for seg in transcription.speech_segments:
            result = gtts.gTTS(seg.text, lang=language)
            result.save(f"/Users/enyiomaosondu/personal/final-year-project/generated-{seg.identifier}.mp3")
