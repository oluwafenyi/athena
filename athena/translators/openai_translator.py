import json

from openai import OpenAI

from models.transcription import Transcription, SpeechSegment
from .translator import Translator


class OpenAITranslator(Translator):
    client: OpenAI

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def translate(self, transcription: Transcription, target_language: str) -> Transcription:
        transcript_data = json.dumps(transcription.model_dump_json())
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that performs text translation, parses and generates JSON."},
                {"role": "user", "content": f"Translate the text properties in the following json object to language code: {target_language}. Ensure that the translation is brief enough to be said in given time segment"},
                {"role": "user", "content": transcript_data}
            ],
            response_format=Transcription
        )
        return response.choices[0].message.parsed

    def translate_text(self, source_text: str, target_language: str, source_language: str="auto") -> str:
        raise NotImplementedError()
