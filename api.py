from typing import List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from backends.composite.search_scrape import SearchScrapeBackend, SearchScrapeInputSchema, SearchScapeResult
from backends.composite.subtitles import SubtitlesBackend, SubtitlesInputSchema, SubtitlesResult

app = FastAPI()

@app.post("/api/v1/search")
async def search(query: str) -> List[SearchScapeResult]:
    request = SearchScrapeInputSchema(query=query)
    composite_model = SearchScrapeBackend()
    results = await composite_model.execute(request)
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