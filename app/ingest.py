import os
import json
import re
from bs4 import BeautifulSoup
from pypdf import PdfReader
from langdetect import detect

CHUNK_SIZE = 500
OVERLAP = 80


# -------------------------
# CLEAN TEXT
# -------------------------
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -------------------------
# EXTRACTORS
# -------------------------
def extract_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_html(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        return soup.get_text()


def extract_json(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        data = json.load(f)
    return json.dumps(data)


def extract(path):
    if path.endswith(".pdf"):
        return extract_pdf(path)
    elif path.endswith(".html") or path.endswith(".htm"):
        return extract_html(path)
    elif path.endswith(".json"):
        return extract_json(path)
    else:
        return extract_txt(path)


# -------------------------
# CHUNKING
# -------------------------
def chunk_text(text):
    words = text.split()
    chunks = []

    i = 0
    while i < len(words):
        chunk = words[i:i + CHUNK_SIZE]
        chunks.append(" ".join(chunk))
        i += CHUNK_SIZE - OVERLAP

    return chunks


# -------------------------
# PROCESS FILE
# -------------------------
def process_file(path):
    text = extract(path)
    text = clean_text(text)

    if len(text) < 50:
        return []

    try:
        lang = detect(text)
    except:
        lang = "unknown"

    chunks = chunk_text(text)

    results = []
    for i, c in enumerate(chunks):
        results.append({
            "text": c,
            "source": path,
            "chunk_id": i,
            "language": lang
        })

    return results


# -------------------------
# MAIN
# -------------------------
def main():
    input_dir = "corpus/seed"
    output_file = "corpus/chunks.jsonl"

    all_chunks = []

    for root, _, files in os.walk(input_dir):
        for f in files:
            path = os.path.join(root, f)
            chunks = process_file(path)
            all_chunks.extend(chunks)

    with open(output_file, "w", encoding="utf-8") as f:
        for c in all_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    print(f"OK chunks generated: {len(all_chunks)}")


if __name__ == "__main__":
    main()