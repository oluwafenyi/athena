from io import BytesIO
from typing import List

from pydub import AudioSegment
from pydub.effects import speedup


def adjust_audio_playback_speed(fp: BytesIO, desired_length: float, format: str = "mp3") -> AudioSegment:
    audio = AudioSegment.from_file(fp, format=format)
    duration = audio.duration_seconds
    speed = duration / desired_length
    new_audio = speedup(audio, speed)
    return new_audio


def join_audio_segments(segments: List[AudioSegment]) -> AudioSegment:
    final_audio = AudioSegment.empty()

    for seg in segments:
        final_audio += seg

    return final_audio
