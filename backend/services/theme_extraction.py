"""Theme extraction service using sentence-transformers and BERTopic.

Embeds customer reviews using 'all-MiniLM-L6-v2', clusters them into representative
themes using BERTopic, and assigns theme IDs and human-readable names to each review.
Includes a lightweight rule/keyword fallback when heavy ML libraries are downloading
or unavailable.
"""

from typing import Tuple, List, Dict
import logging
import re
import pandas as pd

logger = logging.getLogger(__name__)

# Heuristic topic map used for initial naming or fallback mode
FALLBACK_TOPICS = [
    {
        "id": "delivery",
        "name": "Delivery & Logistics",
        "keywords": ["delivery", "shipping", "courier", "package", "arrived", "delay", "shipped", "box", "driveway"]
    },
    {
        "id": "pricing",
        "name": "Pricing & Billing",
        "keywords": ["price", "pricing", "subscription", "expensive", "fee", "tier", "overpriced", "cost", "money", "discounts"]
    },
    {
        "id": "support",
        "name": "Customer Support",
        "keywords": ["support", "agent", "ticket", "service", "representative", "bot", "care", "phone", "help", "warranty"]
    },
    {
        "id": "quality",
        "name": "Product Quality & Hardware",
        "keywords": ["battery", "build", "screen", "display", "plastic", "broke", "case", "strap", "hardware", "charging", "earbuds", "ear"]
    },
    {
        "id": "software",
        "name": "Software & Performance",
        "keywords": ["crash", "sync", "bug", "software", "glitch", "connectivity", "bluetooth", "interface", "firmware", "update"]
    }
]


def _match_heuristic_theme(text: str) -> Tuple[str, str]:
    """Classify review text into a theme based on keyword frequency."""
    lowered = text.lower()
    best_id = "general"
    best_name = "General Feedback"
    max_matches = 0

    for topic in FALLBACK_TOPICS:
        matches = sum(1 for kw in topic["keywords"] if re.search(rf"\b{kw}\b", lowered))
        if matches > max_matches:
            max_matches = matches
            best_id = topic["id"]
            best_name = topic["name"]

    return best_id, best_name


def _cluster_with_bertopic(df: pd.DataFrame) -> pd.DataFrame:
    """Cluster reviews using sentence-transformers (all-MiniLM-L6-v2) and BERTopic.

    Args:
        df (pd.DataFrame): DataFrame containing review text.

    Returns:
        pd.DataFrame: DataFrame with 'theme_id' and 'theme_name' assigned.
    """
    from sentence_transformers import SentenceTransformer
    from bertopic import BERTopic

    logger.info("Initializing sentence-transformer (all-MiniLM-L6-v2)...")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    docs = df["text"].tolist()
    embeddings = embedding_model.encode(docs, show_progress_bar=False)

    logger.info("Fitting BERTopic clustering on %d documents...", len(docs))
    # Configure BERTopic with minimal cluster size suitable for smaller datasets
    min_size = min(3, max(2, len(docs) // 6))
    topic_model = BERTopic(
        embedding_model=embedding_model,
        min_topic_size=min_size,
        calculate_probabilities=False,
        verbose=False
    )
    topics, _ = topic_model.fit_transform(docs, embeddings)

    theme_ids = []
    theme_names = []

    # Map BERTopic topic IDs to readable names
    topic_info = topic_model.get_topic_info()
    topic_name_lookup: Dict[int, str] = {}
    for _, row in topic_info.iterrows():
        t_id = row["Topic"]
        custom_name = row.get("Name", f"Theme {t_id}")
        # Clean default BERTopic name format (e.g. "-1_shipping_delivery_package")
        clean_name = " ".join([w.capitalize() for w in custom_name.split("_")[1:3]]) if "_" in custom_name else custom_name
        topic_name_lookup[t_id] = clean_name or f"Topic {t_id}"

    for idx, (t_id, doc_text) in enumerate(zip(topics, docs)):
        if t_id == -1:
            # Outlier in BERTopic: match with heuristic keyword mapper
            fallback_id, fallback_name = _match_heuristic_theme(doc_text)
            theme_ids.append(fallback_id)
            theme_names.append(fallback_name)
        else:
            raw_title = topic_name_lookup.get(t_id, f"Theme {t_id}")
            theme_slug = f"theme-{t_id}"
            theme_ids.append(theme_slug)
            theme_names.append(raw_title)

    df["theme_id"] = theme_ids
    df["theme_name"] = theme_names
    return df


def extract_themes(df: pd.DataFrame) -> pd.DataFrame:
    """Assign cluster themes to all reviews.

    Attempts to run BERTopic with all-MiniLM-L6-v2 embeddings. If dependencies or
    large weights cannot be initialized in the local runtime, seamlessly falls back
    to robust keyword-driven topic clustering without interrupting service.

    Args:
        df (pd.DataFrame): Ingested reviews DataFrame.

    Returns:
        pd.DataFrame: DataFrame updated with 'theme_id' and 'theme_name' columns.
    """
    logger.info("Extracting themes for %d reviews...", len(df))
    df_copy = df.copy()

    try:
        df_copy = _cluster_with_bertopic(df_copy)
        logger.info("BERTopic theme extraction completed successfully.")
        return df_copy
    except Exception as exc:
        logger.warning(
            "BERTopic initialization unavailable or failed (%s). Using rule-based theme extractor.",
            exc
        )
        theme_ids = []
        theme_names = []
        for text in df_copy["text"]:
            t_id, t_name = _match_heuristic_theme(text)
            theme_ids.append(t_id)
            theme_names.append(t_name)

        df_copy["theme_id"] = theme_ids
        df_copy["theme_name"] = theme_names
        return df_copy
