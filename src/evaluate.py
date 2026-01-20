# In questo file, andiamo infine a valutare l'accuratezza come metrica per le predizioni: 
import pandas as pd
from src.inference import predict_sentiment


def evaluate(csv_path): 
    df = pd.read_csv(csv_path).head(10)  # Prendo solo i primi 10 esempi del dataset, altrimenti la funzione sarebbe troppo lunga da eseguire
    correct = 0

    # Conto tutte le predizioni corrette ciclando su ogni riga del file CSV (ignorando, ovviamente, l'indice di riga) 
    for _, row in df.iterrows(): 
        # Per come ho costruito la funzione di predict, essa restituisce un dizionario contenente la previsione con la corrispondente probabilità; 
        # EX: {'negative': 0.1, 'neutral': 0.2, 'positive': 0.9} 
        # -> Da questo dict, devo poi logicamente ricavare il valore più alto (che coincide con la previsione) 
        scores = predict_sentiment(row["text"])
        pred = max(scores, key=scores.get)

        if pred == row["sentiment"]: 
            correct += 1

    
    accuracy = correct / len(df)
    print(f"Accuracy on {len(df)} samples: {accuracy:.2f}")
