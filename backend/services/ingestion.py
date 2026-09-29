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
        csv_path (Optional[str]): File path to the reviews CSV. If None, defaults to backend/data/reviews.csv.

    Returns:
        pd.DataFrame: Cleaned DataFrame with columns:
            [review_id, text, product, region, date, rating].

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
        ValueError: If required columns are missing from the CSV.
    """
    if csv_path is None:
        base_dir = Path(__file__).resolve().parent.parent
        resolved_path = base_dir / "data" / "reviews.csv"
    else:
        resolved_path = Path(csv_path).resolve()

    if not resolved_path.exists():
        raise FileNotFoundError(f"Review dataset file not found at: {resolved_path}")

    logger.info("Loading review dataset from: %s", resolved_path)
    df = pd.read_csv(resolved_path)

    # Validate required columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"CSV is missing required columns: {missing_cols}")

    # Standardize string fields and clean whitespace
    string_cols = ["review_id", "text", "product", "region"]
    for col in string_cols:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # Drop rows where critical fields 'review_id' or 'text' are empty
    df = df[df["text"].str.len() > 0].copy()
    df = df[df["review_id"].str.len() > 0].copy()

    # Standardize missing product and region values
    df["product"] = df["product"].replace("", "General Product")
    df["region"] = df["region"].replace("", "Global")

    # Standardize date format to YYYY-MM-DD
    # Invalid dates will be coerced and filled with today's date
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
