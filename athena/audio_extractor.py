
import ffmpeg


class AudioExtractor:
    video_stream: bytes

    def __init__(self, *, video_path : str = None, video_stream: bytes = None) -> None:
        if video_path:
            self.video_stream = self._load_video(video_path=video_path)
        else:
            self.video_stream = video_stream

    def _load_video(self, video_path: str) -> bytes:
        with open(video_path, "rb") as f:
            return f.read()

    """
    Returns an audio stream in wav format.
    """
    def extract(self) -> bytes:
        process = ffmpeg.input("pipe:").output(
            "pipe:",
            format='wav',
            acodec='pcm_s16le',
            ac=1,
            ar=44100,
        ).overwrite_output().\
            run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
        audio, _ = process.communicate(input=self.video_stream)
        return audio
