
from dotenv import load_dotenv

from audio_extractor import AudioExtractor
from transcribers.whisper_transcriber import WhisperTranscriber
from translators.google_translator import GoogleTranslator
from synthesizers.google_tts_synthesizer import GoogleTTSSynthesizer


if __name__ == "__main__":
    load_dotenv()

    # extractor = AudioExtractor(video_path="/Users/enyiomaosondu/personal/final-year-project/motivation.mp4")
    # audio = extractor.extract()
    # with open("/Users/enyiomaosondu/personal/final-year-project/sample.wav", "wb") as f:
    #     f.write(audio)

    transcriber = WhisperTranscriber()
    translator = GoogleTranslator()
    synthesizer = GoogleTTSSynthesizer()
    # transcription = transcriber.transcribe(None, "en")
    # translated_transcription = translator.translate(transcription, "fr")

    translated_transcription = None

    import pickle
    with open("/Users/enyiomaosondu/personal/final-year-project/transcription.pkl", "rb") as f:
        translated_transcription = pickle.load(f)

    ...
    audio_fp = synthesizer.synthesize(translated_transcription, translated_transcription.language)
    with open("/Users/enyiomaosondu/personal/final-year-project/output.mp3", "wb") as f:
        f.write(audio_fp.getbuffer())
