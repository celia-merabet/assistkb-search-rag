import time
import statistics
import requests

API_URL = "http://localhost:8000/ask"

QUESTIONS_CORPUS = [
    "Que s'est-il passé lors de l'incident hallucination ?",
    "Quelles sont les causes de l'incident de latence RAG ?",
    "Comment anonymiser le corpus selon les règles RGPD ?",
    "Que contient le retour d'expérience de la mission Banque Alpha ?",
    "Quelle est l'architecture d'AssistKB ?",
]

QUESTIONS_HORS_CORPUS = [
    "Quelle est la capitale de l'Australie ?",
    "Comment faire une tarte aux pommes ?",
    "Qui a gagné la Coupe du Monde 2022 ?",
    "Quel est le prix du Bitcoin aujourd'hui ?",
    "Comment fonctionne un moteur diesel ?",
]

REFUS = "Je ne dispose pas de cette information dans le corpus."


def ask(question):
    r = requests.post(API_URL, json={"question": question}, timeout=120)
    r.raise_for_status()
    return r.json()


def main():
    latences, scores, tokens_totaux = [], [], []
    refus_corpus = 0
    refus_hors = 0

    print("=== Questions DANS le corpus ===")
    for q in QUESTIONS_CORPUS:
        d = ask(q)
        est_refus = d["answer"].strip() == REFUS
        refus_corpus += est_refus
        latences.append(d["latency_ms"])
        tokens_totaux.append(d["tokens"]["prompt"] + d["tokens"]["completion"])
        if d["sources"]:
            scores.append(d["sources"][0]["score"])
        print(f"  [{'REFUS' if est_refus else 'OK   '}] {d['latency_ms']:>5} ms | {q[:55]}")

    print("\n=== Questions HORS corpus ===")
    for q in QUESTIONS_HORS_CORPUS:
        d = ask(q)
        est_refus = d["answer"].strip() == REFUS
        refus_hors += est_refus
        print(f"  [{'REFUS' if est_refus else 'FUITE'}] {d['latency_ms']:>5} ms | {q[:55]}")

    n, m = len(QUESTIONS_CORPUS), len(QUESTIONS_HORS_CORPUS)
    lat = sorted(latences)
    p50 = lat[len(lat) // 2]
    p95 = lat[min(len(lat) - 1, int(len(lat) * 0.95))]
    tokens_moy = statistics.mean(tokens_totaux) if tokens_totaux else 0
    cout_1000 = (tokens_moy * 0.69 / 1_000_000) * 1000

    print("\n=== MÉTRIQUES ===")
    print(f"Score similarité moyen (top-1)    : {statistics.mean(scores):.3f}")
    print(f"Taux de réponse (corpus)          : {(n - refus_corpus) / n * 100:.0f} %")
    print(f"Taux de refus (hors corpus)       : {refus_hors / m * 100:.0f} %")
    print(f"Latence p50 / p95                 : {p50} / {p95} ms")
    print(f"Tokens moyens (prompt+completion) : {tokens_moy:.0f}")
    print(f"Coût projeté / 1000 questions     : {cout_1000:.3f} USD")


if __name__ == "__main__":
    main()