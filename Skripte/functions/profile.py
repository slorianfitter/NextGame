import pandas as pd

def profile(df: pd.DataFrame, weighted=False, last_14_days=False):
    
    df = df.select_dtypes(include=["number"])
    df = df.drop(labels=["id"], axis=1, errors="ignore")  # robust

    df = df.fillna(0)
    
    if weighted and last_14_days:
        total_playtime = df["playtime_2weeks"].sum()

        if total_playtime == 0:
            finished_mean = df.mean().to_frame().T
        else:
            weighted_mean = df["playtime_2weeks"] / total_playtime
            
            weighted_mean_per_row = df.mul(weighted_mean, axis=0)
            finished_mean = weighted_mean_per_row.sum().to_frame().T
    
    elif weighted and not last_14_days:

        total_playtime = df["playtime_forever"].sum()
        if total_playtime == 0:
            finished_mean = df.mean().to_frame().T
        else:
            weighted_mean = df["playtime_forever"] / total_playtime
            
            weighted_mean_per_row = df.mul(weighted_mean, axis=0)
            finished_mean = weighted_mean_per_row.sum().to_frame().T

    elif last_14_days and not weighted:
        total_playtime = df["playtime_2weeks"].sum()
        if total_playtime == 0:
            finished_mean = df.mean().to_frame().T
        else:
            finished_mean = df[df["playtime_2weeks"] > 0].mean().to_frame().T
    else:
        finished_mean = df.mean().to_frame().T

    finished_mean = finished_mean.drop(columns=[
        "total_reviews", "positive_reviews", "negative_reviews", 
        "reviews_30_days_total","reviews_30_days_percentage",
        "price_in_cents_no_discount", "website_price", "rtime_last_played", "playtime_forever","playtime_2weeks"
    ], errors="ignore")
    
    return finished_mean
