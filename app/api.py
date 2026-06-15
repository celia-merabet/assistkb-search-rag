import time
from fastapi import FastAPI
from pydantic import BaseModel

from app.retrieve import search, should_refuse
from app.generate import generate_answer

app = FastAPI()



class Question(BaseModel):
    question: str
    top_k: int = 5



@app.get("/health")
def health():
    return {"status": "ok"}


# ------------------------
# MAIN RAG ENDPOINT
# ------------------------
@app.post("/ask")
def ask(q: Question):

    start = time.time()

    # 1. retrieval Qdrant
    results = search(q.question, top_k=q.top_k)

    # 2. métrique retrieval (score max + moyenne)
    scores = [r.score for r in results]

    avg_similarity = (
        round(sum(scores) / len(scores), 3)
        if scores
        else 0
    )

    best_score = max(scores) if scores else 0

    # 3. refus si hors corpus
    refused = should_refuse(results)

    # 4. CAS REFUS
    if refused:
        return {
            "answer": "Je ne dispose pas de cette information dans le corpus.",
            "sources": [],
            "latency_ms": int((time.time() - start) * 1000),
            "tokens": {"prompt": 0, "completion": 0},
            "metrics": {
                "avg_similarity": avg_similarity,
                "best_score": best_score,
                "refused": True
            }
        }

    # 5. génération LLM
    answer, tokens = generate_answer(q.question, results)

    # 6. réponse finale
    return {
        "answer": answer,

        "sources": [
            {
                "doc": r.payload.get("source"),
                "chunk_id": r.payload.get("chunk_id"),
                "score": round(r.score, 3)
            }
            for r in results
        ],

        "latency_ms": int((time.time() - start) * 1000),

        "tokens": tokens,

        "metrics": {
            "avg_similarity": avg_similarity,
            "best_score": best_score,
            "refused": False
        }
    }