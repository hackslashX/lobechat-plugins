from typing import List
from datetime import datetime
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from ..subtitles.ytdlp import YtDlpSubtitlesBackend, YtDlpSubtitlesInputRequest


# TODO: Make this dynamic to allow for easier extension


class SubtitlesInputSchema(BaseModel):
    url: str
    language: str = "en"
    format: str = "vtt"


class SubtitlesResult(BaseModel):
    title: str = ""
    channel: str = ""
    subtitles: str


class SubtitlesBackendConfig(BaseSettings):
    pass


class SubtitlesBackend:
    def __init__(self):
        self.params = SubtitlesBackendConfig()
        self.subtitles_backend = YtDlpSubtitlesBackend()

    async def execute(self, request: SubtitlesInputSchema) -> SubtitlesResult:
        subtitles_request = YtDlpSubtitlesInputRequest(url=request.url, language=request.language, format=request.format)
        subtitles_results = self.subtitles_backend.extract_subtitles(subtitles_request)
        return SubtitlesResult(
            title=subtitles_results.title,
            channel=subtitles_results.channel,
            subtitles=subtitles_results.subtitles
        )