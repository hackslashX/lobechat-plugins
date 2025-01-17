#!/bin/bash
crawl4ai-doctor
cd /app
uvicorn api:app --host 0.0.0.0 --port 8000
