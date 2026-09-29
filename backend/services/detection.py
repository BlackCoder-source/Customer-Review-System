import pandas as pd
import numpy as np
from typing import List, Dict, Any

def detect_early_issues(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Detects early issues (spikes) by analyzing complaint volumes.
    - Buckets complaint count by day for each theme.
    - Calculates rolling average and std dev over recent buckets.
    - Flags theme as early issue if count > 2 std dev above rolling avg.
    - Calculates velocity score.
    """
    alerts = []
    
    if 'sentiment' not in df.columns or df.empty:
        return alerts
        
    complaints = df[df['sentiment'] == 'negative'].copy()
    if complaints.empty:
        return alerts
        
    complaints['date'] = pd.to_datetime(complaints['date'])
    
    for theme_name, group in complaints.groupby('theme_name'):
        daily = group.groupby(group['date'].dt.date).size().reset_index(name='count')
        daily['date'] = pd.to_datetime(daily['date'])
        
        if daily.empty:
            continue
            
        date_range = pd.date_range(daily['date'].min(), daily['date'].max())
        daily = daily.set_index('date').reindex(date_range).fillna(0)
        daily['count'] = daily['count'].astype(int)
        
        if len(daily) < 2:
            continue
            
        rolling_window = min(7, len(daily))
        daily['rolling_avg'] = daily['count'].rolling(window=rolling_window, min_periods=1).mean().shift(1)
        daily['rolling_std'] = daily['count'].rolling(window=rolling_window, min_periods=1).std().shift(1).fillna(0)
        
        spike_detected = False
        latest_spike_row = None
        latest_spike_date = None
        
        for idx, row in daily.iterrows():
            if pd.isna(row['rolling_avg']):
                continue
            threshold = row['rolling_avg'] + 2 * row['rolling_std']
            if row['count'] > threshold and row['count'] > 0:
                spike_detected = True
                latest_spike_row = row
                latest_spike_date = idx
        
        if spike_detected and latest_spike_row is not None:
            prev_date = latest_spike_date - pd.Timedelta(days=1)
            prev_count = daily.loc[prev_date, 'count'] if prev_date in daily.index else 0
            growth_rate = float(latest_spike_row['count'] - prev_count)
            
            recent_complaints = group[group['date'] >= (latest_spike_date - pd.Timedelta(days=1))]
            if recent_complaints.empty:
                recent_complaints = group
                
            dominant_product = recent_complaints['product'].mode().iloc[0] if not recent_complaints['product'].empty else "Unknown"
            dominant_region = recent_complaints['region'].mode().iloc[0] if not recent_complaints['region'].empty else "Unknown"
            
            supporting_reviews = recent_complaints['review_id'].tolist()
            
            if growth_rate > 5:
                severity_score = "high"
            elif growth_rate > 2:
                severity_score = "medium"
            else:
                severity_score = "low"
                
            alerts.append({
                "alert_id": f"ALT-{abs(hash(theme_name))}-{latest_spike_date.strftime('%Y%m%d')}",
                "theme_name": theme_name,
                "start_date_of_spike": latest_spike_date.strftime('%Y-%m-%d'),
                "growth_rate": growth_rate,
                "affected_product": dominant_product,
                "affected_region": dominant_region,
                "severity_score": severity_score,
                "supporting_review_ids": supporting_reviews
            })
            
    # Sort alerts by growth rate descending
    alerts.sort(key=lambda x: x['growth_rate'], reverse=True)
    return alerts
