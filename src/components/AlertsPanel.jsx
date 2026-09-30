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
        const alertList = Array.isArray(res.data) ? res.data : (res.data?.alerts || []);
        console.log("Raw GET /alerts response object:", alertList[0]);
        setAlerts(alertList);
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

  const getSeverityClass = (severity) => {
    const sev = (severity || "").toUpperCase();
    if (sev === "HIGH") return "badge badge-high severity-high";
    if (sev === "MEDIUM") return "badge badge-medium severity-medium";
    return "badge badge-low severity-low";
  };

  const alertArray = Array.isArray(alerts) ? alerts : (alerts?.alerts || []);

  return (
    <div className="alerts-panel">
      <h2>Emerging Issues / Alerts</h2>
      <div className="alerts-list">
        {alertArray.map((alert, idx) => {
          const themeTitle = alert.theme || alert.theme_name || alert.title || "Unknown Theme";
          const growth = alert.growth_percent ?? alert.growth ?? alert.growth_rate ?? 0;
          const growthSign = growth >= 0 ? "↑ " : "↓ ";
          const severity = (alert.severity || alert.severity_score || "MEDIUM").toUpperCase();
          const alertId = alert.alert_id || alert.id;
          const product = alert.affected_product || alert.product || "All Products";
          const region = alert.affected_region || alert.region || "All Regions";
          const detectedDate = alert.start_date_of_spike || alert.detected_date;

          return (
            <div key={alertId || idx} className="alert-card" data-alert-id={alertId}>
              <div className="alert-card-header">
                <h3 className="alert-card-title">{themeTitle}</h3>
                <span className={getSeverityClass(severity)}>{severity}</span>
              </div>

              <div className="alert-card-body">
                <p className="growth-indicator">
                  <strong>{growthSign}{Math.abs(growth)}%</strong> complaint growth
                </p>
                <p className="affected-info">
                  {product} • {region}
                </p>
                {detectedDate && (
                  <p className="detected-date">
                    Detected: {detectedDate}
                  </p>
                )}
              </div>

              {alert.root_cause ? (
                <div className="root-cause">
                  <strong>Root Cause:</strong>
                  <p>
                    Date: {alert.root_cause.date} | Event:{" "}
                    {alert.root_cause.event_type || alert.root_cause.description}
                  </p>
                </div>
              ) : (
                <p className="no-root-cause">No immediate root cause event detected</p>
              )}

              <div className="alert-card-footer">
                <small className="alert-id-sub">ID: {alertId}</small>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
