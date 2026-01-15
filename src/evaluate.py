# In questo file, andiamo infine a valutare l'accuratezza come metrica per le predizioni: 
import pandas as pd


def evaluate(csv_path): 
    df = pd.read_csv(csv_path)