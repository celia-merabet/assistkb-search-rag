from app.ingest import main as ingest
from app.embed import main as embed
from app.store import create_collection, upsert

print("Ingestion...")
ingest()

print("Embeddings...")
embed()

print("Indexation Qdrant...")
create_collection()
upsert()

print("Pipeline terminé")