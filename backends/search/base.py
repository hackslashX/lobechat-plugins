from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from .exceptions import InvalidEngineSettings


class BaseSearchBackendSettings(BaseSettings):
    pass


class SearchResult(BaseModel):
    title: str
    url: str
    content: str
    pretty_url: str
    # Optional fields
    date: Optional[datetime] = None
    favicon: Optional[str] = None
    engine: Optional[str] = None
    category: Optional[str] = None


class BaseSearchOutputSchema(BaseModel):
    query: str
    results: List[SearchResult]
    total_results: int
    page: int
    # Optional fields
    suggestions: Optional[List[str]] = None
    answers: Optional[List[str]] = None
    correction: Optional[str] = None
    thumbnail: Optional[str] = None


class BaseSearchRequestObject(BaseModel):
    query: str
    page: int = 1
    results: int = 10
    pagesize: int = 10
    language: str = "en"
    safesearch: int = 0
    format: str = "json"


class BaseSearchBackend(ABC):

    # Set schemas for accessibility
    configuration_schema = BaseSearchBackendSettings
    output_schema = BaseSearchOutputSchema


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
    def search(self, request: BaseSearchRequestObject) -> BaseSearchOutputSchema:
        """
        Execute the search based on the query and parameters, and return the results.
        :param request: The search request object containing the query and other parameters.
        :return: A list of results where each result conforms to output_schema
        """
        pass
