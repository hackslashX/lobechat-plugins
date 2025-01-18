FROM python:3.11-slim

WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry

# Set poetry to not use a virtualenv
RUN poetry config virtualenvs.create false

# Install dependencies
COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock
RUN poetry install --no-dev

# Set up playwright and crawl4ai
RUN crawl4ai-setup
RUN playwright install --with-deps

# Copy the source code
COPY backends /app/backends
COPY api.py /app/api.py
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

# Run the application
CMD ["/app/run.sh"]