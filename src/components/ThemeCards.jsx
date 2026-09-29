import React, { useEffect, useState } from "react";
import client from "../api/client";

export default function ThemeCards() {
  const [themes, setThemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    client
      .get("/themes")
      .then((res) => {
        setThemes(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching themes:", err);
        setError("Failed to load themes");
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="themes-section">
      <h2>Themes</h2>
      <div className="theme-cards-grid">
        {themes.map((theme, idx) => (
          <div key={idx} className="theme-card">
            <h3>{theme.theme || theme.theme_name}</h3>
            <p>Review Count: {theme.review_count ?? theme.count}</p>
            <p>Average Sentiment: {theme.average_sentiment ?? theme.avg_sentiment}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
