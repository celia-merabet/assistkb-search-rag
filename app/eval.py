import json
from app.retrieve import search, rerank

GOLDEN_PATH = "eval/golden.json"


def load_golden():
    with open(GOLDEN_PATH, encoding="utf-8") as f:
        return json.load(f)


def rang_du_doc(retrieved, expected):
    for i, doc in enumerate(retrieved, start=1):
        if expected in doc:
            return i
    return None


def evaluate(top_k_values=(1, 3, 5), use_rerank=False):
    golden = load_golden()
    n = len(golden)
    hits = {k: 0 for k in top_k_values}

    for item in golden:
        question = item["question"]
        expected = item["expected_source"]

        # On récupère plus de candidats si on rerank (10), sinon 5
        results = search(question, top_k=10 if use_rerank else max(top_k_values))
        if use_rerank:
            results = rerank(question, results)

        retrieved = [r.payload["source"] for r in results]
        rang = rang_du_doc(retrieved, expected)

        for k in top_k_values:
            if rang is not None and rang <= k:
                hits[k] += 1

    return hits, n


def main():
    print("=== SANS reranking ===")
    hits, n = evaluate(use_rerank=False)
    for k in (1, 3, 5):
        print(f"  Recall@{k} : {hits[k]}/{n} = {hits[k] / n * 100:.0f} %")

    print("\n=== AVEC reranking (cross-encoder) ===")
    hits, n = evaluate(use_rerank=True)
    for k in (1, 3, 5):
        print(f"  Recall@{k} : {hits[k]}/{n} = {hits[k] / n * 100:.0f} %")


if __name__ == "__main__":
    main()