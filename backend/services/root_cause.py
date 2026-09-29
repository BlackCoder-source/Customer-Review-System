from typing import Optional, Dict, Any
import pandas as pd


def find_root_cause(alert_date: str, events_df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """Checks events_df for any event within 5 days before alert_date,

    and returns the matching event row as a dict, or None if no match.
    """
    if events_df is None or events_df.empty:
        return None

    try:
        alert_dt = pd.to_datetime(alert_date)
    except Exception:
        return None

    events_df_copy = events_df.copy()
    events_df_copy["date"] = pd.to_datetime(events_df_copy["date"])

    window_start = alert_dt - pd.Timedelta(days=5)
    matching = events_df_copy[
        (events_df_copy["date"] >= window_start) & (events_df_copy["date"] <= alert_dt)
    ]

    if matching.empty:
        return None

    row = matching.iloc[0].to_dict()
    if "date" in row and hasattr(row["date"], "strftime"):
        row["date"] = str(row["date"].strftime("%Y-%m-%d"))
    elif "date" in row:
        row["date"] = str(row["date"])

    return row
