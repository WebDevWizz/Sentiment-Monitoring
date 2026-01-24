import csv
import os 
from collections import Counter 
from datetime import datetime
from src.inference import predict_sentiment


"""
⚠️ Dopo il feedback dato dal professore post prima consegna (e dopo varie prove fatte nei giorni scorsi), 
 ho deciso di scrivere un'unica funzione completa di monitoraggio che non si limita solo a monitorare la confidence, ma che calcoli anche la distribuzione di ogni label 
 (= % di label positive/neutrali/negative) e soprattutto il Drift (rispetto ad una baseline, giusto per avere un punto di riferimento da cui partire nel monitoraggio; tra l'altro, dopo vari tentativi, ho deciso di impostare la soglia del drift a 0.2)
"""


def monitor_batch(texts, csv_path, baseline_distribution = None, drift_threshold = 0.2): 
    # Definisco 2 vettori in cui salvare, rispettivamente, i sentiment (= label) predetti e la confidence: 
    sentiments = []
    confidences = []

    # Flag che mi serve in inferenza per controllare se il file csv già esiste: 
    file_exists = os.path.isfile(csv_path)

    # 1. INFERENZA -> Inizio a calcolare le predizioni (e a prendere quella più grande) e le confidence per ogni text, e le scrivo nel file csv
    with open(csv_path, mode="a", newline="") as f: 
        writer = csv.writer(f)

        # Check che il file non esista già
        if not file_exists:
            # Scrivo l'header di ogni colonna: 
            writer.writerow(["timestamp", "sentiment", "confidence"])


        # A questo punto faccio inferenza: 
        for text in texts: 
            predictions = predict_sentiment(text)
            label = max(predictions, key = predictions.get).lower() # Devo metterle in minuscolo, in quanto il modello fornito nella traccia ha label tutte in minuscolo
            # E ora calcolo la confidence (= probabilità della predizione)
            confidence = predictions[label]

            # Calcolo anche il timestamp: 
            timestamp = datetime.utcnow().isoformat()

            # Scrivo nel file: 
            writer.writerow([timestamp, label, confidence])

            # Salvo le label e le confidence negli appositi vettori: 
            sentiments.append(label)
            confidences.append(confidence)

    
    # 2. Calcolo Distribuzione -> Uso un Counter per raccogliere in un dict le occorrenze di ogni label, per poi dividere per il numero totale di label e ricavare le distribuzioni: 
    counts = Counter(sentiments)
    dim = len(sentiments)

    # Costruisco il mio dizionario delle distribuzioni (OSS: con counts.get("Positive") raccolgo tutte le occorrenze con label "Positive", ecc.): 
    distribution = {
        "positive": counts.get("positive", 0) / dim,
        "neutral": counts.get("neutral", 0) / dim,
        "negative": counts.get("negative", 0) / dim
    }

    # Per completezza, calcolo anche la confidence media: 
    avg_confidence = sum(confidences)/dim


    # 3. Drift -> si verifica quando le caratteristiche dei dati in ingresso cambiano nel tempo; come detto inizialmente, il cambiamento lo monitoro utilizzando una soglia:
    is_drift = False 
    if baseline_distribution: 
        for label in distribution: 
            # Calcolo del drift: (ex: se normalmente abbiamo una distribuzione di "Positive" dell'80%, ma in seguito ad un bug questa si abbassa al 30%, la differenza sarà: |0.3 - 0.8| = 0.5 > 0.2 => DRIFT)
            if abs(distribution[label] - baseline_distribution.get(label, 0)) > drift_threshold: 
                is_drift = True # A questo punto, il sistema avrebbe poi bisogno di un retraining
                break

    
    # 4. Stampo gli output del monitoraggio: 
    print("\nBatch timestamp:", datetime.utcnow().isoformat())
    print("\nDistributions:")
    print(f"\nPositive: {distribution['positive']:.0%}")
    print(f"\nNeutral: {distribution['neutral']:.0%}")
    print(f"\nNegative: {distribution['negative']:.0%}")
    print(f"\nAvg confidence: {avg_confidence:.2f}")
    print(f"Drift detected:", "YES" if is_drift else "NO")


    # La funzione mi ritorna poi un dict contenente distribuzione, confidence media e drift: 
    return {
        "distribution": distribution,
        "avg confidence": avg_confidence,
        "drift": is_drift
    }