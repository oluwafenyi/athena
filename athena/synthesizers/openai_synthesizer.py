from io import BytesIO
import os

from openai import OpenAI
from pydub import AudioSegment

from models.transcription import Transcription
from utils import load_audio_segment, join_audio_segments
from .synthesizer import Synthesizer


TEMP_DIRECTORY = "/Users/enyiomaosondu/personal/final-year-project/athena_media/temp"


class OpenAISynthesizer(Synthesizer):
    client: OpenAI

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def synthesize(self, transcription: Transcription, language: str) -> BytesIO:
        audio_segments = []
        last_end = 0

        for seg in transcription.speech_segments:
            print(seg.text)
            silence_duration = last_end - seg.start

            if (silence_duration > 0):
                audio_segments.append(AudioSegment.silent(duration=silence_duration*1000))

            last_end = seg.end
            temp_file_path = os.path.join(TEMP_DIRECTORY, f"synthesized-{seg.identifier}.mp3")

            response = self.client.audio.speech.create(
                model="tts-1-hd",
                voice="echo",
                input=seg.text,
                response_format="mp3",
            )
            response.write_to_file(temp_file_path)

            with open(temp_file_path, "rb") as f:
                fp = BytesIO(f.read())

            fp.seek(0)
            adjusted_fp = load_audio_segment(fp, format="mp3", fit_audio=True, audio_length=seg.end - seg.start)
            audio_segments.append(adjusted_fp)

        output_fp = BytesIO()
        final_audio = join_audio_segments(audio_segments)
        output_fp = final_audio.export(output_fp, format="mp3")
        output_fp.seek(0)
        return output_fp
