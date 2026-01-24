from monitoring.monitoring import monitor_batch

""" 
    1. Test che verifica l'output strutturalmente corretto del sistema di monitoraggio.
    - tmp_path = crea una cartella temporanea solo per questo test.

    Con questo test verifico che: 
    - Il risultato sia un dict
    - Nel dict c'è la distribuzione, avg confidence e drift

    Basta simulare la produzione di un monitoring su un csv temporaneo
"""
def test_output(tmp_path): # ✅ PASSATO
    csv_path = tmp_path / "metrics.csv"

    texts = [
        "I love this product",
        "This is the worst thing ever",
        "It's okay, nothing special"
    ]

    result = monitor_batch(texts, csv_path=str(csv_path))

    assert isinstance(result, dict)
    assert "distribution" in result 
    assert "avg confidence" in result 
    assert "drift" in result 



""" 
    2. Test che verifica che le chiavi del dict delle distribuzioni siano corrette
"""
def test_distribution_keys(tmp_path): # ✅ PASSATO
    csv_path = tmp_path / "metrics.csv"

    texts = [
        "I love this", 
        "I hate this", 
        "It's okay"
    ]

    result = monitor_batch(texts, csv_path=str(csv_path))
    distribution = result["distribution"]

    # Salvo in un array le chiavi che mi aspetto, e poi testo: 
    expcted_keys = {"positive", "neutral", "negative"}

    # Uso un set per raccogliere le chiavi del dict, in modo da evitare duplicati
    assert set(distribution.keys()) == expcted_keys



""" 
    3. Test che verifica che i valori delle distribuzioni sommino (come da definizione di distribuzione) a ~1.0
"""
def test_distribution_values(tmp_path): # ✅ PASSATO
    csv_path = tmp_path / "metrics.csv"
    texts = [
        "Amazing experience",
        "Terrible experience", 
        "Not bad"
    ]

    result = monitor_batch(texts, csv_path = str(csv_path))
    distribution_values = result["distribution"].values()

    total = sum(distribution_values)

    assert abs(total-1.0) < 1e-5




""" 
    4. Test che verifica che sentiment esterni vengano classificati correttamente
"""
def test_external_sentiment(tmp_path): # ✅ PASSATO
    csv_path = tmp_path / "metrics.csv"

    texts = [
        "I absolutely love this product, it's fantastic!",
        "This is the worst experience of my life, terrible service"
    ]

    result = monitor_batch(texts, csv_path=str(csv_path))
    distribution = result["distribution"]

    assert distribution["positive"] > 0.0
    assert distribution["negative"] > 0.0