# ⚠️ Dopo il feedback del professore, ho deciso di implementare l'evaluate andando a valutare direttamente il classification_report e accuracy_score, in modo da avere accuracy, precision, f1 e recall.
# OSS: ovviamente, nel file requirements.txt ho adesso inclusso sci-kit learn.

import pandas as pd
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from src.inference import predict_sentiment


def evaluate(csv_path): 
    df = pd.read_csv(csv_path).head(300)  #⚠️ Dopo il feedback del professore, ho deciso di prendere i primi 300 esempi del dataset, in modo da avere delle delle metriche più precise.
    y_true = []
    y_pred = []

    # Conto tutte le predizioni corrette ciclando su ogni riga del file CSV (ignorando, ovviamente, l'indice di riga) 
    for _, row in df.iterrows(): 
        # Per come ho costruito la funzione di predict, essa restituisce un dizionario contenente la previsione con la corrispondente probabilità; 
        # EX: {'negative': 0.1, 'neutral': 0.2, 'positive': 0.9} 
        # -> Da questo dict, devo poi logicamente ricavare il valore più alto (che coincide con la previsione) 
        scores = predict_sentiment(row["text"])
        pred = max(scores, key=scores.get)

        y_true.append(row["sentiment"])
        y_pred.append(pred)
    
    report = classification_report(y_true, y_pred)
    acc = accuracy_score(y_true, y_pred)
    conf_matrix = confusion_matrix(y_true, y_pred)

    print(f"Accuracy: {acc:.2f}")
    print("\nDetailed Report:")
    print(report)
    print("\nConfusion Matrix:")
    print(conf_matrix)
