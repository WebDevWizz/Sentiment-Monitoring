# In questo file, scrivo un piccolo test unitario per il metodo "predict_sentiment" -> l'obiettivo è controllare che
# venga restituito un dict
from src.inference import predict_sentiment

def test_predict(): 
    pred = predict_sentiment("Questa è una stringa di esempio")
    assert isinstance(pred, dict) # Test passato correttamente ✅