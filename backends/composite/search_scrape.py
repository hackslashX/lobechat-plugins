from typing import List
from datetime import datetime
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from ..search.searxng import SearXNGSearchBackend, BaseSearchRequestObject
from ..scrape.crawl4_ai import Crawl4AIScrapeBackend


# TODO: Make this dynamic to allow for easier extension


class SearchScrapeInputSchema(BaseModel):
    query: str


class SearchScapeResult(BaseModel):
    title: str
    url: str
    content: str
    full_content: str
    date: datetime | None = None


class SearchScrapeBackendConfig(BaseSettings):
    COMPOSITE__USE_SCRAPING: bool = True
    COMPOSITE__SCRAPING_RESULTS_LIMIT: int = 5
    COMPOSITE__FINAL_RESULTS_LIMIT: int = 5


class SearchScrapeBackend:
    def __init__(self):
        self.params = SearchScrapeBackendConfig()
        self.search_backend = SearXNGSearchBackend()
        self.scrape_backend = Crawl4AIScrapeBackend()

    async def execute(self, request: SearchScrapeInputSchema) -> List[SearchScapeResult]:
        search_request = BaseSearchRequestObject(query=request.query)
        search_results = self.search_backend.search(search_request)
        
        # Limit scraping to first three results only for now
        if self.params.COMPOSITE__USE_SCRAPING:
            scrape_request = search_results.results[:self.params.COMPOSITE__SCRAPING_RESULTS_LIMIT]
            scrape_results = await self.scrape_backend.scrape_multi(scrape_request)

        results = []
        # Add the remaning search results to the list
        for i, search_result in enumerate(search_results.results):
            if self.params.COMPOSITE__USE_SCRAPING and i < self.params.COMPOSITE__SCRAPING_RESULTS_LIMIT:
                full_content = scrape_results[i].full_content
            else:
                full_content = ""
            results.append(
                SearchScapeResult(
                    title=search_result.title,
                    url=search_result.url,
                    content=search_result.content,
                    full_content=full_content,
                    date=search_result.date
                )
            )

        return results[:self.params.COMPOSITE__FINAL_RESULTS_LIMIT]