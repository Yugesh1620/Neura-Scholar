# locustfile.py
import random
import string
from locust import HttpUser, TaskSet, task, between

# A small set of example queries and texts to drive your tests
EXAMPLE_QUERIES = [
    "machine learning systems engineering",
    "semantic search research papers",
    "vector databases performance",
    "deep learning optimizations",
    "devops ml pipelines",
]

EXAMPLE_SUMMARY_TEXTS = [
    "This paper explores the impact of quantization on model size and inference latency in ONNXRuntime.",
    "We propose a novel CI/CD pipeline for continuous retraining of summarization models using human-in-the-loop feedback.",
    "An evaluation of dynamic batching strategies for Triton Inference Server under bursty workloads.",
]


class RAGTasks(TaskSet):
    @task(4)
    def search(self):
        payload = {
            "query": random.choice(EXAMPLE_QUERIES),
            "top_k": random.choice([3, 5, 10]),
            # you can also test alternate embedding models
            "model_name": random.choice([None, "all-mpnet-base-v2"]),
        }
        self.client.post("/search", json=payload, name="POST /search")

    @task(2)
    def summarize_text(self):
        payload = {"text": random.choice(EXAMPLE_SUMMARY_TEXTS)}
        self.client.post("/summarize", json=payload, name="POST /summarize - text")

    @task(1)
    def summarize_doc(self):
        # assumes your VectorDB mock has IDs "1","2","3"
        payload = {"doc_id": random.choice(["1", "2", "3"])}
        self.client.post("/summarize", json=payload, name="POST /summarize - doc_id")

    @task(1)
    def create_and_delete_document(self):
        # create a new document
        text = " ".join(random.choices(string.ascii_lowercase, k=50))
        create_payload = {"text": text}
        with self.client.post(
            "/documents",
            json=create_payload,
            name="POST /documents",
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                doc_id = resp.json()["id"]
                # immediately delete it
                self.client.delete(
                    f"/documents/{doc_id}", name="DELETE /documents/{doc_id}"
                )


class RAGUser(HttpUser):
    tasks = [RAGTasks]
    wait_time = between(0.5, 2.0)
