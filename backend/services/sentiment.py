"""Sentiment analysis service using Hugging Face transformers.

Scores customer reviews into positive, negative, or neutral categories using
'distilbert-base-uncased-finetuned-sst-2-english', accompanied by confidence scores.
Includes a sentiment lexicon fallback when running offline or downloading models.
"""

from typing import List, Dict, Tuple
import logging
import re
import pandas as pd

logger = logging.getLogger(__name__)

# Fallback lexicon scoring keywords for offline / lightweight execution
POSITIVE_WORDS = {
    "great", "excellent", "seamless", "stellar", "loving", "recommend", "recommended",
    "fast", "pristine", "snappy", "reliable", "comfy", "good", "beyond", "polite",
    "accurate", "intuitive", "helpful", "clean", "world-class"
}
NEGATIVE_WORDS = {
    "delayed", "crushed", "closed", "unresolved", "glitch", "crash", "crashed",
    "hidden", "unusable", "overpriced", "cheap", "broken", "broke", "terrible",
    "extortionate", "unhelpful", "offline", "disappointing", "damage", "damaged",
    "poor", "bad", "worst"
}


def _heuristic_sentiment(text: str, rating: float) -> Tuple[str, float]:
    """Calculate sentiment and confidence score from review text and user rating."""
    lowered = text.lower()
    words = set(re.findall(r"\b\w+\b", lowered))

    pos_count = len(words.intersection(POSITIVE_WORDS))
    neg_count = len(words.intersection(NEGATIVE_WORDS))

    if rating >= 4.0 or pos_count > neg_count + 1:
        sentiment = "positive"
        score = 0.85 + min(0.14, 0.03 * pos_count)
    elif rating <= 2.0 or neg_count > pos_count + 1:
        sentiment = "negative"
        score = 0.85 + min(0.14, 0.03 * neg_count)
    else:
        sentiment = "neutral"
        score = 0.70 + 0.10 * (1.0 if rating == 3.0 else 0.5)

    return sentiment, round(float(score), 4)


def _predict_with_hf_pipeline(texts: List[str]) -> List[Dict[str, float]]:
    """Predict sentiment labels and scores using Hugging Face pipeline.

    Model: distilbert-base-uncased-finetuned-sst-2-english
    """
    from transformers import pipeline

    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    logger.info("Initializing Hugging Face sentiment pipeline with %s...", model_name)
    classifier = pipeline(
        "sentiment-analysis",
        model=model_name,
        tokenizer=model_name,
        truncation=True
    )
    results = classifier(texts)
    return results


def analyze_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """Classify sentiment (positive/negative/neutral) and compute confidence score.

    Uses distilbert-base-uncased-finetuned-sst-2-english with a neutral score threshold.
    Falls back gracefully to lexicon-based scoring if the model is not cached or fails.

    Args:
        df (pd.DataFrame): DataFrame with 'text' and 'rating' columns.

    Returns:
        pd.DataFrame: Updated DataFrame with 'sentiment' and 'sentiment_score'.
    """
    logger.info("Running sentiment analysis for %d reviews...", len(df))
    df_copy = df.copy()

    try:
        texts = df_copy["text"].tolist()
        raw_preds = _predict_with_hf_pipeline(texts)

        sentiments = []
        scores = []
        for i, pred in enumerate(raw_preds):
            label = pred.get("label", "").upper()
            raw_score = float(pred.get("score", 0.0))

            # DistilBERT outputs POSITIVE / NEGATIVE; low-confidence predictions or 3-star ratings classify as neutral
            rating = float(df_copy.iloc[i].get("rating", 3.0))
            if raw_score < 0.60 or (rating == 3.0 and raw_score < 0.75):
                sentiment = "neutral"
                score = round(1.0 - raw_score, 4) if raw_score > 0.5 else round(raw_score, 4)
            elif "POS" in label:
                sentiment = "positive"
                score = round(raw_score, 4)
            else:
                sentiment = "negative"
                score = round(raw_score, 4)

            sentiments.append(sentiment)
            scores.append(score)

        df_copy["sentiment"] = sentiments
        df_copy["sentiment_score"] = scores
        logger.info("Hugging Face sentiment analysis completed successfully.")
        return df_copy
    except Exception as exc:
        logger.warning(
            "Hugging Face pipeline unavailable (%s). Falling back to lexicon sentiment analyzer.",
            exc
        )
        sentiments = []
        scores = []
        for _, row in df_copy.iterrows():
            sentiment, score = _heuristic_sentiment(row["text"], float(row.get("rating", 3.0)))
            sentiments.append(sentiment)
            scores.append(score)

        df_copy["sentiment"] = sentiments
        df_copy["sentiment_score"] = scores
        return df_copy
