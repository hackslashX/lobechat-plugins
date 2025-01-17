import requests
from .base import BaseSearchBackend, BaseSearchBackendSettings, BaseSearchOutputSchema, BaseSearchRequestObject, SearchResult
from .exceptions import ErrorInEngine

class SearXNGBaseSettings(BaseSearchBackendSettings):
    SEARCH__SEARXNG_BASE_URL: str
    

class SearXNGSearchBackend(BaseSearchBackend):

    # Override the configuration schema
    configuration_schema = SearXNGBaseSettings

    # Add type hints for the parameters
    params: SearXNGBaseSettings

    def search(self, request: BaseSearchRequestObject) -> BaseSearchOutputSchema:
        try:
            # Extract supported parameters from the request object
            request_params = {
                "q": request.query,
                "pageno": request.page,
                "format": request.format,
                "language": request.language,
                "safesearch": request.safesearch,
            }

            # Make the request to the SearXNG API
            with requests.get(
                f"{self.params.SEARCH__SEARXNG_BASE_URL}",
                params=request_params,
            ) as response:
                # Format the response to the expected output schema
                response = response.json()
                search_results = []
                if response.get("results"):
                    for result in response["results"]:
                        search_results.append(
                            SearchResult(
                                title=result.get("title"),
                                url=result.get("url"),
                                content=result.get("content"),
                                pretty_url=result.get("url"),
                                engine=result.get("engine"),
                                date=result.get("publishedDate"),
                                thumbnail=result.get("thumbnail"),
                                favicon=result.get("favicon"),
                                category=result.get("category"),
                            )
                        )
                result_object = BaseSearchOutputSchema(
                    query=request.query,
                    results=search_results,
                    total_results=response.get("number_of_results"),
                    page=request.page
                )
                return result_object
        except Exception as e:
            raise ErrorInEngine(class_name=self.__class__.__name__, error=e)