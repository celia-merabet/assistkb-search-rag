import os
import requests

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = (
    "Tu réponds UNIQUEMENT à partir du contexte fourni. "
    "Cite tes sources au format [source: <document>]. "
    "Si le contexte ne contient pas la réponse, réponds exactement : "
    "'Je ne dispose pas de cette information dans le corpus.'"
)


def build_context(results):
    """Construit le contexte avec la source de chaque chunk."""
    blocs = []
    for r in results:
        blocs.append(f"[source: {r.payload['source']}]\n{r.payload['text']}")
    return "\n\n---\n\n".join(blocs)


def call_groq(prompt):
    """Appelle le LLM Groq et renvoie (texte, tokens)."""
    response = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    text = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    tokens = {
        "prompt": usage.get("prompt_tokens", 0),
        "completion": usage.get("completion_tokens", 0),
    }
    return text, tokens


def generate_answer(query, results):
    context = build_context(results)
    prompt = f"CONTEXTE:\n{context}\n\nQUESTION:\n{query}"
    return call_groq(prompt)