from typing import List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from backends.composite import CompositeBackend, InputSchema, SingleResult

app = FastAPI()

@app.post("/api/v1/search")
async def search(query: str) -> List[SingleResult]:
    request = InputSchema(query=query)
    composite_model = CompositeBackend()
    results = await composite_model.execute(request)
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3400)