"""Sentiment-model validation service.

Holds a small, manually-labelled holdout sample of reviews and
compares the sentiment model's predicted labels against the ground-
truth labels to compute an accuracy score.

The holdout set covers each sentiment class (positive / neutral /
negative) and each product, giving a representative micro-benchmark
without needing a separate CSV file.

Public API
----------
run_validation() -> ValidationResult
    Runs the sentiment model on the holdout texts, compares the
    output to the gold labels, and returns a ``ValidationResult``
    dict containing accuracy, per-class counts, and mismatches.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, TypedDict

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Manually-labelled holdout sample
# Each entry: (review_id, text, rating, gold_label)
# Labels must be  "positive" | "neutral" | "negative"
# ---------------------------------------------------------------------------
_HOLDOUT_SAMPLES: List[Dict[str, Any]] = [
    # ── Positive ────────────────────────────────────────────────────────────
    {
        "review_id": "HO-001",
        "text": "Exceptional build quality and very snappy interface! Battery life easily lasts 3 full days. Highly recommended.",
        "rating": 5.0,
        "gold_label": "positive",
    },
    {
        "review_id": "HO-002",
        "text": "Fast shipping! Arrived 2 days earlier than scheduled in pristine condition. Great packaging.",
        "rating": 5.0,
        "gold_label": "positive",
    },
    {
        "review_id": "HO-003",
        "text": "Great product overall. The display is crisp and legible under direct sunlight. Setup was seamless.",
        "rating": 4.0,
        "gold_label": "positive",
    },
    {
        "review_id": "HO-004",
        "text": "Representative was polite and resolved my warranty claim within 10 minutes. Stellar customer service.",
        "rating": 5.0,
        "gold_label": "positive",
    },
    {
        "review_id": "HO-005",
        "text": "Cloud sync is lightning fast and effortless across MacBook and Windows workstation. Loving the new update.",
        "rating": 5.0,
        "gold_label": "positive",
    },
    {
        "review_id": "HO-006",
        "text": "Active Noise Cancellation is world-class. Cuts out airplane cabin noise completely. Super comfy ear pads.",
        "rating": 5.0,
        "gold_label": "positive",
    },
    {
        "review_id": "HO-007",
        "text": "Seamless onboarding and clean intuitive dashboard. Our entire marketing team adopted it easily.",
        "rating": 5.0,
        "gold_label": "positive",
    },
    {
        "review_id": "HO-008",
        "text": "Reliable smartwatch with accurate heart rate tracking and sleep metrics. Good value for money.",
        "rating": 4.0,
        "gold_label": "positive",
    },
    {
        "review_id": "HO-009",
        "text": "Customer care team went above and beyond to replace my damaged charging cable without hassle.",
        "rating": 5.0,
        "gold_label": "positive",
    },
    # ── Neutral ─────────────────────────────────────────────────────────────
    {
        "review_id": "HO-010",
        "text": "Fairly average wireless earbuds. Sound is decent, but nothing extraordinary for this price tier.",
        "rating": 3.0,
        "gold_label": "neutral",
    },
    {
        "review_id": "HO-011",
        "text": "Monthly plan is reasonable, but enterprise pricing tier is extortionate for small teams.",
        "rating": 3.0,
        "gold_label": "neutral",
    },
    {
        "review_id": "HO-012",
        "text": "Expensive initial purchase, but frequent discounts and bundle sales make it acceptable.",
        "rating": 3.0,
        "gold_label": "neutral",
    },
    # ── Negative ────────────────────────────────────────────────────────────
    {
        "review_id": "HO-013",
        "text": "The delivery was delayed by over two weeks. When the package arrived, the outer box was completely crushed.",
        "rating": 1.0,
        "gold_label": "negative",
    },
    {
        "review_id": "HO-014",
        "text": "Customer support took 4 days to respond to my ticket, and then closed it without resolving the firmware glitch.",
        "rating": 2.0,
        "gold_label": "negative",
    },
    {
        "review_id": "HO-015",
        "text": "The subscription pricing skyrocketed overnight without notice. Hidden fees make this unusable.",
        "rating": 1.0,
        "gold_label": "negative",
    },
    {
        "review_id": "HO-016",
        "text": "Software crashed twice while editing high-resolution files. Lost 30 minutes of work. Urgent bugfix needed.",
        "rating": 2.0,
        "gold_label": "negative",
    },
    {
        "review_id": "HO-017",
        "text": "The charging case stopped working after three weeks. Very cheap plastic materials used.",
        "rating": 1.0,
        "gold_label": "negative",
    },
    {
        "review_id": "HO-018",
        "text": "Courier dropped package in the driveway under pouring rain. Product got wet and damaged.",
        "rating": 1.0,
        "gold_label": "negative",
    },
    {
        "review_id": "HO-019",
        "text": "Phone support was offline during advertised working hours. Left waiting with zero assistance.",
        "rating": 1.0,
        "gold_label": "negative",
    },
    {
        "review_id": "HO-020",
        "text": "The latest firmware update ruined the battery life completely. It drains in hours.",
        "rating": 1.0,
        "gold_label": "negative",
    },
]


class MismatchDetail(TypedDict):
    review_id: str
    text: str
    gold_label: str
    predicted_label: str


class ValidationResult(TypedDict):
    total_samples: int
    correct: int
    accuracy: float
    per_class: Dict[str, Dict[str, int]]  # {gold: {correct, total}}
    mismatches: List[MismatchDetail]


def run_validation() -> ValidationResult:
    """Run the sentiment model against the holdout sample and return metrics.

    Uses the same ``analyze_sentiment`` function (HuggingFace pipeline
    with lexicon fallback) that the main pipeline uses so results are
    directly comparable.

    Returns:
        ValidationResult dict with accuracy, per-class breakdown, and
        a list of mismatched samples for debugging.
    """
    import pandas as pd
    from services.sentiment import analyze_sentiment  # local import avoids circular dep

    # Build a DataFrame that mirrors what the main pipeline produces
    df = pd.DataFrame(
        [
            {
                "review_id": s["review_id"],
                "text": s["text"],
                "rating": s["rating"],
                "gold_label": s["gold_label"],
                # Dummy columns required by analyze_sentiment (not used for scoring)
                "product": "Validation",
                "region": "Global",
                "date": "2026-01-01",
            }
            for s in _HOLDOUT_SAMPLES
        ]
    )

    logger.info("Running sentiment validation on %d holdout samples …", len(df))
    scored_df = analyze_sentiment(df)

    # ── Metrics ──────────────────────────────────────────────────────────────
    total = len(scored_df)
    correct = 0
    per_class: Dict[str, Dict[str, int]] = {}
    mismatches: List[MismatchDetail] = []

    for _, row in scored_df.iterrows():
        gold = str(row["gold_label"])
        predicted = str(row["sentiment"])

        if gold not in per_class:
            per_class[gold] = {"correct": 0, "total": 0}
        per_class[gold]["total"] += 1

        if predicted == gold:
            correct += 1
            per_class[gold]["correct"] += 1
        else:
            mismatches.append(
                MismatchDetail(
                    review_id=str(row["review_id"]),
                    text=str(row["text"]),
                    gold_label=gold,
                    predicted_label=predicted,
                )
            )

    accuracy = round(correct / total, 4) if total > 0 else 0.0
    logger.info(
        "Validation complete – accuracy %.2f%% (%d/%d correct).",
        accuracy * 100,
        correct,
        total,
    )

    return ValidationResult(
        total_samples=total,
        correct=correct,
        accuracy=accuracy,
        per_class=per_class,
        mismatches=mismatches,
    )
