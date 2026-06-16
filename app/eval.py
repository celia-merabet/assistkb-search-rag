import json
from app.retrieve import search

GOLDEN_PATH = "eval/golden.json"


def load_golden():
    with open(GOLDEN_PATH, encoding="utf-8") as f:
        return json.load(f)


def evaluate(top_k_values=(1, 3, 5)):
    golden = load_golden()
    n = len(golden)
    hits = {k: 0 for k in top_k_values}
    details = []

    for item in golden:
        question = item["question"]
        expected = item["expected_source"]

        # Recherche directe dans Qdrant (pas d'appel LLM)
        results = search(question, top_k=max(top_k_values))
        retrieved = [r.payload["source"] for r in results]

        rang = None
        for i, doc in enumerate(retrieved, start=1):
            if expected in doc:
                rang = i
                break

        for k in top_k_values:
            if rang is not None and rang <= k:
                hits[k] += 1

        details.append((question[:50], expected, rang))

    print("=== Détail par question ===")
    for q, exp, rang in details:
        statut = f"rang {rang}" if rang else "ABSENT"
        print(f"  [{statut:>8}] {q}  ->  attendu: {exp}")

    print("\n=== RECALL@k ===")
    for k in top_k_values:
        print(f"  Recall@{k} : {hits[k]}/{n} = {hits[k] / n * 100:.0f} %")


if __name__ == "__main__":
    evaluate()