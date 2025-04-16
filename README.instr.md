# RAG Pipeline API with CRUD and Embedding

This API implements a complete Retrieval Augmented Generation (RAG) pipeline. It provides endpoints to:
- Compute text embeddings using a SentenceTransformer (with dynamic model selection).
- Perform a semantic search against a vector database abstraction.
- Summarize documents via a summarization model.
- Manage document entries (CRUD) while automatically computing embeddings if needed.

## Prerequisites

Ensure you have Python 3.7+ installed. Then, install the required packages:

```bash
pip install fastapi uvicorn sentence-transformers transformers pytest
```

## Running the API Server

1. Save the API code into a file (e.g., `main.py`).

2. Run the API with Uvicorn:

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at [http://localhost:8000](http://localhost:8000).

## Interactive API Documentation

FastAPI provides interactive documentation pages:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

These interfaces let you inspect and interact with the API endpoints directly.

## Testing the Endpoints

### 1. Search Endpoint

Send a POST request to `/search` to compute the embedding for a query and retrieve the top matching documents.

**Example using cURL:**

```bash
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{
          "query": "Deep learning in NLP",
          "model_name": "Linq-Embed-Mistral",
          "top_k": 3
     }'
```

### 2. Summarization Endpoint

The `/summarize` endpoint accepts either raw text or a document ID and returns a summary.

**Using raw text:**

```bash
curl -X POST "http://localhost:8000/summarize" \
     -H "Content-Type: application/json" \
     -d '{
          "text": "Your long text that needs summarization goes here."
     }'
```

**Using a document ID:**

```bash
curl -X POST "http://localhost:8000/summarize" \
     -H "Content-Type: application/json" \
     -d '{
          "doc_id": "1"
     }'
```

### 3. CRUD Endpoints for Documents

#### Create a Document

Create a new document. The server automatically computes an embedding from the provided text if one is not supplied. You may optionally include a `"model_name"` to control which embedding model is used.

```bash
curl -X POST "http://localhost:8000/documents" \
     -H "Content-Type: application/json" \
     -d '{
          "text": "New research document text",
          "model_name": "Linq-Embed-Mistral"
     }'
```

#### List All Documents

Retrieve a list of all documents in the vector DB:

```bash
curl -X GET "http://localhost:8000/documents"
```

#### Get a Specific Document by ID

Replace `<doc_id>` with an actual document ID:

```bash
curl -X GET "http://localhost:8000/documents/<doc_id>"
```

#### Update a Document

Update a document's text. The embedding is recomputed automatically if the text is updated.

```bash
curl -X PUT "http://localhost:8000/documents/<doc_id>" \
     -H "Content-Type: application/json" \
     -d '{
           "text": "Updated research document text",
           "model_name": "Linq-Embed-Mistral"
         }'
```

#### Delete a Document

Delete a document by its ID:

```bash
curl -X DELETE "http://localhost:8000/documents/<doc_id>"
```

## Automated Testing with pytest

You can also write automated tests. Below is an example test file (`test_main.py`):

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_endpoint():
    payload = {
        "query": "Deep learning in NLP",
        "model_name": "Linq-Embed-Mistral",
        "top_k": 3
    }
    response = client.post("/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "embedding" in data
    assert "retrieved_documents" in data

def test_create_document():
    payload = {
        "text": "This is a new research paper for testing.",
        "model_name": "Linq-Embed-Mistral"
    }
    response = client.post("/documents", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["text"] == payload["text"]
    assert "embedding" in data

# Additional tests for get, update, and delete can be added here.
```

Run the tests with:

```bash
pytest test_main.py
```

## Additional Information

- **In-Memory Database:**  
  The vector database in this implementation is in-memory. Documents will not persist across server restarts.

- **Dynamic Model Selection:**  
  You can change the embedding model by providing a different `"model_name"` in your requests.

- **Logging:**  
  Check the terminal logs to see messages for model loading, embedding computations, and CRUD operations.

---

This README guides you through running and testing the API. Adjust the instructions as needed for your development and deployment workflow.
```