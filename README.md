
# AssistKB Search - Projet RAG


## Équipe du projet

* Membre 1 : Celia Merabet
* Membre 2 : BOUYABRI Mohamed

  NOTE: pour l’instant le travail est en cours sur les deux branches R2-RETRIEVAL et R3-RETRIEVAL

---

## Lancement du projet

### Installation

```bash
git clone https://github.com/celia-merabet/assistkb-search-rag.git
cd assistkb-search-rag
pip install -r requirements.txt
```

### Lancement avec Docker

```bash
docker-compose up --build
```

---

## Contexte du projet

Ce projet s’inscrit dans un TP de mise en pratique d’un pipeline complet de Retrieval-Augmented Generation (RAG).
L’objectif est de construire un assistant capable de répondre à des questions en s’appuyant sur un corpus documentaire externe, tout en citant ses sources

Le système est conçu comme un assistant de recherche interne type ESN, permettant d’interroger une base de connaissances hétérogène (PDF, HTML, JSON) et de générer des réponses contextualisées via un modèle de langage

---

## Objectifs

* Construire un pipeline RAG complet de bout en bout
* Ingestion et traitement d’un corpus documentaire
* Indexation vectorielle des documents
* Recherche sémantique (retrieval top-k)
* Génération de réponse avec un LLM
* Retour de sources associées aux réponses
* Conteneurisation via Docker Compose

---

## Stack technique

* Python
* FastAPI
* Sentence-Transformers
* Qdrant (vector database)
* LLM : Gemini ou Groq (free tier)
* Docker / Docker Compose

---

