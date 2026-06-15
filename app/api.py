import time
from fastapi import FastAPI
from pydantic import BaseModel
from app.retrieve import search, should_refuse
from app.generate import generate_answer

app = FastAPI()


class Question(BaseModel):
    question: str
    top_k: int = 5


@app.post("/ask")
def ask(q: Question):
    start = time.time()
    results = search(q.question, top_k=q.top_k)

    if should_refuse(results):
        return {
            "answer": "Je ne dispose pas de cette information dans le corpus.",
            "sources": [],
            "latency_ms": int((time.time() - start) * 1000),
            "tokens": {"prompt": 0, "completion": 0},
        }

    answer, tokens = generate_answer(q.question, results)

    return {
        "answer": answer,
        "sources": [
            {
                "doc": r.payload["source"],
                "chunk_id": r.payload["chunk_id"],
                "score": round(r.score, 3),
            }
            for r in results
        ],
        "latency_ms": int((time.time() - start) * 1000),
        "tokens": tokens,
    }