from transformers import pipeline
import re

class SimpleDetector:
    def __init__(self):
        self.nlp = pipeline("zero-shot-classification",
                            model="facebook/bart-large-mnli")
        self.labels = ["Human", "AI", "Deepfake", "Manipulated"]

    def analyze(self, text):
        """
        Возвращает детальный словарь:
        - label: Human / AI
        - probability: float
        - sources: список найденных источников
        - signs_of_falsification: список признаков
        - final_decision: Human / AI / Possibly Manipulated
        """
        res = self.nlp(text, self.labels)
        label = res['labels'][0]
        probability = res['scores'][0]

        url_pattern = r'(https?://[^\s]+|www\.[^\s]+)'
        sources = re.findall(url_pattern, text)

        signs = []
        if any(w in text.lower() for w in ["deepfake","generated","ai"]):
            signs.append("AI generated content detected")
        if any(w in text.lower() for w in ["manipulated","edited","photoshopped"]):
            signs.append("Manipulation detected")

        if "AI generated content detected" in signs or label in ["AI", "Deepfake"]:
            final_decision = "AI / Possibly Manipulated"
        else:
            final_decision = "Human"

        return {
            "label": label,
            "probability": round(probability, 4),
            "sources": sources,
            "signs_of_falsification": signs,
            "final_decision": final_decision
        }

    @staticmethod
    def load():
        return SimpleDetector()
