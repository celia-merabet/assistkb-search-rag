import sys
import os


sys.path.append(os.path.abspath("."))

from app.retrieve import search, should_refuse


TEST_QUESTIONS = [
    # DANS corpus (doit répondre)
    "Quelles mesures de sécurité sont recommandées pour les données personnelles ?",
    "Qu'est-ce qu'une recherche vectorielle hybride ?",

    # HORS corpus (doit refuser)
    "Quelle est la capitale de l'Australie ?",
    "Quel est le chiffre d'affaires 2025 de banque-alpha ?"
]


def evaluate():
    total = len(TEST_QUESTIONS)
    refus = 0
    scores = []

    for q in TEST_QUESTIONS:

        results = search(q, top_k=5)

        # score max retrieval
        if results:
            scores.append(results[0].score)
        else:
            scores.append(0)

        if should_refuse(results):
            refus += 1

        print("\nQUESTION:", q)
        print("TOP SCORE:", results[0].score if results else 0)
        print("REFUS:", should_refuse(results))

    print("\n====================")
    print("RESULTATS GLOBAUX")
    print("Refus rate:", refus / total)
    print("Avg score:", sum(scores) / len(scores))


if __name__ == "__main__":
    evaluate()