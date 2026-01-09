from functions.better_reviews import agresti_coull, euklidische_distanz, cos_similarity, normalize_age_price

import pandas as pd
import numpy as np


def base_recommend(user_games, all_games):

    # Top Genre
    genre = user_games["genre"].str.split(";")
    genre_explode = genre.explode()
    top_genre = genre_explode.value_counts().idxmax()

    # Top Category
    categories = user_games["categories"].str.split(";")
    categories_explode = categories.explode()
    top_category = categories_explode.value_counts().idxmax()

    # Top Tag
    tags = user_games["tags"].str.split(";")
    tags_explode = tags.explode()
    top_tag = tags_explode.value_counts().idxmax()

    # Alle Spalten vorbereiten
    for col in ["genre", "categories", "tags"]:
        all_games[col] = (
            all_games[col]
            .fillna("")
            .astype(str)
            .str.rstrip(";")
            .str.split(";")
        )

    # Filter anwenden
    data_filtered = all_games[
        all_games["genre"].apply(lambda x: top_genre in x) &
        all_games["categories"].apply(lambda x: top_category in x) &
        all_games["tags"].apply(lambda x: top_tag in x)
    ]

    # Empfehlung ziehen
    try:
        recommendation = data_filtered.sample(min(3, len(data_filtered)))
        result = recommendation[["id","name","price","released","genre","categories","tags","required_age","feature"]]
        # Falls Spalte price_in_cents_no_discount existiert, sonst price verwenden
        if "price_in_cents_no_discount" in result.columns:
            result = result.sort_values(by="price_in_cents_no_discount", ascending=True)
        else:
            result = result.sort_values(by="price", ascending=True)
    except ValueError:
        result = "Zu viele Filter aktiv. Versuche weniger oder andere Kombinationen"
    
    return result



#----------------------------------------



def recommend_games(
    game_data: pd.DataFrame,
    profil_data: pd.DataFrame,
    own_game_ids:set,
    use_reviews:bool=False,
    review_weight:float=0.3,
    cos_threshold:float=0.6,
    top_k=20
):
    """
    Docstring for recommend_games
    
    :param game_data: Spiele Daten df. Numerische Werte erforderlich. 
    :type game_data: pd.DataFrame
    
    :param profil_data: Profilvektor. numerische Werte
    :type profil_data: pd.DataFrame

    :param own_game_ids: Spiele, die der User bereits besitzt. Hier nur ein 1D-Vektor notwendig mit den Spiele-Ids
    :type own_game_ids: set
    
    :param use_reviews: 
    :type use_reviews: bool
    
    :param review_weight: Falls Reviews miteinbezogen werden sollen, dann kann das Gewicht dieses Parameters festgelegt werden. Werde von 0-1 sinnvoll.
    :type review_weight: float
    
    :param cos_threshold: Grenze für die Spiele, die beim Filtern nach der Cosinus-Ähnlichkeit ausgeschlossen werden.
    :type cos_threshold: float
    
    :param top_k: Anzahl der Spiele, die höchstens vorgeschlagen werden können
    :type top_k: float
    """
    
    
    # Sicherstellen, dass die richtigen Spalten für die Normalisierung vorhanden sind

    game_norm, profil_norm = normalize_age_price(game_data, profil_data)

    # Cosinus-Filter
    cos = cos_similarity(profil_norm, game_norm)
    cos_filtered = cos[cos["cosine_similarity"] > cos_threshold] # alles größer als der threshold wird genutzt

    if len(cos_filtered) > 0:
        filtered_games = game_data.loc[cos_filtered.index]

        # Euklidische Distanz NUR auf Kandidaten
        euc_dist = euklidische_distanz(profil_norm, filtered_games)
        
        top_indices = euc_dist.head(top_k).index # index sind hier die Spieleids. euc dist ist schon ascending sortiert
        filtered_top = filtered_games.loc[top_indices]

        # Eigene Spiele ausschließen
        filtered_top = filtered_top[~filtered_top["id"].isin(own_game_ids)]
        euc_dist = euc_dist.loc[filtered_top.index]["euc_distance"]

        # Normierung
        dist_score = 1 - (euc_dist.max() - euc_dist) / euc_dist.max()
        
        # Optional Reviews
        if use_reviews:
            reviews = agresti_coull(filtered_top, days_30=False)
            score = (
                review_weight * reviews +
                (1 - review_weight) * dist_score
            )
        else:
            score = dist_score.dropna()
    else:
        score = None

    return pd.Series(score, name="score").sort_values(ascending=False).dropna()
