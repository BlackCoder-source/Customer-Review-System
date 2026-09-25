"""FastAPI backend application for Customer Review Intelligence.

Exposes RESTful endpoints for health inspection, dashboard aggregates,
theme summaries, theme details with review previews, and full reviews by theme.
Configured with CORS for React / Vite frontend consumption.
"""

from typing import Dict, Any, List
from contextlib import asynccontextmanager
import logging
import pandas as pd
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import (
    HealthResponse,
    DashboardSummaryResponse,
    ThemesListResponse,
    ThemeDetailResponse,
    ThemeReviewsResponse,
    ThemeSummaryItem,
    SentimentBreakdown,
    ReviewItem,
    AlertsListResponse,
    AlertItem,
    ValidationResponse,
)
from services.ingestion import load_and_clean_reviews
from services.theme_extraction import extract_themes
from services.sentiment import analyze_sentiment
from services.detection import detect_early_issues
from services.root_cause import find_root_cause
from services.pii_redaction import redact_text
from services.validation import run_validation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("backend.main")

# In-memory storage for processed customer review intelligence
reviews_cache: Dict[str, Any] = {
    "df": pd.DataFrame(),
    "initialized": False
}


def compute_sentiment_breakdown(df_subset: pd.DataFrame) -> SentimentBreakdown:
    """Calculate counts and percentage distribution of sentiment in a reviews subset.

    Args:
        df_subset (pd.DataFrame): DataFrame containing 'sentiment' column.

    Returns:
        SentimentBreakdown: Breakdown of positive, neutral, and negative counts and percentages.
    """
    total = len(df_subset)
    if total == 0:
        return SentimentBreakdown(
            positive=0, neutral=0, negative=0,
            positive_pct=0.0, neutral_pct=0.0, negative_pct=0.0
        )

    counts = df_subset["sentiment"].value_counts().to_dict()
    pos = int(counts.get("positive", 0))
    neu = int(counts.get("neutral", 0))
    neg = int(counts.get("negative", 0))

    return SentimentBreakdown(
        positive=pos,
        neutral=neu,
        negative=neg,
        positive_pct=round((pos / total) * 100, 1),
        neutral_pct=round((neu / total) * 100, 1),
        negative_pct=round((neg / total) * 100, 1),
    )


def compute_severity(complaint_count: int, total_theme_reviews: int) -> str:
    """Determine complaint severity tier based on volume and ratio.

    Args:
        complaint_count (int): Negative review count.
        total_theme_reviews (int): Total review count for theme.

    Returns:
        str: 'high', 'medium', or 'low'
    """
    if complaint_count >= 3 or (total_theme_reviews > 0 and (complaint_count / total_theme_reviews) >= 0.5):
        return "high"
    elif complaint_count >= 1:
        return "medium"
    return "low"


def row_to_review_item(row: pd.Series) -> ReviewItem:
    """Map a DataFrame row to a Pydantic ReviewItem model.

    Args:
        row (pd.Series): Review record row.

    Returns:
        ReviewItem: Validated review model.
    """
    return ReviewItem(
        review_id=str(row["review_id"]),
        text=str(row["text"]),
        product=str(row["product"]),
        region=str(row["region"]),
        date=str(row["date"]),
        rating=float(row["rating"]),
        theme_id=str(row["theme_id"]),
        theme_name=str(row["theme_name"]),
        sentiment=str(row["sentiment"]),
        sentiment_score=float(row["sentiment_score"]),
    )



def filter_reviews(df: pd.DataFrame, product: Optional[str] = None, region: Optional[str] = None, date: Optional[str] = None) -> pd.DataFrame:
    if df.empty:
        return df
    if product:
        df = df[df["product"] == product]
    if region:
        df = df[df["region"] == region]
    if date:
        df = df[df["date"] == date]
    return df

