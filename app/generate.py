def build_context(results):
    return "\n\n".join([
        r.payload["text"] for r in results
    ])


def generate_answer(llm_call, query, results):
    context = build_context(results)

    prompt = f"""
Tu es un assistant qui répond uniquement avec le contexte.

CONTEXTE:
{context}

QUESTION:
{query}

Si la réponse n'est pas dans le contexte, dis :
"Je ne dispose pas de cette information dans le corpus."
"""

    return llm_call(prompt)