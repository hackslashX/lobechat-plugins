import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from .exceptions import InvalidEngineSettings


class BaseScrapeBackendSettings(BaseSettings):
    pass


class BaseScrapeOutputSchema(BaseModel):
    full_content: str


class BaseScrapeRequestObject(BaseModel):
    url: str


class BaseScrapeBackend(ABC):

    # Set schemas for accessibility
    configuration_schema = BaseScrapeBackendSettings
    output_schema = BaseScrapeOutputSchema


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
    async def scrape_single(self, request: BaseScrapeRequestObject) -> BaseScrapeOutputSchema:
        """
        Execute the scraping logic based on the provided request.
        :param request: An object conforming to input_schema
        :return: A result conforming to output_schema
        """
        pass

    async def scrape_multi(self, requests: List[BaseScrapeRequestObject]) -> List[BaseScrapeOutputSchema]:
        """
        Execute the scraping logic based on the provided request.
        :param request: An object conforming to input_schema
        :return: A result conforming to output_schema
        """
        return await asyncio.gather(*[self.scrape_single(request) for request in requests])
