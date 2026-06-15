import os
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Host configurable : "localhost" en local, "qdrant" dans Docker
QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.environ.get("QDRANT_PORT", 6333))
SEUIL = float(os.environ.get("SEUIL_SIMILARITE", 0.35))
COLLECTION = "assistkb"

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query, top_k=5):
    query_vec = model.encode(query, normalize_embeddings=True)
    results = client.search(
        collection_name=COLLECTION,
        query_vector=query_vec,
        limit=top_k
    )
    return results


def should_refuse(results):
    """Refus si aucun résultat ou si le meilleur score est sous le seuil."""
    if not results:
        return True
    return results[0].score < SEUIL


if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "mesures de sécurité"
    for r in search(q):
        print(f"[{r.score:.2f}] {r.payload['source']} :: {r.payload['text'][:80]}...")