# Ziel dieser Datei ist es ein Basismodell als Funktion zu schreiben um später die verschiedenen Modelle zu vergleichen.
# Ich beginne hier mit einem einfachen Modell.
#   Regel:
#   Finde heraus, welches Genre in der Bibliothek am häufigsten (oder am längsten) gespielt wurde,
#   und empfehle eine liste von Spielen aus diesem Genre, die du noch nicht besitzt.


# import der pakete
import pandas as pd
import random



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

