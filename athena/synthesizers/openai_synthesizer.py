
from openai import OpenAI

from models.transcription import Transcription
from .synthesizer import Synthesizer


class OpenAISynthesizer(Synthesizer):
    client: OpenAI

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def synthesize(self, transcription: Transcription, language: str) -> bytes:
        for seg in transcription.speech_segments:
            response = self.client.audio.speech.create(
                model="tts-1-hd",
                voice="alloy",
                input=seg.text,
                response_format="wav",
            )
            response.write_to_file(f"/Users/enyiomaosondu/personal/final-year-project/generated-{seg.identifier}.wav")
