"""
Script di test per il sistema di monitoraggio.

Permette di validare facilmente:
- il corretto funzionamento della funzione di monitoring
- la scrittura dei risultati nel file CSV
- il calcolo di sentiment e confidence

Rispetto all'utilizzo diretto da terminale, questo script
fornisce un test controllato e ripetibile.
"""

from monitoring.monitoring import monitor_batch

def run_test():
    print("Start Monitoring...\n")

    test_sentences = [
        "This company is amazing, I really love it",
        "The product is terrible and disappointing",
        "Package arrived on time, everything is fine",
        "I expected something better",
        "What a terrible experience",
        "This company sucks!",
        "Not bad"
    ]

    # Baseline (opzionale, può anche essere rimossa): 
    baseline = {
        "Positive": 0.7, 
        "Neutral": 0.2, 
        "Negative": 0.1
    }

    results = monitor_batch(
        texts=test_sentences, 
        csv_path="metrics/sentiment_metrics.csv", 
        baseline_distribution=baseline, 
        drift_threshold=0.2
    )

    print("End Monitoring")
    


if __name__ == "__main__":
    run_test()