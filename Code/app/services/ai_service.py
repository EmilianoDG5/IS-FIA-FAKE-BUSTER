import re
import torch
import json
from datetime import datetime
from collections import Counter
from langdetect import detect, LangDetectException
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

MODEL_PATH = r"C:\Users\Golde\OneDrive\Desktop\PROGETTI IS-FIA\IS\IS-FAKE-BUSTER\FIA\traning\fakebuster_model"


def clean_text_bias(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_gibberish(text: str) -> bool:
    words = re.findall(r"[a-zàèéìòù]+", text.lower())
    words = [w for w in words if len(set(w)) > 1]

    if len(words) < 6:
        return True

    avg_len = sum(len(w) for w in words) / len(words)
    if avg_len > 15:
        return True

    counts = Counter(text)
    if counts.most_common(1)[0][1] / len(text) > 0.4:
        return True

    return False


class AIService:
    def __init__(self):

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        self.model.eval()

    def analyze_text(self, raw_text: str):
        text = clean_text_bias(raw_text)

        if not text or len(text) < 20:
            return -1.0, json.dumps({"error": "Testo troppo breve o vuoto"})

        if is_gibberish(text):
            return -1.0, json.dumps({"error": "Testo privo di significato"})

        try:
            lang = detect(text)
            if lang not in ["it", "en"]:
                return -1.0, json.dumps({"error": f"Lingua non supportata: {lang}"})
        except LangDetectException:
            return -1.0, json.dumps({"error": "Testo incomprensibile"})

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
            "clean_len": len(text),
            "lang": lang,
            "score": round(score, 3)
        }

        return round(score, 3), json.dumps(ai_log)