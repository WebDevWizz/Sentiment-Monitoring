import csv
import os
from datetime import datetime
from src.inference import predict_sentiment


METRICS_FILE = "metrics/sentiment_metrics.csv"

# Questo è il semplice monitoraggio che implemento:
def monitor_text(text):
    # Raccolgo gli scores: 
    scores = predict_sentiment(text)

    # Restituendo un dizionario di prob, prendo quella più alta: 
    sentiment = max(scores, key = scores.get)

    # ⚠️ Correzione post feedback del professore -> come richiesto, salvo anche la confidence della predizione: 
    confidence = scores[sentiment]

    # Controllo se il file esiste già: 
    file_exists = os.path.isfile(METRICS_FILE)

    # Esporto nel file csv: 
    with open(METRICS_FILE, "a", newline= "") as f: 
        writer = csv.writer(f)

        # Se il file è nuovo, scrivo l'header prima dei dati
        if not file_exists:
            writer.writerow(["timestamp", "sentiment", "confidence"])

        writer.writerow([datetime.now().isoformat(), sentiment, confidence])

    return sentiment, confidence


# ⚠️ Correzione post feedback del professore -> ho deciso di implementare anche uno script per testare la funzione, piuttosto che fare tutto da terminale.
# La funzione in questione la può trovare sempre in questa cartella