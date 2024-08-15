
from dotenv import load_dotenv

from audio_extractor import AudioExtractor
from transcribers.whisper_transcriber import WhisperTranscriber
from translators.google_translator import GoogleTranslator, GoogleTranslatorWithRephrasing
from synthesizers.google_tts_synthesizer import GoogleTTSSynthesizer
from audio_video_synchronizer import AudioVideoSynchronizer

from utils import load_transcription, store_transcription


if __name__ == "__main__":
    load_dotenv()

    # extractor = AudioExtractor(video_path="/Users/enyiomaosondu/personal/final-year-project/motivation.mp4")
    # audio = extractor.extract()
    # with open("/Users/enyiomaosondu/personal/final-year-project/sample.wav", "wb") as f:
    #     f.write(audio)

    transcriber = WhisperTranscriber()
    translator = GoogleTranslatorWithRephrasing()
    synthesizer = GoogleTTSSynthesizer()
    synchronizer = AudioVideoSynchronizer()

    # transcription = transcriber.transcribe("/Users/enyiomaosondu/personal/final-year-project/sample.wav", "en")
    # store_transcription(transcription, "/Users/enyiomaosondu/personal/final-year-project/transcription-untranslated.pkl")

    # transcription = load_transcription("/Users/enyiomaosondu/personal/final-year-project/transcription-untranslated.pkl")
    # translated_transcription = translator.translate(transcription, "fr")

    translated_transcription = None

    import pickle
    with open("/Users/enyiomaosondu/personal/final-year-project/transcription-translated-rephrased.pkl", "rb") as f:
        translated_transcription = pickle.load(f)

    # store_transcription(translated_transcription, "/Users/enyiomaosondu/personal/final-year-project/transcription-translated-rephrased.pkl")

    # ...
    audio_fp = synthesizer.synthesize(translated_transcription, translated_transcription.language)
    with open("/Users/enyiomaosondu/personal/final-year-project/output.mp3", "wb") as f:
        f.write(audio_fp.getbuffer())

    # synchronizer.merge_audio_with_video(video_path="/Users/enyiomaosondu/personal/final-year-project/motivation.mp4", audio_path="/Users/enyiomaosondu/personal/final-year-project/output.mp3", result_path="/Users/enyiomaosondu/personal/final-year-project/final-video.mp4")
