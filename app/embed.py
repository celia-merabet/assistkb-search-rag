import json
from sentence_transformers import SentenceTransformer

MODEL = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL)


def load_chunks(path="corpus/chunks.jsonl"):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def main():
    chunks = load_chunks()

    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, normalize_embeddings=True)

    for i in range(len(chunks)):
        chunks[i]["embedding"] = embeddings[i].tolist()

    with open("corpus/embedded.jsonl", "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    print(f"OK embeddings generated: {len(chunks)}")


if __name__ == "__main__":
    main()