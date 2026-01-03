import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
import json
from datetime import datetime


class AIService:
    def __init__(self):
        # Salgo fino alla root del progetto
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../")
        )

        # Percorso reale del modello
        model_path = os.path.join(
            project_root, "FIA", "traning", "fakebuster_model"
        )

        print("MODEL PATH:", model_path)
        print("EXISTS:", os.path.exists(model_path))

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
    def analyze_text(self, text: str):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=256
        )

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)

        score = probs[0][1].item()

        ai_log = {
            "timestamp": datetime.utcnow().isoformat(),
            "model": "xlm-roberta",
            "score": round(score, 3)
        }

        return round(score, 3), json.dumps(ai_log)
