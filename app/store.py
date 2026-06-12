from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import json
import uuid
import os

COLLECTION = "assistkb"

client = QdrantClient(host=os.environ.get("QDRANT_HOST", "localhost"), port=6333)


# -------------------------
# CREATE COLLECTION
# -------------------------
def create_collection():
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION not in names:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )
        print("Collection created")


# -------------------------
# LOAD DATA
# -------------------------
def load_data(path="corpus/embedded.jsonl"):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


# -------------------------
# UPSERT
# -------------------------
def upsert():
    data = load_data()

    points = []
    for d in data:
        points.append(
            PointStruct(
                id=str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{d['source']}_{d['chunk_id']}")),
                vector=d["embedding"],
                payload={
                    "text": d["text"],
                    "source": d["source"],
                    "chunk_id": d["chunk_id"],
                    "language": d["language"]
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION,
        points=points
    )

    print(f"Inserted {len(points)} vectors")


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    create_collection()
    upsert()