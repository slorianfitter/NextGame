import numpy as np
from scipy.stats import norm
import pandas as pd

def agresti_coull(game_data: pd.DataFrame, days_30 = True):
    #Agresti Coull-Intervall

    if not days_30:
        k = game_data["positive_reviews"].fillna(0)
        n = game_data["total_reviews"].fillna(0)
    else:
        positive_reviews = game_data["reviews_30_days_percentage"].fillna(0)
        n = game_data["reviews_30_days_total"].fillna(0)
        k = round(positive_reviews*n)

    # z-Wert für 95% Konfidenzintervall
    alpha = 0.05
    z = norm.ppf(1 - alpha/2)

    #adjustierten werte: 

    k_tilde = k + z**2 / 2
    n_tilde = n + z**2
    p_tilde = k_tilde/n_tilde
    SE_ac = np.sqrt((p_tilde*(1-p_tilde)/n_tilde))


    agresti_coull_intervall_lower_bound = p_tilde - z*SE_ac
    agresti_coull_intervall_lower_bound  = pd.Series(agresti_coull_intervall_lower_bound, name="agresti_coull_intervall_lower_bound")
    return agresti_coull_intervall_lower_bound



#----------------------------------------



def cos_similarity(skalar_profile: pd.DataFrame, skalar_df: pd.DataFrame):
    """
    Berechnet die Cosinus-Ähnlichkeit zwischen jeder Zeile des DataFrames
    und dem Profil.
    Sprich: Das Skalarprodukt zwei genormter Vektoren
    """
    # Sicherstellen, dass gleiche Spalten
    gleiche_cols = skalar_profile.columns
    skalar_profile = skalar_profile[gleiche_cols]
    skalar_df = skalar_df[gleiche_cols]

    # Nur numerische Spalten
    df = skalar_df.select_dtypes(include=["number"])
    profile = skalar_profile.select_dtypes(include=["number"])

    # Profilvektor (1D) -> immer 1d
    profile_vec = profile.iloc[0].values

    # Matrix des DataFrames
    df_matrix = df.values

    # Normen 
    profile_norm = np.linalg.norm(profile_vec)
    df_norms = np.linalg.norm(df_matrix, axis=1)

    # Skalarprodukt zwischen Profil und jeder Zeile

    dot_products = np.array(df_matrix) @ np.array(profile_vec)

    # cosinus - similarity:
    cosine_sim = dot_products / (df_norms * profile_norm)

    # In DataFrame packen
    result = pd.DataFrame({
        "cosine_similarity": cosine_sim
    }, index=df.index)

    # Höchste Similarity = beste Empfehlung
    result = result.sort_values(by="cosine_similarity", ascending=False)

    return result




#----------------------------------------



def euklidische_distanz(df_profil:pd.DataFrame, df_games:pd.DataFrame):

    # Sicherstellen, dass nur numerics vorhanden sind
    df_profil = df_profil.select_dtypes(include=["number"])

    # nur die gleichen Spalten wählen
    gleiche_cols = df_profil.columns
    df_profil = df_profil[gleiche_cols]
    df_games = df_games[gleiche_cols]


    profile_vec = df_profil.iloc[0].values


    result = np.zeros(len(df_games))

    for i in range(len(df_games)):
        game_vec = df_games.iloc[i].values
        result[i] = np.linalg.norm(profile_vec - game_vec)

    # Als DataFrame zurückgeben
    result_series = pd.DataFrame(
        result,
        columns=["euc_distance"],
        index=df_games.index
    )

    return result_series.sort_values(by="euc_distance", ascending=True)



#----------------------------------------



def normalize_age_price(game_df, profile_df):

    game = game_df.copy()
    profile = profile_df.copy()

    age_max = game["required_age"].max()
    price_max = game["price"].max()

    for df in (game, profile):
        df["required_age"] = 1-(age_max - df["required_age"]) / age_max
        df["price"] = 1-(price_max - df["price"]) / price_max

    return game, profile 