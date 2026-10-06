import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

key = os.environ["AZURE_LANGUAGE_KEY"]
endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_azure_sentiment(text: str):
    response = client.analyze_sentiment([text])[0]
    return {
        "sentiment": response.sentiment,  # "positive", "negative", "neutral", or "mixed"
        "confidence": {
            "positive": response.confidence_scores.positive,
            "neutral": response.confidence_scores.neutral,
            "negative": response.confidence_scores.negative,
        }
    }

def get_azure_sentiment_batch(texts: list[str]):
    # Azure allows up to 10 documents per batch call on free tier
    results = []
    for i in range(0, len(texts), 10):
        batch = texts[i:i+10]
        response = client.analyze_sentiment(batch)
        for doc in response:
            results.append({
                "sentiment": doc.sentiment,
                "confidence": {
                    "positive": doc.confidence_scores.positive,
                    "neutral": doc.confidence_scores.neutral,
                    "negative": doc.confidence_scores.negative,
                }
            })
    return results