def process_and_cache_dataset() -> pd.DataFrame:
    """Execute end-to-end ingestion, theme clustering, and sentiment scoring."""
    logger.info("Initializing dataset pipeline...")
    cleaned_df = load_and_clean_reviews()
    themed_df = extract_themes(cleaned_df)
    scored_df = analyze_sentiment(themed_df)
    
    logger.info("Detecting early issues...")
    alerts = detect_early_issues(scored_df)
    
    for alert in alerts:
        alert['root_cause'] = find_root_cause(alert)
        
    reviews_cache["df"] = scored_df
    reviews_cache["alerts"] = alerts
    reviews_cache["initialized"] = True
    logger.info("Dataset successfully processed and cached (%d rows). Detected %d alerts.", len(scored_df), len(alerts))
    return scored_df


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup and shutdown procedures."""
    logger.info("Starting up Customer Review Intelligence Backend...")
    try:
        process_and_cache_dataset()
    except Exception as exc:
        logger.error("Failed to initialize dataset pipeline on startup: %s", exc)
    yield
    logger.info("Shutting down Customer Review Intelligence Backend.")


app = FastAPI(
    title="Customer Review Intelligence API",
    description="Backend API for customer review ingestion, BERTopic theme extraction, and sentiment scoring.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for React frontend (Vite default :5173, Create-React-App :3000, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    tags=["System"]
)
def health_check() -> HealthResponse:
    """Return system health status and total loaded review count."""
    df = reviews_cache.get("df", pd.DataFrame())
    return HealthResponse(
        status="ok",
        version="1.0.0",
        total_reviews_loaded=len(df)
    )


@app.get(
    "/dashboard/summary",
    response_model=DashboardSummaryResponse,
    summary="Dashboard Summary",
    tags=["Dashboard"]
)
def get_dashboard_summary(product: Optional[str] = Query(None), region: Optional[str] = Query(None), date: Optional[str] = Query(None)) -> DashboardSummaryResponse:
    """Retrieve overall customer intelligence metrics, including theme and sentiment counts."""
    df: pd.DataFrame = reviews_cache.get("df", pd.DataFrame())
    df = filter_reviews(df, product, region, date)
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Review intelligence dataset is not yet initialized."
        )

    overall_sentiment = compute_sentiment_breakdown(df)

    # Aggregate themes
    theme_items: List[ThemeSummaryItem] = []
    for theme_id, group in df.groupby("theme_id"):
        theme_name = group["theme_name"].iloc[0]
        theme_sentiment = compute_sentiment_breakdown(group)
        complaints_count = theme_sentiment.negative
        severity = compute_severity(complaints_count, len(group))

        theme_items.append(
            ThemeSummaryItem(
                theme_id=theme_id,
                theme_name=theme_name,
                total_reviews=len(group),
                complaints=complaints_count,
                severity=severity,
                sentiment=theme_sentiment,
            )
        )

    # Sort themes by complaint volume descending
    theme_items.sort(key=lambda t: t.complaints, reverse=True)

    return DashboardSummaryResponse(
        total_reviews=len(df),
        overall_sentiment=overall_sentiment,
        themes_count=len(theme_items),
        themes=theme_items,
    )


@app.get(
    "/themes",
    response_model=ThemesListResponse,
    summary="List Themes",
    tags=["Themes"]
)
def list_themes(product: Optional[str] = Query(None), region: Optional[str] = Query(None), date: Optional[str] = Query(None)) -> ThemesListResponse:
    """Retrieve all extracted themes with review counts, complaint counts, and severity rankings."""
    df: pd.DataFrame = reviews_cache.get("df", pd.DataFrame())
    df = filter_reviews(df, product, region, date)
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Review intelligence dataset is not yet initialized."
        )

    theme_items: List[ThemeSummaryItem] = []
    for theme_id, group in df.groupby("theme_id"):
        theme_name = group["theme_name"].iloc[0]
        theme_sentiment = compute_sentiment_breakdown(group)
        complaints = theme_sentiment.negative
        severity = compute_severity(complaints, len(group))

        theme_items.append(
            ThemeSummaryItem(
                theme_id=theme_id,
                theme_name=theme_name,
                total_reviews=len(group),
                complaints=complaints,
                severity=severity,
                sentiment=theme_sentiment,
            )
        )

    theme_items.sort(key=lambda t: t.complaints, reverse=True)
    return ThemesListResponse(themes=theme_items, total_themes=len(theme_items))


@app.get(
    "/themes/{theme_id}",
    response_model=ThemeDetailResponse,
    summary="Get Theme Details",
    tags=["Themes"]
)
def get_theme_detail(
    theme_id: str,
    preview_limit: int = Query(3, ge=1, le=20, description="Number of preview reviews to return")
) -> ThemeDetailResponse:
    """Retrieve specific theme details along with a preview sample of representative customer reviews."""
    df: pd.DataFrame = reviews_cache.get("df", pd.DataFrame())
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Review intelligence dataset is not yet initialized."
        )

    matched = df[df["theme_id"] == theme_id]
    if matched.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Theme with ID '{theme_id}' not found."
        )

    theme_name = matched["theme_name"].iloc[0]
    theme_sentiment = compute_sentiment_breakdown(matched)
    complaints = theme_sentiment.negative
    severity = compute_severity(complaints, len(matched))

    # Show preview reviews prioritizing negative/complaint reviews then highest ratings
    preview_df = matched.sort_values(by=["rating"], ascending=True).head(preview_limit)
    preview_reviews = [row_to_review_item(row) for _, row in preview_df.iterrows()]

    return ThemeDetailResponse(
        theme_id=theme_id,
        theme_name=theme_name,
        total_reviews=len(matched),
        complaints=complaints,
        severity=severity,
        sentiment=theme_sentiment,
        preview_reviews=preview_reviews,
    )


@app.get(
    "/themes/{theme_id}/reviews",
    response_model=ThemeReviewsResponse,
    summary="Get Theme Reviews",
    tags=["Themes"]
)
def get_theme_reviews(theme_id: str) -> ThemeReviewsResponse:
    """Retrieve all customer reviews mapped to a specific theme."""
    df: pd.DataFrame = reviews_cache.get("df", pd.DataFrame())
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Review intelligence dataset is not yet initialized."
        )

    matched = df[df["theme_id"] == theme_id]
    if matched.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Theme with ID '{theme_id}' not found."
        )

    theme_name = matched["theme_name"].iloc[0]
    reviews = [row_to_review_item(row) for _, row in matched.iterrows()]

    # Redact PII from every review text before returning
    for review in reviews:
        review.text = redact_text(review.text)

    return ThemeReviewsResponse(
        theme_id=theme_id,
        theme_name=theme_name,
        total=len(reviews),
        reviews=reviews,
    )


@app.get(
    "/alerts",
    response_model=AlertsListResponse,
    summary="List Early Issue Alerts",
    tags=["Alerts"]
)
def get_alerts(product: Optional[str] = Query(None), region: Optional[str] = Query(None), date: Optional[str] = Query(None)) -> AlertsListResponse:
    """List of Early Issue Detection alerts, sorted by urgency/velocity."""
    if not reviews_cache.get("initialized"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Review intelligence dataset is not yet initialized."
        )
    alerts = reviews_cache.get("alerts", [])
    if product:
        alerts = [a for a in alerts if a.get("affected_product") == product]
    if region:
        alerts = [a for a in alerts if a.get("affected_region") == region]
    if date:
        alerts = [a for a in alerts if a.get("start_date_of_spike") == date]
    return AlertsListResponse(alerts=alerts)


@app.get(
    "/alerts/{alert_id}",
    response_model=AlertItem,
    summary="Get Alert Detail",
    tags=["Alerts"]
)
def get_alert_detail(alert_id: str) -> AlertItem:
    """Retrieve full alert detail including correlated root cause events."""
    if not reviews_cache.get("initialized"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Review intelligence dataset is not yet initialized."
        )
    
    alerts = reviews_cache.get("alerts", [])
    for alert in alerts:
        if alert["alert_id"] == alert_id:
            alert_item = AlertItem(**alert)

            # Redact PII from the supporting review texts for this alert
            df: pd.DataFrame = reviews_cache.get("df", pd.DataFrame())
            if not df.empty and alert_item.supporting_review_ids:
                supporting_df = df[df["review_id"].isin(alert_item.supporting_review_ids)]
                redacted_reviews = [
                    row_to_review_item(row) for _, row in supporting_df.iterrows()
                ]
                for rev in redacted_reviews:
                    rev.text = redact_text(rev.text)
                alert_item.supporting_reviews = redacted_reviews

            return alert_item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Alert with ID '{alert_id}' not found."
    )



@app.get("/trends/compare", response_model=CompareTrendsResponse, tags=["Trends"])
def compare_trends(start_date_1: str = Query(...), end_date_1: str = Query(...), start_date_2: str = Query(...), end_date_2: str = Query(...)) -> CompareTrendsResponse:
    df: pd.DataFrame = reviews_cache.get("df", pd.DataFrame())
    if df.empty:
        raise HTTPException(status_code=503, detail="Not initialized")
    
    def get_period_trend(sd, ed):
        sub = df[(df["date"] >= sd) & (df["date"] <= ed)]
        total = len(sub)
        themes = []
        for theme_id, group in sub.groupby("theme_id"):
            themes.append(ThemeTrend(
                theme_name=group["theme_name"].iloc[0],
                count=len(group),
                sentiment=compute_sentiment_breakdown(group)
            ))
        return PeriodTrend(start_date=sd, end_date=ed, total_reviews=total, themes=themes)

    return CompareTrendsResponse(
        period_1=get_period_trend(start_date_1, end_date_1),
        period_2=get_period_trend(start_date_2, end_date_2)
    )

@app.get("/summary/executive", response_model=ExecutiveSummaryResponse, tags=["Summary"])
def get_executive_summary() -> ExecutiveSummaryResponse:
    df: pd.DataFrame = reviews_cache.get("df", pd.DataFrame())
    if df.empty:
        raise HTTPException(status_code=503, detail="Not initialized")
    
    overall = compute_sentiment_breakdown(df)
    theme_counts = df["theme_name"].value_counts()
    top_theme = theme_counts.index[0] if not theme_counts.empty else "N/A"
    
    alerts = reviews_cache.get("alerts", [])
    biggest_risk = alerts[0].get("theme_name") if alerts else "None"
    
    summary_text = (
        f"The dashboard currently reflects {len(df)} total reviews with an overall sentiment of "
        f"{overall.positive_pct}% positive and {overall.negative_pct}% negative. "
        f"The most discussed theme is '{top_theme}'. "
        f"The biggest emerging risk identified is '{biggest_risk}' based on recent velocity alerts. "
        f"Action is recommended to monitor the '{biggest_risk}' trend closely."
    )
    return ExecutiveSummaryResponse(summary=summary_text)

@app.get("/export", tags=["Export"])
def export_dashboard(product: Optional[str] = Query(None), region: Optional[str] = Query(None), date: Optional[str] = Query(None)):
    df: pd.DataFrame = reviews_cache.get("df", pd.DataFrame())
    if df.empty:
        raise HTTPException(status_code=503, detail="Not initialized")
    
    df = filter_reviews(df, product, region, date)
    
    stream = io.BytesIO()
    with pd.ExcelWriter(stream, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Reviews')
    stream.seek(0)
    
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=dashboard_export.xlsx"}
    )

@app.post(
    "/validate/sentiment",
    response_model=ValidationResponse,
    summary="Validate Sentiment Model",
    tags=["Validation"]
)
def validate_sentiment() -> ValidationResponse:
    """Run the sentiment model against a manually-labelled holdout sample and return accuracy.

    Computes overall accuracy, per-class accuracy breakdown, and lists
    any mismatched predictions for diagnostic purposes.
    """
    try:
        result = run_validation()
    except Exception as exc:
        logger.error("Sentiment validation failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation run failed: {exc}"
        )

    return ValidationResponse(
        total_samples=result["total_samples"],
        correct=result["correct"],
        accuracy=result["accuracy"],
        per_class=result["per_class"],
        mismatches=result["mismatches"],
    )

