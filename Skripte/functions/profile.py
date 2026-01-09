import pandas as pd

def profile(df: pd.DataFrame, df_01: pd.DataFrame, weighted=False, last_14_days=False):

    df = df[["id", "playtime_2weeks", "playtime_forever"]]
    res = pd.merge(df, df_01, how="left", on="id").fillna(0)

    # Spielzeit bestimmen
    playtime_col = "playtime_2weeks" if last_14_days else "playtime_forever"
    playtime = res[playtime_col]

    # NUR Feature-Spalten
    feature_cols = res.drop(labels=["id", "playtime_2weeks", "playtime_forever"], errors="ignore", axis=1)
    X = feature_cols

    if weighted:
        total = playtime.sum()
        if total == 0:
            profile_vec = X.mean()
        else:
            weights = playtime / total
            profile_vec = (X.T @ weights)
    else:
        if last_14_days:
            profile_vec = X[playtime > 0].mean()
        else:
            profile_vec = X.mean()

    return profile_vec.to_frame().T

