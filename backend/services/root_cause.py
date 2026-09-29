import pandas as pd
import os
from typing import Dict, Any, Optional

EVENTS_CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "events.csv")

def find_root_cause(alert: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Correlates a detected spike against data/events.csv.
    Checks for any event within a few days before the spike started,
    matching product/region.
    """
    if not os.path.exists(EVENTS_CSV_PATH):
        return None
        
    try:
        events_df = pd.read_csv(EVENTS_CSV_PATH)
    except Exception:
        return None
        
    if events_df.empty:
        return None
        
    events_df['date'] = pd.to_datetime(events_df['date'])
    
    spike_date = pd.to_datetime(alert['start_date_of_spike'])
    window_start = spike_date - pd.Timedelta(days=7) # Look back up to 7 days
    
    mask = (
        (events_df['product'] == alert['affected_product']) &
        (events_df['region'] == alert['affected_region']) &
        (events_df['date'] >= window_start) &
        (events_df['date'] <= spike_date)
    )
    
    matched = events_df[mask]
    if not matched.empty:
        latest_event = matched.sort_values(by='date', ascending=False).iloc[0]
        return {
            "event_type": str(latest_event.get('event_type', 'unknown')),
            "date": latest_event['date'].strftime('%Y-%m-%d'),
            "product": str(latest_event.get('product', 'unknown')),
            "region": str(latest_event.get('region', 'unknown')),
            "description": str(latest_event.get('description', ''))
        }
    return None
