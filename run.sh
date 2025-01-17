#!/bin/bash
crawl4ai-doctor
cd /app
fastapi run --workers 4 --host 0.0.0.0 --port 8000 api.py
