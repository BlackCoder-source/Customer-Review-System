import React, { useEffect, useState } from "react";
import client from "../api/client";

export default function AlertsPanel() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    client
      .get("/alerts")
      .then((res) => {
        setAlerts(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching alerts:", err);
        setError("Failed to load alerts");
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="alerts-panel">
      <h2>Emerging Issues / Alerts</h2>
      <div className="alerts-list">
        {alerts.map((alert, idx) => (
          <div key={idx} className="alert-card">
            <h3>Theme: {alert.theme}</h3>
            <p>Alert Dates: {alert.alert_dates?.join(", ")}</p>
            {alert.root_cause ? (
              <div className="root-cause">
                <strong>Root Cause:</strong>
                <p>
                  Date: {alert.root_cause.date} | Event:{" "}
                  {alert.root_cause.event_type || alert.root_cause.description}
                </p>
              </div>
            ) : (
              <p>No immediate root cause event detected</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
