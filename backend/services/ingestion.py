"""Data ingestion and preprocessing module for customer reviews.

Loads reviews from a CSV file, cleans missing values, standardizes date formats,
validates columns, and ensures proper numerical data types.
"""

from pathlib import Path
from typing import Optional
import logging
import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = ["review_id", "text", "product", "region", "date", "rating"]


def load_and_clean_reviews(csv_path: Optional[str] = None) -> pd.DataFrame:
    """Load reviews from a CSV file, sanitize missing values, and standardize date format.

    Args:
        csv_path (Optional[str]): File path to the reviews CSV. If None, checks available data files.

    Returns:
        pd.DataFrame: Cleaned DataFrame with standardized columns.
    """
    if csv_path is None:
        base_dir = Path(__file__).resolve().parent.parent
        candidates = ["reviews_scored_final.csv", "reviews_scored.csv", "reviews.csv"]
        resolved_path = None
        for cand in candidates:
            p = base_dir / "data" / cand
            if p.exists():
                resolved_path = p
                break
        if resolved_path is None:
            resolved_path = base_dir / "data" / "reviews.csv"
    else:
        resolved_path = Path(csv_path).resolve()

    if not resolved_path.exists():
        raise FileNotFoundError(f"Review dataset file not found at: {resolved_path}")

    logger.info("Loading review dataset from: %s", resolved_path)
    df = pd.read_csv(resolved_path)

    # Standardize column mappings if loading pre-scored dataset
    col_mapping = {}
    if "ProductId" in df.columns and "product" not in df.columns:
        df["product"] = df["ProductId"]
    if "Score" in df.columns and "rating" not in df.columns:
        df["rating"] = df["Score"]
    if "topic_id" in df.columns and "theme_id" not in df.columns:
        df["theme_id"] = df["topic_id"].astype(str)
    if "theme" in df.columns and "theme_name" not in df.columns:
        df["theme_name"] = df["theme"].astype(str)
    if "review_id" not in df.columns:
        prod = df["product"] if "product" in df.columns else "REV"
        df["review_id"] = prod.astype(str) + "-" + df.index.astype(str)

    # Standardize sentiment column
    if "sentiment" in df.columns:
        sent_map = {0: "negative", 1: "neutral", 2: "positive", "0": "negative", "1": "neutral", "2": "positive"}
        df["sentiment"] = df["sentiment"].map(sent_map).fillna(df["sentiment"].astype(str).str.lower())
        # Clean up any residual numeric strings
        df["sentiment"] = df["sentiment"].replace({"0": "negative", "1": "neutral", "2": "positive"})

    if "sentiment_score" not in df.columns and "confidence" in df.columns:
        df["sentiment_score"] = pd.to_numeric(df["confidence"], errors="coerce").fillna(0.8)

    # Validate required columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"CSV is missing required columns: {missing_cols}")

    # Standardize string fields and clean whitespace
    string_cols = ["review_id", "text", "product", "region"]
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip()

    # Drop rows where critical fields 'review_id' or 'text' are empty
    df = df[df["text"].str.len() > 0].copy()
    df = df[df["review_id"].str.len() > 0].copy()

    # Standardize missing product and region values
    df["product"] = df["product"].replace("", "General Product")
    if "region" not in df.columns or df["region"].isnull().all():
        df["region"] = "Global"
    else:
        df["region"] = df["region"].replace("", "Global")

    # Standardize date format to YYYY-MM-DD
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    today_str = pd.Timestamp.now().strftime("%Y-%m-%d")
    df["date"] = df["date"].dt.strftime("%Y-%m-%d").fillna(today_str)

    # Standardize rating to float between 1.0 and 5.0
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(3.0)
    df["rating"] = df["rating"].clip(lower=1.0, upper=5.0)

    # Deduplicate review_id if present
    df = df.drop_duplicates(subset=["review_id"]).reset_index(drop=True)

    logger.info("Successfully ingested and cleaned %d reviews.", len(df))
    return df
