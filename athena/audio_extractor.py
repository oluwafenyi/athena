
import ffmpeg


# TODO: extractor instance should be re-usable

class AudioExtractor:
    def _load_video(self, video_path: str) -> bytes:
        with open(video_path, "rb") as f:
            return f.read()

    """
    Returns an audio stream in wav format.
    """
    def extract(self, video_path_or_video_stream: bytes | str) -> bytes:
        if isinstance(video_path_or_video_stream, str):
            video_path_or_video_stream = self._load_video(video_path=video_path_or_video_stream)

        process = ffmpeg.input("pipe:").output(
            "pipe:",
            format='wav',
            acodec='pcm_s16le',
            ac=1,
            ar=44100,
        ).overwrite_output().\
            run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
        audio, _ = process.communicate(input=video_path_or_video_stream)
        return audio
