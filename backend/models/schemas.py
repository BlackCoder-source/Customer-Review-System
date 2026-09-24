"""Pydantic schemas for API request and response models."""

from typing import List, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str = Field(..., description="Service health status", example="ok")
    version: str = Field(..., description="API version", example="1.0.0")
    total_reviews_loaded: int = Field(
        ..., description="Total count of ingested reviews", example=25
    )


class SentimentBreakdown(BaseModel):
    """Sentiment count and percentage breakdown."""

    positive: int = Field(0, description="Total positive reviews count")
    neutral: int = Field(0, description="Total neutral reviews count")
    negative: int = Field(0, description="Total negative reviews count")
    positive_pct: float = Field(0.0, description="Percentage of positive reviews")
    neutral_pct: float = Field(0.0, description="Percentage of neutral reviews")
    negative_pct: float = Field(0.0, description="Percentage of negative reviews")


class ThemeSummaryItem(BaseModel):
    """Aggregated theme item summary."""

    theme_id: str = Field(..., description="Identifier for the theme")
    theme_name: str = Field(..., description="Human-readable theme title")
    total_reviews: int = Field(..., description="Total reviews grouped under this theme")
    complaints: int = Field(
        ..., description="Number of negative/complaint reviews in this theme"
    )
    severity: str = Field(
        ..., description="Severity level based on complaints (low, medium, high)"
    )
    sentiment: SentimentBreakdown = Field(
        ..., description="Sentiment distribution within this theme"
    )


class DashboardSummaryResponse(BaseModel):
    """Overall dashboard summary schema."""

    total_reviews: int = Field(..., description="Total processed customer reviews")
    overall_sentiment: SentimentBreakdown = Field(
        ..., description="Overall sentiment breakdown across all reviews"
    )
    themes_count: int = Field(..., description="Total identified unique themes")
    themes: List[ThemeSummaryItem] = Field(
        default_factory=list, description="List of identified themes"
    )


class ReviewItem(BaseModel):
    """Individual review record representation."""

    review_id: str = Field(..., description="Unique review ID")
    text: str = Field(..., description="Review text content")
    product: str = Field(..., description="Target product name")
    region: str = Field(..., description="Customer geographical region")
    date: str = Field(..., description="Standardized review date (YYYY-MM-DD)")
    rating: float = Field(..., description="Customer numerical rating (1-5)")
    theme_id: str = Field(..., description="Assigned cluster theme ID")
    theme_name: str = Field(..., description="Assigned cluster theme name")
    sentiment: str = Field(
        ..., description="Predicted sentiment: positive, negative, or neutral"
    )
    sentiment_score: float = Field(
        ..., description="Model confidence score for sentiment prediction (0.0 to 1.0)"
    )


class ThemesListResponse(BaseModel):
    """Response containing list of all themes with complaint metrics."""

    themes: List[ThemeSummaryItem] = Field(
        ..., description="Themes list ordered by complaint counts"
    )
    total_themes: int = Field(..., description="Total number of themes available")


class ThemeDetailResponse(BaseModel):
    """Detailed theme information along with a preview of representative reviews."""

    theme_id: str = Field(..., description="Theme identifier")
    theme_name: str = Field(..., description="Theme title")
    total_reviews: int = Field(..., description="Total reviews in this theme")
    complaints: int = Field(..., description="Count of complaints in this theme")
    severity: str = Field(..., description="Severity level: low, medium, or high")
    sentiment: SentimentBreakdown = Field(
        ..., description="Sentiment distribution inside this theme"
    )
    preview_reviews: List[ReviewItem] = Field(
        default_factory=list,
        description="Top representative review previews for this theme",
    )


class ThemeReviewsResponse(BaseModel):
    """Complete collection of reviews for a specified theme."""

    theme_id: str = Field(..., description="Theme identifier")
    theme_name: str = Field(..., description="Theme title")
    total: int = Field(..., description="Total reviews returned")
    reviews: List[ReviewItem] = Field(
        ..., description="Full list of reviews assigned to this theme"
    )


class RootCauseItem(BaseModel):
    """Correlated root cause for a spike."""
    event_type: str = Field(..., description="Type of event")
    date: str = Field(..., description="Date of the event")
    product: str = Field(..., description="Affected product")
    region: str = Field(..., description="Affected region")
    description: str = Field("", description="Optional description of the event")


class AlertItem(BaseModel):
    """Early issue detection alert model."""
    alert_id: str = Field(..., description="Unique alert ID")
    theme_name: str = Field(..., description="Theme that spiked")
    start_date_of_spike: str = Field(..., description="Date the spike started")
    growth_rate: float = Field(..., description="Velocity/acceleration score")
    affected_product: str = Field(..., description="Dominant affected product")
    affected_region: str = Field(..., description="Dominant affected region")
    severity_score: str = Field(..., description="Severity of the spike (low, medium, high)")
    supporting_review_ids: List[str] = Field(default_factory=list, description="Reviews part of the spike")
    root_cause: Optional[RootCauseItem] = Field(None, description="Correlated root cause if any")


class AlertsListResponse(BaseModel):
    """Response containing list of early issue detection alerts."""
    alerts: List[AlertItem] = Field(..., description="List of detected early issues")
