import numpy as np
import pandas as pd

def cos_similarity(skalar_df: pd.DataFrame, skalar_profile: pd.DataFrame):
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
