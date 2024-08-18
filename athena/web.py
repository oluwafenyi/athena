import os
import datetime
import aiofiles
import uuid
from typing import Annotated

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from audio_extractor import AudioExtractor
from transcribers.whisper_transcriber import WhisperTranscriber
from translators.google_translator import GoogleTranslatorWithRephrasing
from synthesizers.google_tts_synthesizer import GoogleTTSSynthesizer
from audio_video_synchronizer import AudioVideoSynchronizer
from utils import watermark_video


TEMP_DIRECTORY = "/Users/enyiomaosondu/personal/final-year-project/athena_media/temp"
INPUT_DIRECTORY_PATH = "/Users/enyiomaosondu/personal/final-year-project/athena_media/inputs"
OUTPUT_DIRECTORY_PATH = "/Users/enyiomaosondu/personal/final-year-project/athena_media/outputs"

extractor = AudioExtractor()
transcriber = WhisperTranscriber()
translator = GoogleTranslatorWithRephrasing()
synthesizer = GoogleTTSSynthesizer()
synchronizer = AudioVideoSynchronizer()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranslationPayload(BaseModel):
    video_file: Annotated[UploadFile, File(description="video file to be translated")]
    source_language_code: str = Field(..., max_length=2)
    target_language_code: str = Field(..., max_length=2)


def process_translation(video_path, source_language, target_language) -> str:
    source_audio = extractor.extract(video_path)
    temp_source_audio_file_path = os.path.join(TEMP_DIRECTORY, f"{uuid.uuid4()}.wav")
    with open(temp_source_audio_file_path, "wb") as f:
        f.write(source_audio)

    source_transcription = transcriber.transcribe(temp_source_audio_file_path, source_language=source_language)
    translated_transcription = translator.translate(source_transcription, target_language=target_language)
    print(translated_transcription.as_dict())
    target_audio_fp = synthesizer.synthesize(translated_transcription, translated_transcription.language)
    temp_target_audio_file_path = os.path.join(TEMP_DIRECTORY, f"{uuid.uuid4()}.mp3")
    with open(temp_target_audio_file_path, "wb") as f:
        f.write(target_audio_fp.getbuffer())

    result_path = os.path.join(OUTPUT_DIRECTORY_PATH, os.path.basename(video_path))
    synchronizer.merge_audio_with_video(video_path=video_path, audio_path=temp_target_audio_file_path, result_path=result_path)
    os.unlink(temp_source_audio_file_path)
    os.unlink(temp_target_audio_file_path)
    watermark_video(result_path)
    return result_path


@app.post("/translate/", description="Translates input video in source language to target language", response_class=FileResponse)
async def translate(video_file: UploadFile = Form(...), source_language_code: str = Form(...), target_language_code: str = Form(...)) -> FileResponse:
    payload = TranslationPayload(video_file=video_file, source_language_code=source_language_code, target_language_code=target_language_code)
    file_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{payload.video_file.filename}"

    input_path = os.path.join(INPUT_DIRECTORY_PATH, file_name)
    async with aiofiles.open(input_path, "wb") as f:
        while content := await payload.video_file.read(1024):
            await f.write(content)

    output_path = process_translation(input_path, source_language_code, target_language_code)
    file_name = os.path.basename(output_path)
    headers = {"Access-Control-Expose-Headers": "Content-Disposition"}
    return FileResponse(output_path, filename=file_name, headers=headers)


if __name__ == "__main__":
    uvicorn.run("web:app", port=8000)
