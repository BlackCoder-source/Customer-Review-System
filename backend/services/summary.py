from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_executive_summary(df):
    top_themes = df["theme"].value_counts().head(5)
    negative_themes = df[df["sentiment"] == 0]["theme"].value_counts().head(3)

    raw_text = (
        f"The top customer complaint themes are: {', '.join(top_themes.index)}. "
        f"Themes showing the most negative sentiment are: {', '.join(negative_themes.index)}. "
        f"Total reviews analyzed: {len(df)}."
    )

    result = summarizer(raw_text, max_length=80, min_length=25, do_sample=False)
    return result[0]["summary_text"]
