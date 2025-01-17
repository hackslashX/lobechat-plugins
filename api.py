from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import os
os.environ["SEARCH__SEARXNG_BASE_URL"] = "http://localhost:8081"

from backends.composite import CompositeBackend, InputSchema, SingleResult

app = FastAPI()

@app.post("/api/v1/search")
async def search(request: InputSchema) -> List[SingleResult]:
    composite_model = CompositeBackend()
    results = await composite_model.execute(request)
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3400)