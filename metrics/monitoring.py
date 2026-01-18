import csv
from datetime import datetime
from src.inference import predict_sentiment


METRICS_FILE = "metrics/sentiment_metrics.csv"

# Questo è il semplice monitoraggio che implemento:
def monitor_text(text):
    # Raccolgo gli scores: 
    scores = predict_sentiment(text)

    # Restituendo un dizionario di prob, prendo quella più alta: 
    sentiment = max(scores, key = scores.get)

    # Esporto nel file csv: 
    with open(METRICS_FILE, "a", newline= "") as f: 
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), sentiment])

    return sentiment