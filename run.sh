#!/bin/bash
crawl4ai-doctor
cd /app
mkdir -p /app/.temp
fastapi run --workers 4 --host 0.0.0.0 --port 3400 api.py
