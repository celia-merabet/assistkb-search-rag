# AssistKB Search - Projet RAG


## Équipe du projet

* Membre 1 : Celia Merabet
* Membre 2 : BOUYABRI Mohamed

---

## Contexte du projet

Ce projet s'inscrit dans un TP de mise en pratique d'un pipeline complet de
Retrieval-Augmented Generation (RAG). L'objectif est de construire un assistant
capable de répondre à des questions en s'appuyant sur un corpus documentaire,
tout en citant ses sources et en **refusant de répondre** lorsque l'information
n'est pas présente dans le corpus (seuil de similarité, anti-hallucination).

Le système simule un assistant de recherche interne type ESN, interrogeant une
base de connaissances hétérogène (incidents, REX, fiches outils, RGPD).

---

## Stack technique

* FastAPI
* Sentence-Transformers (all-MiniLM-L6-v2)
* Qdrant
* Groq (llama-3.3-70b-versatile)
* Docker / Docker Compose
* BeautifulSoup / PyPDF / lxml

---

## Lancement du projet

```bash
git clone https://github.com/celia-merabet/assistkb-search-rag.git
cd assistkb-search-rag
git checkout r3-retrieval

# Configurer la clé API (gratuite sur console.groq.com)
cp .env.example .env
# → renseigner GROQ_API_KEY dans .env

docker compose up -d --build
```

Au démarrage, le conteneur API indexe automatiquement le corpus
(`corpus/seed`) puis lance l'API sur http://localhost:8000.

---

## Tester l'API

Question présente dans le corpus (réponse avec sources) :
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Que s est-il passé lors de l incident hallucination ?"}'
```

Question hors corpus (refus) :
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Quelle est la capitale de l Australie ?"}'
```

Interface interactive : http://localhost:8000/docs

Mesurer les métriques (depuis un environnement avec `requests`) :
```bash
python app/metrics.py
```

---

## Évaluation et bonus

**Golden dataset (recall@k)** — `eval/golden.json` associe des questions au document attendu. Le script `app/eval.py` mesure le recall@1/@3/@5 du retrieval :
```bash
docker compose exec api python -m app.eval
```

**Reranking (cross-encoder)** — un cross-encoder (`ms-marco-MiniLM-L-6-v2`) re-classe les résultats. Sur le golden dataset, le recall@1 passe de 88 % à 100 %.

**Intégration continue** — un workflow GitHub Actions (`.github/workflows/ci.yml`) vérifie la syntaxe Python et la validité du golden dataset à chaque push.

---

## Structure du projet

```
app/
  ingest.py      # extraction + chunking des documents
  embed.py       # vectorisation (all-MiniLM-L6-v2)
  store.py       # indexation Qdrant (IDs déterministes anti-doublons)
  retrieve.py    # recherche top-k + seuil de refus
  generate.py    # appel LLM Groq, réponse citée
  api.py         # API FastAPI POST /ask
  metrics.py     # mesures qualité + exploitation
scripts/
  index.py       # pipeline complet (lancé au démarrage du conteneur)
  fetch_corpus.sh / .ps1   # récupération de corpus additionnel
corpus/seed/     # base de connaissances (incidents, REX, RGPD, architecture)
docs/            # compte-rendu et captures
```

---

## Corpus utilisé

Le corpus de base (`corpus/seed`) contient des documents internes simulés :
fiches d'incidents, retours d'expérience de mission, fiche outil Qdrant,
document RGPD et description d'architecture. Un corpus additionnel (data.gouv)
peut être récupéré via `scripts/fetch_corpus.ps1 -Profile open`.

---

## Variables d'environnement (`.env`)

```
GROQ_API_KEY=          # votre clé Groq
GROQ_MODEL=llama-3.3-70b-versatile
QDRANT_HOST=qdrant
QDRANT_PORT=6333
SEUIL_SIMILARITE=0.35  # en dessous : refus de répondre

```