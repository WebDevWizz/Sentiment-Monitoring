# Sistema di Monitoraggio
Il progetto include un sistema di monitoraggio progettato per osservare in modo continuo il comportamento del modello di sentiment analysis, usando il modello pre-addestrato Twitter RoBERTa. Il dataset è stato invece preso da Kaggle, e salvato nel progetto come "Tweets.csv". 

## Raccolta delle Metriche
Prima dell’introduzione di Docker Compose, è stato implementato un sistema di raccolta delle metriche basato su file CSV.
In particolare, il file sentiment_metrics.csv (presente nella cartella metrics/) viene utilizzato per salvare:
- un timestamp, necessario per una successiva visualizzazione temporale in Grafana;
- il sentiment predetto dal modello.


È stata definita una funzione di monitoraggio **monitor_text**, che esegue l’inferenza sul testo in ingresso e salva automaticamente il risultato nel file CSV. La funzione è stata testata manualmente da terminale, verificando che le predizioni vengano correttamente registrate nel file.

---

## Docker Compose
Per quanto riguarda l’infrastruttura di monitoraggio, è stato utilizzato **Docker Compose** per configurare ***Grafana*** come piattaforma di visualizzazione.
Il file ***docker-compose.yml*** prevede un singolo container Grafana e un volume condiviso, in modo da rendere persistente e accessibile il file CSV contenente le metriche di monitoraggio.


### Configurazione di Grafana
Seguendo la procedura mostrata dal professore durante le lezioni, Grafana è stato configurato nel seguente modo:
- creazione di un Data Source di tipo “Infinity”, utilizzato per la gestione di file CSV;
- creazione di una nuova dashboard, impostando il tipo di query su CSV e specificando come URL il percorso:
***var/lib/grafana/data/metrics/sentiment_metrics.csv***

---


## Nota su una Limitazione Tecnica
Nonostante diversi tentativi e differenti configurazioni dei plugin nel file Docker Compose, Grafana non è riuscito a visualizzare correttamente i dati contenuti nel file CSV tramite il Data Source Infinity.

L’errore restituito è stato costantemente il seguente:
"error while performing the infinity query. error getting response from url /var/lib/grafana/data/metrics/sentiment_metrics.csv.
Error: Get "https:///var/lib/grafana/data/metrics/sentiment_metrics.csv": http: no Host in request URL"

Il sistema di monitoraggio, tuttavia, funziona correttamente dal punto di vista applicativo: le metriche vengono prodotte dal modello e salvate in modo persistente nel file CSV.
Il problema riscontrato sembra essere legato alle limitazioni del plugin Infinity nell’accesso a file locali all’interno di un ambiente containerizzato.

---

## Nota sui Test
Per consentire la corretta esecuzione dei test automatici, è stato necessario inizializzare un file pytest.ini, utilizzato per configurare correttamente il percorso dei moduli Python. In assenza di tale file, l’esecuzione dei test generava errori di import.
