# Dockerfile for RAG Pipeline API
# Use official Python slim image
FROM python:3.13-slim

# Default environment variables (override via `--env` or .env)
ENV DEFAULT_EMBEDDING_MODEL=all-mpnet-base-v2
ENV DEFAULT_SUMMARIZER_MODEL=facebook/bart-large-cnn
ENV APP_HOST=0.0.0.0
ENV APP_PORT=8000
ENV LOG_LEVEL=info

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Expose application port
EXPOSE ${APP_PORT}

# Launch the API with environment-driven configuration
CMD uvicorn main:app --host $APP_HOST --port $APP_PORT --log-level $LOG_LEVEL