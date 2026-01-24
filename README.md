# Sistema di Monitoraggio
Il progetto include un sistema di monitoraggio progettato per osservare in modo continuo il comportamento del modello di sentiment analysis, usando il modello pre-addestrato Twitter RoBERTa. Il dataset è stato invece preso da Kaggle, e salvato nel progetto come "Tweets.csv". 

Il sistema di monitoraggio è stato progettato secondo una logica MLOps-oriented, con separazione tra:
- fase di inferenza
- fase di raccolta delle metriche
- fase di analisi
- fase di visualizzazione


## Raccolta delle Metriche
È stato implementato un sistema di logging basato su file CSV, utilizzato come storage persistente delle metriche di monitoraggio. Il file ```sentiment_metrics.csv``` (presente nella cartella metrics/) contiene per ogni predizione:
- timestamp → istante temporale della predizione (UTC, formato ISO)
- sentiment → label predetta dal modello (positive, neutral, negative)
- confidence → probabilità associata alla predizione (softmax score)

La raccolta delle metriche è gestita dalla funzione:
``` monitor_batch(...) ```
che esegue le seguenti operazioni:
- inferenza batch sui testi in input
- logging automatico delle predizioni nel CSV
- calcolo della distribuzione delle classi (positive/neutral/negative)
- calcolo della confidence media
- rilevamento del drift rispetto a una baseline opzionale

---

## Distribuzione e Drit Detection
Il sistema di monitoraggio non si limita al semplice logging, ma implementa anche:

### 📊 Distribuzione delle label
Calcolo percentuale delle classi predette nel batch:
- positive
- neutral
- negative

### 📈 Confidence media
Calcolo della probabilità media delle predizioni come indicatore di affidabilità del modello.

### Drift Detection
Il drift viene rilevato confrontando la distribuzione corrente con una baseline di riferimento:
```
baseline_distribution = {
    "positive": ...,
    "neutral": ...,
    "negative": ...
}
```

Se la differenza assoluta tra distribuzione corrente e baseline supera una soglia (drift_threshold = 0.2), il sistema segnala drift:
```
Drift detected: YES
```

Questo meccanismo simula un reale scenario MLOps, in cui il drift rappresenta un segnale per un possibile retraining del modello.

---


## Visualizzazione delle Metriche
Inizialmente è stata progettata una visualizzazione basata su Grafana, utilizzando Docker Compose e il plugin Infinity per la lettura di file CSV.

### Docker Compose

Il file docker-compose.yml configura un container Grafana con volume persistente:
```
services:
  grafana:
    image: grafana/grafana-enterprise
    container_name: grafana
    restart: unless-stopped
    ports:
      - '3000:3000'
    environment:
      - GF_INSTALL_PLUGINS=yesoreyeram-infinity-datasource
    volumes:
      - grafana-storage:/var/lib/grafana

volumes:
  grafana-storage: {}
```


### Configurazione Grafana
Configurazione prevista:
- Data Source di tipo Infinity
- Query di tipo CSV
- URL:
```
file:///var/lib/grafana/data/metrics/sentiment_metrics.csv
```


### Limitazione Tecnica
Nonostante diverse configurazioni e test, Grafana non è riuscito a leggere correttamente il file CSV locale tramite il plugin Infinity.

Errore riscontrato:
```
error while performing the infinity query. 
error getting response from url /var/lib/grafana/data/metrics/sentiment_metrics.csv.
Error: Get "https:///var/lib/grafana/data/metrics/sentiment_metrics.csv": http: no Host in request URL
```
Questa limitazione è legata alle restrizioni del plugin Infinity nell’accesso a file locali all’interno di ambienti containerizzati.
---

## Soluzione Alternativa di Visualizzazione (Funzionante)
Per garantire un sistema di monitoraggio realmente operativo e verificabile, è stata implementata una visualizzazione alternativa in Python, basata su pandas e matplotlib.

Il modulo:
```
monitoring/visualize.py
```
permette di visualizzare direttamente:
- distribuzione del sentiment
- andamento delle predizioni

Esempio di utilizzo:
```
from monitoring.visualize import plot_sentiment_distribution

visualize_sentiment_distribution("metrics/sentiment_metrics.csv")
```

Questa soluzione garantisce:
- visualizzazione reale dei dati
- riproducibilità
- indipendenza dall’infrastruttura container
- funzionamento deterministico
