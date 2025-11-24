# Ziel des Skript ist es ein K-nearest-neighbours model aufzuschreiben um die ähnliche Spiele zu finden für die Spieleempfehlung.

import numpy as np

import pandas as pd

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


