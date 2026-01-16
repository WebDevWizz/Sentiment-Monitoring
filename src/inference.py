# In questo file, vado a fare inferenza sul modello con il dataset che ho trovato su Kaggle, ovvero "Tweets.csv"

from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
from src.preprocess import preprocess
from scipy.special import softmax
import torch

MODEL_NAME = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Metodo che uso per fare la predizione (codice che ho scritto basandomi sempre sulla documentazione fornita): 
def predict_sentiment(text: str): 
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt') # Spezzo il testo in unità più piccole (token) con il classico 'tokenizer', facendomi restituire i dati in tensori PyTorch

    # Dovendo solo fare la predizione (senza train), non mi interessano i gradienti: 
    with torch.no_grad(): 
        output = model(**encoded_input) # Passiamo i token al al modello (** = scompatta il dizionario encoded_input passando tutti gli input necessari)

    # Infine, vado come sempre a calcolare i punteggi tramite softmax: 
    scores = softmax(output.logits[0].numpy()) # Prendo il primo dei logits restituiti dal modello e vado ad applicare la softmax per avere le prob.
    # Creo un vettore con le label: 
    labels = ["negative", "neutral", "positive"]

    return dict(zip(labels, scores))