import pandas as pd
import re
import os

# CONFIGURAZIONE
INPUT_FILE = "WELFake_Dataset.csv"
OUTPUT_FILE = "WELFake_Cleaned.csv"


def clean_text_bias(text):
    """
    Pulisce il testo rimuovendo pattern Reuters e URL
    """
    if not isinstance(text, str):
        return ""

    # Rimuove "WASHINGTON (Reuters) -" e simili all'inizio
    text = re.sub(r"^.*?\(Reuters\)\s*-\s*", "", text)
    text = re.sub(r"^.*?\([A-Z]+\)\s*-\s*", "", text)
    # Rimuove URL
    text = re.sub(r"http\S+", "", text)
    # Rimuove spazi extra
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    print("--- INIZIO PULIZIA ---")

    # 1. Controllo file
    # Costruiamo il percorso assoluto per evitare errori "File Not Found"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, INPUT_FILE)
    output_path = os.path.join(base_dir, OUTPUT_FILE)

    if not os.path.exists(input_path):
        print(f"ERRORE: Non trovo {INPUT_FILE} in {base_dir}")
        return

    print("Caricamento dataset...")
    df = pd.read_csv(input_path)
    print(f"Righe iniziali: {len(df)}")

    # 2. Pulizia
    print("Riempimento valori vuoti...")
    df['title'] = df['title'].fillna('')
    df['text'] = df['text'].fillna('')

    print("Unione Titolo + Testo...")
    df['full_text'] = df['title'] + " " + df['text']

    print("Rimozione bias fonti (Reuters)...")
    df['clean_text'] = df['full_text'].apply(clean_text_bias)

    print("Rimozione duplicati...")
    df.drop_duplicates(subset=['clean_text'], inplace=True)

    # Filtro: teniamo solo articoli con più di 20 caratteri
    df = df[df['clean_text'].str.len() > 20]

    print(f"Righe finali: {len(df)}")

    # 3. Salvataggio
    # Salviamo solo testo pulito e label (1=Real, 0=Fake)
    df_final = df[['clean_text', 'label']]
    df_final.to_csv(output_path, index=False)
    print(f"Salvato in: {OUTPUT_FILE}")
    print("--- FINE ---")


if __name__ == "__main__":
    main()