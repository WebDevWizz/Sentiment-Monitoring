# In questo file ho scritto questo script per testare la funzione e il file csv più facilmente, rispetto a prima del feedback dove invece era necessario passare per il terminale

from monitoring.monitoring import monitor_text

def run_test():
    print("Inizio Monitoraggio...\n")

    frasi_test = [
        "Questa azienda è fantastica, la adoro", 
        "Il prodotto di questa azienda è davvero pessimo", 
        "Pacco arrivato in orario, tutto ok", 
        "Pensavo meglio"
    ]

    for test in frasi_test: 
        sentiment, confidence = monitor_text(test)
        print(f"Testo: {test} -> sentiment: {sentiment}, confidence: {confidence:.2f}")

    print("\nTest completato!")


if __name__ == "__main__":
    run_test()