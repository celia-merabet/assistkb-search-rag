#!/bin/bash

set -e

RAW_DIR="corpus/raw"

mkdir -p "$RAW_DIR"

echo "==========================="
echo "Fetch corpus..."
echo "Destination: $RAW_DIR"
echo "==========================="

# DATA_QUERY optionnelle
QUERY="${DATA_QUERY:-intelligence artificielle}"

echo "Query: $QUERY"

# ---------
# Wikipedia FR (HTML)
# ---------

curl -L \
"https://fr.wikipedia.org/wiki/Intelligence_artificielle" \
-o "$RAW_DIR/wiki_ia.html"

curl -L \
"https://fr.wikipedia.org/wiki/Recherche_d%27information" \
-o "$RAW_DIR/wiki_recherche.html"

# ---------
# data.gouv (JSON)
# ---------

curl -L \
"https://www.data.gouv.fr/api/1/datasets/" \
-o "$RAW_DIR/data_gouv.json"

# ---------
# Seed local
# ---------

mkdir -p corpus/seed

if [ ! -f corpus/seed/guide_rag.txt ]; then

cat > corpus/seed/guide_rag.txt <<EOF
Une recherche vectorielle hybride combine recherche dense et recherche lexicale.

Les données personnelles doivent être protégées par chiffrement,
journalisation et contrôle des accès.

Les systèmes RAG doivent refuser de répondre lorsqu'aucune information
fiable n'est retrouvée dans le corpus.
EOF

fi

echo ""
echo "Corpus téléchargé :"

find corpus -type f

echo ""
echo "Terminé."