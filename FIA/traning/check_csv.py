import pandas as pd
import os

# Configurazione
filename = "WELFake_Dataset.csv"
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, filename)

print(f"--- CONTROLLO FILE: {filename} ---")

if not os.path.exists(file_path):
    print("ERRORE: File non trovato! Controlla di averlo messo in 'training'")
    exit()

# Leggiamo solo le prime 5 righe per essere veloci
df = pd.read_csv(file_path, nrows=5)

print("\n1. NOMI DELLE COLONNE TROVATE:")
print(list(df.columns))

print("\n2. ESEMPIO DI TESTO (Prima riga):")
# Stampiamo i primi 200 caratteri del testo per vedere se c'è "Reuters"
print(str(df.iloc[0]['text'])[:200])

print("\n3. ESEMPIO DI LABEL:")
print(df.iloc[0]['label'])