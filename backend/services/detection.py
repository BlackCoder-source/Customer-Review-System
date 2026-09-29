import pandas as pd


def detect_early_issues(df, theme, z_threshold=2):
    daily = df[df["theme"] == theme].groupby(df["date"].dt.date).size()
    daily.index = pd.to_datetime(daily.index)
    rolling_mean = daily.shift(1).rolling(7, min_periods=3).mean()
    rolling_std = daily.shift(1).rolling(7, min_periods=3).std().fillna(0)
    z_score = (daily - rolling_mean) / rolling_std.replace(0, 1)
    alerts = z_score[z_score > z_threshold]

    daily_dict = {
        str(d.date() if hasattr(d, "date") else d): int(v)
        for d, v in daily.to_dict().items()
    }
    z_dict = {
        str(d.date() if hasattr(d, "date") else d): float(v)
        for d, v in z_score.fillna(0).to_dict().items()
    }

    return {
        "theme": theme,
        "alert_dates": [str(d.date()) for d in alerts.index],
        "daily_counts": daily_dict,
        "z_scores": z_dict,
    }


def get_all_alerts(df, z_threshold=2):
    results = []
    for theme in df["theme"].dropna().unique():
        result = detect_early_issues(df, theme, z_threshold)
        if result["alert_dates"]:
            results.append(result)
    return results
