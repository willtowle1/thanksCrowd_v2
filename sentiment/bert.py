import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "finiteautomata/bertweet-base-sentiment-analysis"
CLASSES = ["NEG", "NEU", "POS"]

class SentimentAnalyzer:
    def __init__(self) -> None:
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    def analyze(self, content: str) -> bool:
    
        inputs = self.tokenizer(content, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
                logits = self.model(**inputs).logits
            
        predicted_class = torch.argmax(logits, dim=1).item()

        return predicted_class == len(CLASSES)-1