import yt_dlp
from typing import List, Any
from abc import ABC, abstractmethod
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from .exceptions import InvalidEngineSettings


class BaseSubtitlesInputRequest(BaseModel):
    url: str
    language: str = "en"
    format: str = "vtt"


class BaseSubtitlesOutputSchema(BaseModel):
    subtitles: str


class BaseSubtitlesBackendSettings(BaseSettings):
    pass


class BaseSubtitlesBackend(ABC):

    # Set schemas for accessibility
    configuration_schema = BaseSubtitlesBackendSettings
    output_schema = BaseSubtitlesOutputSchema


    def __init__(self, **params: Any) -> None:
        self.params = params
        self.validate_params()

    def validate_params(self) -> None:
        # Implement schema validation logic based on param_schema
        try:
            self.params = self.configuration_schema(**self.params)
        except Exception as e:
            raise InvalidEngineSettings(class_name=self.__class__.__name__, error=e)

    @abstractmethod
    def extract_subtitles(self, request: BaseSubtitlesInputRequest) -> BaseSubtitlesOutputSchema:
        """
        Execute the subtitles extraction logic based on the provided request.
        :param request: An object conforming to input_schema
        :return: A result conforming to output_schema
        """
        pass
