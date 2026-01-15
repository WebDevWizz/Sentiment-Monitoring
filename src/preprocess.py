# Funzione che serve per pre-processare le stringhe di testo che vengono passate in input al modello, in modo da renderle coerenti con
# i dati su cui è stato addestrato il modello. Utilizzo la funzione presente nella documentazione fornita dal professore.

def preprocess(text): # In pratica, viene ripulito il testo rimuovendo link, tag HTML o normalizzando i caratteri
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)

    # Debug: 
    print("Funzione correttamente eseguita!")
    return " ".join(new_text)