import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
import json
from datetime import datetime


class AIService:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        model_path = os.path.join(base_dir, "fakebuster_model")

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
