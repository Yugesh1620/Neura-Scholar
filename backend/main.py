# app.py (updated to use environment-based config)
import os
import asyncio
import logging
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic_settings import BaseSettings
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# ---------------------------
# Configuration via environment
# ---------------------------

class Settings(BaseSettings):
    DEFAULT_EMBEDDING_MODEL: str = "all-mpnet-base-v2"
    DEFAULT_SUMMARIZER_MODEL: str = "facebook/bart-large-cnn"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Load settings once
settings = Settings()

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

# Initialize FastAPI
app = FastAPI(title="RAG Pipeline API with CRUD and Embedding", version="0.3")
Instrumentator().instrument(app).expose(app, include_in_schema=False, endpoint="/metrics")

# ---------------------------
# Model utilities using settings
# ---------------------------

# Override default model names with configured values
DEFAULT_EMBEDDING_MODEL = settings.DEFAULT_EMBEDDING_MODEL
DEFAULT_SUMMARIZER_MODEL = settings.DEFAULT_SUMMARIZER_MODEL

embedding_model_cache = {}
def load_embedding_model(model_name: str) -> SentenceTransformer:
    model_name = model_name or DEFAULT_EMBEDDING_MODEL
    if model_name in embedding_model_cache:
        logging.info("Model '%s' loaded from cache", model_name)
        return embedding_model_cache[model_name]
    logging.info("Loading embedding model: '%s'", model_name)
    model = SentenceTransformer(model_name)
    embedding_model_cache[model_name] = model
    return model

summarizer_model = None
def load_summarizer_model():
    global summarizer_model
    if summarizer_model is None:
        logging.info("Loading summarizer model: '%s'", DEFAULT_SUMMARIZER_MODEL)
        summarizer_model = pipeline("summarization", model=DEFAULT_SUMMARIZER_MODEL)
    return summarizer_model

async def compute_embedding(text: str, model_name: Optional[str] = None) -> List[float]:
    actual_name = model_name or DEFAULT_EMBEDDING_MODEL
    model = load_embedding_model(actual_name)
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: model.encode(text).tolist())

# ... rest of your VectorDB, Pydantic schemas, and endpoints remain unchanged ...

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        log_level=settings.LOG_LEVEL.lower(),
    )