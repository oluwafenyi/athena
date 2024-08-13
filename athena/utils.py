import os
import pickle
from io import BytesIO
from typing import List
import time

from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.effects import speedup
from hugchat import hugchat
from hugchat.login import Login

from models.transcription import Transcription


load_dotenv()
cookie_path_dir = "/Users/enyiomaosondu/personal/final-year-project/cookies/"
sign = Login(os.getenv("HUGGING_FACE_USERNAME"), os.getenv("HUGGING_FACE_PASSWORD"))
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())


def load_audio_segment(fp: BytesIO, format: str = "mp3", fit_audio: bool = False, audio_length: float = 0) -> AudioSegment:
    if fit_audio:
        return adjust_audio_playback_speed(fp, audio_length, format)
    return AudioSegment.from_file(fp, format=format)


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


def rephrase_sentence(text: str) -> str:
    for _ in range(20):
        try:
            message_result = chatbot.chat(f'Rephrase this to be shorter and give me only the result: {text}').wait_until_done()
            print(f"Rephrased: {text} -> {message_result}")
            return message_result
        except Exception as e:
            # print(f"An error occurred when translating '{text}':", e)
            time.sleep(8)


def store_transcription(transcription: Transcription, path: str):
    with open(path, "wb") as f:
        pickle.dump(transcription, f)


def load_transcription(path: str) -> Transcription:
    with open(path, "rb") as f:
        return pickle.load(f)
