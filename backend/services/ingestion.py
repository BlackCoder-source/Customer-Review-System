from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

REVIEWS_CSV_PATH = BASE_DIR / "data" / "reviews_scored_final.csv"
if not REVIEWS_CSV_PATH.exists():
    REVIEWS_CSV_PATH = Path("backend/data/reviews_scored_final.csv")

EVENTS_CSV_PATH = BASE_DIR / "data" / "events.csv"
if not EVENTS_CSV_PATH.exists():
    EVENTS_CSV_PATH = Path("backend/data/events.csv")

LABEL_MAP = {
    0: "negative",
    1: "neutral",
    2: "positive",
    "0": "negative",
    "1": "neutral",
    "2": "positive",
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive",
}

_reviews_df_cache = None
_events_df_cache = None


def load_reviews() -> pd.DataFrame:
    """Reads backend/data/reviews_scored_final.csv with pandas, parsing 'date' column as datetime."""
    global _reviews_df_cache
    if _reviews_df_cache is not None:
        return _reviews_df_cache

    df = pd.read_csv(REVIEWS_CSV_PATH)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if "sentiment" in df.columns:
        df["sentiment_num"] = pd.to_numeric(df["sentiment"], errors="coerce")
        df["sentiment"] = df["sentiment"].map(lambda x: LABEL_MAP.get(x, str(x)))
    _reviews_df_cache = df
    return _reviews_df_cache


def load_events() -> pd.DataFrame:
    """Reads backend/data/events.csv with pandas, parsing 'date' column as datetime."""
    global _events_df_cache
    if _events_df_cache is not None:
        return _events_df_cache

    df = pd.read_csv(EVENTS_CSV_PATH)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    _events_df_cache = df
    return _events_df_cache


# Cache both in memory at module load
reviews_df = load_reviews()
events_df = load_events()
