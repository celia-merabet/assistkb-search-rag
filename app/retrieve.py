from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer("all-MiniLM-L6-v2")

COLLECTION = "assistkb"


def search(query, top_k=5):
    query_vec = model.encode(query, normalize_embeddings=True)

    results = client.search(
        collection_name=COLLECTION,
        query_vector=query_vec,
        limit=top_k
    )

    return results