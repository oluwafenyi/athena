from io import BytesIO

import gtts
from pydub import AudioSegment

from models.transcription import Transcription
from utils import adjust_audio_playback_speed, join_audio_segments
from .synthesizer import Synthesizer


class GoogleTTSSynthesizer(Synthesizer):
    def synthesize(self, transcription: Transcription, language: str) -> BytesIO:
        audio_segments = []
        last_end = 0

        for seg in transcription.speech_segments:
            silence_duration = seg.start - last_end

            if (seg.start - last_end > 0):
                audio_segments.append(AudioSegment.silent(duration=silence_duration*1000))

            last_end = seg.end
            result = gtts.gTTS(seg.text, lang=language)
            fp = BytesIO()
            result.write_to_fp(fp)
            fp.seek(0)
            adjusted_fp = adjust_audio_playback_speed(fp, seg.end - seg.start, "mp3")
            audio_segments.append(adjusted_fp)

        output_fp = BytesIO()
        final_audio = join_audio_segments(audio_segments)
        output_fp = final_audio.export(output_fp, format="mp3")
        output_fp.seek(0)
        return output_fp
