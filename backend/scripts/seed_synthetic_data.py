import pandas as pd
import os
from datetime import timedelta

def run():
    base_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(base_dir, exist_ok=True)
    reviews_path = os.path.join(base_dir, "reviews.csv")
    events_path = os.path.join(base_dir, "events.csv")
    
    # Load reviews
    if os.path.exists(reviews_path):
        df = pd.read_csv(reviews_path)
    else:
        print("reviews.csv not found.")
        return
        
    # Inject a spike for "SmartWatch Pro" in "North America"
    end_date = pd.to_datetime("2026-08-30")
    
    new_reviews = []
    for i in range(25):
        days_back = 2 - (i // 9) # roughly 8-9 per day for 3 days
        date = (end_date - timedelta(days=days_back)).strftime("%Y-%m-%d")
        new_reviews.append({
            "review_id": f"SYN-{1000+i}",
            "text": "The latest firmware update ruined the battery life completely. It drains in hours.",
            "product": "SmartWatch Pro",
            "region": "North America",
            "date": date,
            "rating": 1
        })
        
    new_df = pd.DataFrame(new_reviews)
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(reviews_path, index=False)
    
    # Create events.csv to correlate
    events = [
        {
            "date": "2026-08-27",
            "event_type": "firmware_update_v2.1",
            "product": "SmartWatch Pro",
            "region": "North America",
            "description": "Pushed OTA update 2.1 to NA users. Contains new battery optimizations."
        }
    ]
    pd.DataFrame(events).to_csv(events_path, index=False)
    print("Synthetic data injected into reviews.csv and events.csv created.")

if __name__ == "__main__":
    run()
