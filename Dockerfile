FROM python:3.11-slim

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN crawl4ai-setup
RUN playwright install --with-deps

# Copy the source code
WORKDIR /app
COPY backends /app/backends
COPY api.py /app/api.py
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

# Run the application
CMD ["/app/run.sh"]