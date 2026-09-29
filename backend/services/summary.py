"""Executive summary generation service.

Generates a concise plain-language executive summary directly from the
processed reviews DataFrame without requiring an external ML model.
This ensures fast, reliable operation regardless of the installed
transformers version.
"""

import pandas as pd


# Dummy sentinel kept for backwards-compatible import in main.py
summarizer = None


def generate_executive_summary(df: pd.DataFrame) -> str:
    """Generate a data-driven executive summary from the reviews DataFrame.

    Args:
        df: Processed reviews DataFrame with columns: theme_name, sentiment,
            product, region, rating, date.

    Returns:
        A concise multi-sentence executive summary string.
    """
    if df.empty:
        return "No review data is currently available to summarise."

    total = len(df)

    # --- Sentiment breakdown ---
    sentiment_counts = df["sentiment"].value_counts()
    pos = int(sentiment_counts.get("positive", 0))
    neg = int(sentiment_counts.get("negative", 0))
    neu = int(sentiment_counts.get("neutral", 0))
    pos_pct = round((pos / total) * 100)
    neg_pct = round((neg / total) * 100)

    # --- Theme analysis ---
    theme_col = "theme_name" if "theme_name" in df.columns else "theme"
    top_themes = df[theme_col].value_counts().head(3)
    top_theme_name = top_themes.index[0] if len(top_themes) > 0 else "Unknown"

    # Most negative themes
    neg_df = df[df["sentiment"] == "negative"]
    if not neg_df.empty:
        neg_theme = neg_df[theme_col].value_counts().index[0]
        neg_theme_count = int(neg_df[theme_col].value_counts().iloc[0])
    else:
        neg_theme = None
        neg_theme_count = 0

    # --- Rating ---
    avg_rating = None
    if "rating" in df.columns:
        try:
            avg_rating = round(float(df["rating"].mean()), 1)
        except Exception:
            pass

    # --- Top product / region ---
    top_product = None
    if "product" in df.columns:
        prod_counts = df["product"].value_counts()
        if not prod_counts.empty:
            top_product = prod_counts.index[0]

    top_region = None
    if "region" in df.columns:
        region_counts = df["region"].value_counts()
        if not region_counts.empty:
            top_region = region_counts.index[0]

    # --- Build summary sentences ---
    sentences = []

    # Sentence 1: volume + overall sentiment
    sentiment_tone = "broadly positive" if pos_pct >= 60 else ("mixed" if pos_pct >= 40 else "predominantly negative")
    sentences.append(
        f"Across {total:,} customer reviews analysed, sentiment is {sentiment_tone} "
        f"with {pos_pct}% positive and {neg_pct}% negative feedback."
    )

    # Sentence 2: top theme
    sentences.append(
        f"The most discussed theme is '{top_theme_name}', which accounts for the largest share of customer mentions."
    )

    # Sentence 3: key concern
    if neg_theme and neg_theme_count > 0:
        sentences.append(
            f"The primary area of concern is '{neg_theme}', which drives {neg_theme_count} negative reviews "
            f"and warrants immediate investigation."
        )

    # Sentence 4: rating context
    if avg_rating is not None:
        rating_label = "strong" if avg_rating >= 4 else ("acceptable" if avg_rating >= 3 else "below expectations")
        sentences.append(
            f"Average customer rating stands at {avg_rating} out of 5, indicating {rating_label} overall satisfaction."
        )

    # Sentence 5: geographic / product focus
    if top_product and top_region:
        sentences.append(
            f"Feedback is most concentrated around '{top_product}' in the {top_region}, "
            f"making these the priority focus for follow-up action."
        )

    return " ".join(sentences)
