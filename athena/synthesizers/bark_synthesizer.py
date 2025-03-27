from io import BytesIO
import os

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from pydub import AudioSegment

from models.transcription import Transcription
from utils import load_audio_segment, join_audio_segments
from .synthesizer import Synthesizer


# https://huggingface.co/blog/optimizing-bark
# https://github.com/suno-ai/bark/pull/447/files
TEMP_DIRECTORY = "/Users/enyiomaosondu/personal/final-year-project/athena_media/temp"

PREFERRED_VOICE_MODELS = [
    { "id": 1, "language": "English", "code": "en", "speaker": "v2/en_speaker_6", "name": "Suno Favorite" },
    { "id": 2, "language": "Chinese (Simplified)", "code": "zh", "speaker": "v2/zh_speaker_0", "name": "Male" },
    { "id": 3, "language": "French", "code": "fr", "speaker": "v2/fr_speaker_3", "name": "Male" },
    { "id": 4, "language": "German", "code": "de", "speaker": "v2/de_speaker_0", "name": "Male" },
    { "id": 5, "language": "Hindi", "code": "hi", "speaker": "v2/hi_speaker_2", "name": "Male" },
    { "id": 6, "language": "Italian", "code": "it", "speaker": "v2/it_speaker_4", "name": "Suno Favorite" },
    { "id": 7, "language": "Japanese", "code": "ja", "speaker": "v2/ja_speaker_2", "name": "Male" },
    { "id": 8, "language": "Korean", "code": "ko", "speaker": "v2/ko_speaker_1", "name": "Male" },
    { "id": 9, "language": "Polish", "code": "pl", "speaker": "v2/pl_speaker_0", "name": "Male" },
    { "id": 10, "language": "Portuguese", "code": "pt", "speaker": "v2/pt_speaker_0", "name": "Male" },
    { "id": 11, "language": "Russian", "code": "ru", "speaker": "v2/ru_speaker_0", "name": "Male" },
    { "id": 12, "language": "Spanish", "code": "es", "speaker": "v2/es_speaker_0", "name": "Male" },
    { "id": 13, "language": "Turkish", "code": "tr", "speaker": "v2/tr_speaker_0", "name": "Male" }
]


class BarkSynthesizer(Synthesizer):

    def __init__(self):
        preload_models()

    def synthesize(self, transcription: Transcription, language: str) -> BytesIO:
        audio_segments = []
        last_end = 0

        voice_model = [v for v in PREFERRED_VOICE_MODELS if v["code"] == language][0]["speaker"]

        for seg in transcription.speech_segments:
            print(seg.text)
            silence_duration = last_end - seg.start

            if (silence_duration > 0):
                audio_segments.append(AudioSegment.silent(duration=silence_duration*1000))

            last_end = seg.end

            # generate audio from text
            fp = BytesIO()
            audio_array = generate_audio(seg.text, history_prompt=voice_model, max_gen_duration_s=seg.end - seg.start)
            write_wav(fp, SAMPLE_RATE, audio_array)
            fp.seek(0)
            adjusted_fp = load_audio_segment(fp, format="wav", fit_audio=False, audio_length=seg.end - seg.start)
            audio_segments.append(adjusted_fp)

        output_fp = BytesIO()
        final_audio = join_audio_segments(audio_segments)
        output_fp = final_audio.export(output_fp, format="mp3")
        output_fp.seek(0)
        return output_fp
