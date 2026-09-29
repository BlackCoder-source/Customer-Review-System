from pathlib import Path
from typing import List, Dict, Any
from transformers import pipeline

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models" / "sentiment_model"

if MODEL_DIR.exists():
    MODEL_PATH = str(MODEL_DIR)
else:
    MODEL_PATH = "models/sentiment_model"

classifier = pipeline(
    "text-classification",
    model=MODEL_PATH,
    tokenizer=MODEL_PATH,
    truncation=True,
    max_length=256
)

LABEL_MAP = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive",
    "0": "negative",
    "1": "neutral",
    "2": "positive",
    "NEGATIVE": "negative",
    "NEUTRAL": "neutral",
    "POSITIVE": "positive",
}


def get_sentiment(text: str) -> Dict[str, Any]:
    """Score a single text string with sentiment model."""
    results = classifier([text], truncation=True, max_length=256)
    res = results[0]
    raw_label = str(res.get("label", "")).upper()
    sentiment = LABEL_MAP.get(raw_label, raw_label.lower())
    confidence = float(res.get("score", 0.0))
    return {"sentiment": sentiment, "confidence": confidence}


def get_sentiment_batch(texts: List[str]) -> List[Dict[str, Any]]:
    """Batch score multiple text strings using pipeline batch_size=64."""
    if not texts:
        return []
    results = classifier(texts, batch_size=64, truncation=True, max_length=256)
    output = []
    for res in results:
        raw_label = str(res.get("label", "")).upper()
        sentiment = LABEL_MAP.get(raw_label, raw_label.lower())
        confidence = float(res.get("score", 0.0))
        output.append({"sentiment": sentiment, "confidence": confidence})
    return output
