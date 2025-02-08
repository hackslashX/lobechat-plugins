from typing import Optional, List
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai import AsyncWebCrawler, CacheMode, BrowserConfig, CrawlerRunConfig, CacheMode

from .base import BaseScrapeBackend, BaseScrapeRequestObject, BaseScrapeOutputSchema, BaseScrapeBackendSettings
from .exceptions import InvalidEngineSettings


class Crawl4AiOutputSchema(BaseScrapeOutputSchema):
    pass


class Crawl4AiInputSchema(BaseScrapeRequestObject):
    pass


class Crawl4AIBackendSettings(BaseScrapeBackendSettings):
    CRAWL4AI__IGNORE_LINKS: bool = True
    CRAWL4AI__EXCLUDE_TAGS: List[str] = ["nav", "footer", "aside"]
    CRAWL4AI__REMOVE_OVERLAY_ELEMENTS: bool = True
    CRAWL4AI__PRUNING_CONTENT_FILTER_THRESHOLD: Optional[float] = 0.48
    CRAWL4AI__PRUNING_CONTENT_FILTER_THRESHOLD_TYPE: Optional[str] = "fixed"
    CRAWL4AI__PRUNING_CONTENT_FILTER_MIN_WORD_THRESHOLD: Optional[int] = 0
    CRAWL4AI__MAXIMUM_CONTENT_LENGTH: Optional[int] = 0


class Crawl4AIScrapeBackend(BaseScrapeBackend):

    configuration_schema = Crawl4AIBackendSettings
    params: Crawl4AIBackendSettings

    async def scrape_single(self, request: BaseScrapeRequestObject) -> BaseScrapeOutputSchema:

        config = CrawlerRunConfig(
            cache_mode=CacheMode.ENABLED,
            excluded_tags=self.params.CRAWL4AI__EXCLUDE_TAGS,
            remove_overlay_elements=self.params.CRAWL4AI__REMOVE_OVERLAY_ELEMENTS,
            markdown_generator=DefaultMarkdownGenerator(
                content_filter=PruningContentFilter(
                    threshold=self.params.CRAWL4AI__PRUNING_CONTENT_FILTER_THRESHOLD,
                    threshold_type=self.params.CRAWL4AI__PRUNING_CONTENT_FILTER_THRESHOLD_TYPE,
                    min_word_threshold=self.params.CRAWL4AI__PRUNING_CONTENT_FILTER_MIN_WORD_THRESHOLD,
                ),
                options={
                    "ignore_links": self.params.CRAWL4AI__IGNORE_LINKS,
                }
            ),
        )
        
        try:
            async with AsyncWebCrawler(verbose=False) as crawler:
                result = await crawler.arun(
                    url=request.url,
                    config=config,
                )
            return BaseScrapeOutputSchema(full_content=result.markdown_v2.fit_markdown)
        except Exception as e:
            raise InvalidEngineSettings(class_name=self.__class__.__name__, error=e)
