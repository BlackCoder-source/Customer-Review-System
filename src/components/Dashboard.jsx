import React, { useEffect, useState } from "react";
import client from "../api/client";
import ThemeCards from "./ThemeCards";
import AlertsPanel from "./AlertsPanel";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    client
      .get("/dashboard/summary")
      .then((res) => {
        setSummary(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching dashboard summary:", err);
        setError("Failed to load dashboard summary");
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="dashboard-container">
      <h1>Customer Intelligence Dashboard</h1>
      <div className="summary-metrics">
        <div className="metric-card">
          <h3>Total Reviews</h3>
          <p>{summary?.total_reviews?.toLocaleString()}</p>
        </div>
        <div className="metric-card">
          <h3>Themes Count</h3>
          <p>{summary?.number_of_themes ?? summary?.themes_count}</p>
        </div>
        <div className="metric-card">
          <h3>Active Alerts</h3>
          <p>{summary?.number_of_active_alerts ?? summary?.active_alerts_count}</p>
        </div>
        <div className="metric-card">
          <h3>Sentiment Breakdown</h3>
          <p>
            Positive: {summary?.sentiment_breakdown?.positive} | Neutral:{" "}
            {summary?.sentiment_breakdown?.neutral} | Negative:{" "}
            {summary?.sentiment_breakdown?.negative}
          </p>
        </div>
      </div>

      <ThemeCards />
      <AlertsPanel />
    </div>
  );
}
