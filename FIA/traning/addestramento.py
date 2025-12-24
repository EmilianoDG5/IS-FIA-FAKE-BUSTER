


import pandas as pd
import torch
import os
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments


def main():
    # Percorsi corretti
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, "WELFake_Cleaned.csv")

    # Percorso dove salvare il modello 

    output_model_dir = os.path.join(base_dir, "fakebuster_model")


    df = pd.read_csv(dataset_path)
    MAX_SAMPLES = 20000
    df = df.sample(n=MAX_SAMPLES, random_state=42)
    

    print(f"Avvio training su {len(df)} articoli...")

    # Divisione Train/Test
    # Usiamo la colonna 'clean_text' creata dallo script di pulizia
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        df['clean_text'].tolist(), df['label'].tolist(), test_size=0.2
    )

    # Preparazione AI Multilingua (XLM-RoBERTa)
    model_name = "xlm-roberta-base"
    print(f"Scaricamento modello {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    print("Tokenizzazione in corso (può richiedere tempo)...")
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=512)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=512)

    class FakeNewsDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels

        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            item['labels'] = torch.tensor(self.labels[idx])
            return item

        def __len__(self):
            return len(self.labels)

    train_dataset = FakeNewsDataset(train_encodings, train_labels)
    val_dataset = FakeNewsDataset(val_encodings, val_labels)

    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    # Parametri di training
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=2,  # 2 Giri completi di studio
        per_device_train_batch_size=4,  # Abbassa a 2 se dà errore di memoria
        logging_dir='./logs',
        logging_steps=50,
        save_strategy="no"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    print("INIZIO ADDESTRAMENTO...")
    trainer.train()

    print(f"Salvataggio modello in {output_model_dir}...")
    model.save_pretrained(output_model_dir)
    tokenizer.save_pretrained(output_model_dir)
    print("ADDESTRAMENTO COMPLETATO!")


if __name__ == "__main__":
    main()