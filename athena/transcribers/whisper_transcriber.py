from typing import List, Dict

import whisper
import numpy as np

from models.speech_segment import SpeechSegment
from models.transcription import Transcription
from .transcriber import Transcriber


class WhisperTranscriber(Transcriber):
    _model: whisper.Whisper

    def __init__(self) -> None:
        self._model = whisper.load_model("medium")

    def _load_transcription(self, data: List[Dict], language: str) -> Transcription:
        if data is None:
            return Transcription()

        return Transcription(
            language=language,
            speech_segments=[
            SpeechSegment(
                identifier=i+1,
                start=segment["start"],
                end=segment["end"],
                text=segment["text"],
            ) for i, segment in enumerate(data)
        ])


    def transcribe(self, audio_stream: bytes, source_language: str) -> Transcription:
        # audio_array = np.frombuffer(audio_stream, np.int16).flatten().astype(np.float32) / 32768.0
        results = self._model.transcribe("/Users/enyiomaosondu/personal/final-year-project/sample.wav")
        transcription = self._load_transcription(results.get("segments"), results.get("language"))
        return transcription
