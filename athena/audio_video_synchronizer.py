from io import BytesIO

import ffmpeg


class AudioVideoSynchronizer:
    # Todo: handle in-memory
    def merge_audio_with_video(self, video_path: str, audio_path: str):
        input_video = ffmpeg.input(video_path)
        input_audio = ffmpeg.input(audio_path)
        ffmpeg.concat(input_video, input_audio, v=1, a=1).output("/Users/enyiomaosondu/personal/final-year-project/final-video.mp4").run()
