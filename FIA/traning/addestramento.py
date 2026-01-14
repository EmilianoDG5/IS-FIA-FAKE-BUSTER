import pandas as pd
import torch
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

import numpy as np
import torch
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def compute_metrics(eval_pred):
    logits, labels = eval_pred

    # Probabilità
    probs = torch.softmax(torch.tensor(logits), dim=1).numpy()

    score_fake = probs[:, 1]          
    THRESHOLD = 0.7                   

    # Decisione come in produzione
    predictions = (score_fake >= THRESHOLD).astype(int)

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        pos_label=0,                  
        average="binary",
        zero_division=0
    )

    accuracy = accuracy_score(labels, predictions)

    return {
        "accuracy": accuracy,
        "precision_real": precision,
        "recall_real": recall,
        "f1_real": f1
    }




def main():
    # Percorsi
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, "WELFake_Cleaned.csv")
    output_model_dir = os.path.join(base_dir, "fakebuster_model")

    # Caricamento dataset
    df = pd.read_csv(dataset_path)
    df["label"] = df["label"].apply(lambda x: 1 if x == 0 else 0)
    MAX_SAMPLES = 1000
    
    df = df.groupby("label", group_keys=False)\
     .apply(lambda x: x.sample(n=500, random_state=42))
    print(f"Avvio training su {len(df)} articoli...")

    train_texts, val_texts, train_labels, val_labels = train_test_split(
        df['clean_text'].tolist(),
        df['label'].tolist(),
        test_size=0.2,
        random_state=42
    )

    # Modello
    model_name = "xlm-roberta-base"
    print(f"Caricamento modello {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Tokenizzazione
    print("Tokenizzazione in corso...")
    train_encodings = tokenizer(
        train_texts,
        truncation=True,
        padding=True,
        max_length=512
    )
    val_encodings = tokenizer(
        val_texts,
        truncation=True,
        padding=True,
        max_length=512
    )

    class FakeNewsDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels

        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            item["labels"] = torch.tensor(self.labels[idx])
            return item

        def __len__(self):
            return len(self.labels)

    train_dataset = FakeNewsDataset(train_encodings, train_labels)
    val_dataset = FakeNewsDataset(val_encodings, val_labels)

    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=2
    )

    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=4,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        do_eval=True,
        eval_steps=500,
        logging_dir="./logs",
        logging_steps=50,
        save_strategy="no"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    print(" INIZIO ADDESTRAMENTO...")
    trainer.train()

    print(" VALUTAZIONE FINALE")
    metrics = trainer.evaluate()
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")

    print(f"Salvataggio modello in {output_model_dir}...")
    model.save_pretrained(output_model_dir)
    tokenizer.save_pretrained(output_model_dir)

    print("ADDESTRAMENTO COMPLETATO!")


if __name__ == "__main__":
    main()
