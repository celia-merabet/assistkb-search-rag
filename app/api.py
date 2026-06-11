from fastapi import FastAPI
from app.retrieve import search, should_refuse
from app.generate import generate_answer
import time

app = FastAPI()


# 👉 LLM SIMPLE (tu remplaces par Groq ou Gemini)
def fake_llm(prompt):
    return "Réponse basée sur le contexte fourni."


@app.post("/ask")
def ask(question: str):
    start = time.time()

    results = search(question, top_k=5)

    if should_refuse(results):
        return {
            "answer": "Je ne dispose pas de cette information dans le corpus.",
            "sources": [],
            "latency_ms": int((time.time() - start) * 1000)
        }

    answer = generate_answer(fake_llm, question, results)

    return {
        "answer": answer,
        "sources": [r.payload["source"] for r in results],
        "latency_ms": int((time.time() - start) * 1000)
    }