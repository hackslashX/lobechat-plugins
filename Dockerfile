FROM python:3.11-slim

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN crawl4ai-setup
RUN crawl4ai-doctor
RUN playwright install --with-deps

# Copy the source code
WORKDIR /app
COPY backends /app/backends
COPY api.py /app/api.py

# Run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]