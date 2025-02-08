import dotenv
try:
    dotenv.load_dotenv()
except:
    pass

from typing import List
from fastapi import FastAPI

from backends.composite.search_scrape import SearchScrapeBackend, SearchScrapeInputSchema, SearchScapeResult
from backends.composite.subtitles import SubtitlesBackend, SubtitlesInputSchema, SubtitlesResult
from backends.search.searxng import SearXNGSearchBackend, SearXNGInputSchema, SearXNGOutputSchema
from backends.scrape.crawl4_ai import Crawl4AIScrapeBackend, Crawl4AiInputSchema, Crawl4AiOutputSchema

app = FastAPI()

@app.post("/api/v1/search")
async def search(query: str) -> List[SearchScapeResult]:
    request = SearchScrapeInputSchema(query=query)
    composite_model = SearchScrapeBackend()
    results = await composite_model.execute(request)
    return results


@app.post("/api/v1/search/searxng")
async def search_searxng(query: str) -> SearXNGOutputSchema:
    request = SearXNGInputSchema(query=query)
    single_model = SearXNGSearchBackend()
    results = single_model.search(request)
    return results


@app.post("/api/v1/scrape/crawl4ai")
async def scrape_crawl4ai(url: str) -> Crawl4AiOutputSchema:
    request = Crawl4AiInputSchema(url=url)
    single_model = Crawl4AIScrapeBackend()
    results = await single_model.scrape_single(request)
    return results


@app.post("/api/v1/subtitles")
async def subtitles(url: str, language: str = "en", format: str = "vtt") -> SubtitlesResult:
    request = SubtitlesInputSchema(url=url, language=language, format="vtt")
    composite_model = SubtitlesBackend()
    results = await composite_model.execute(request)
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3400)