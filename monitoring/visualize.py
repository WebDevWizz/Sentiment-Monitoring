""" 
    Alla luce dei problemi che ho riscontrato nella visualizzazione con Grafana (e che purtroppo non sono riuscito ancora a risolvere), 
    implemento qui una Visualizzazione delle metriche calcolate durante il monintoraggio usando stesso Python
"""

import pandas as pd 
import matplotlib.pyplot as plt


def visualize_sentiment_distribution(csv_path: str) -> None: 
    """ 
    Visualizza la distribuzione del sentiment dal monitoraggio del file CSV
    """

    df = pd.read_csv(csv_path)

    sentiment_counts = df["sentiment"].value_counts(normalize=True)

    sentiment_counts.plot(kind="bar", title="Sentiment Distribution", ylabel="Percentage")

    plt.show()