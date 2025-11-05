# Ziel dieser Datei ist es ein Basismodell als Funktion zu schreiben um später die verschiedenen Modelle zu vergleichen.
# Ich beginne hier mit einem einfachen Modell.
#   Regel:
#   Finde heraus, welches Genre in der Bibliothek am häufigsten (oder am längsten) gespielt wurde,
#   und empfehle eine liste von Spielen aus diesem Genre, die du noch nicht besitzt.


# import der pakete
import pandas as pd
import random
from .clean_and_prepared_data import clean_and_prepare_data



def base_recommend(user_games):
    url = "https://drive.google.com/file/d/1bqf0ik0TgFTKW2dKo-DznRsGRtwij1yD/view?usp=sharing"
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
        
    total_games = pd.read_csv(path)
    user_games = pd.DataFrame(user_games)

    # 2. Daten vorbereiten (angenommen deine Funktion existiert)
    games = clean_and_prepare_data(user_games, total_games)

    # 3. Genre-Analyse für User-Daten
    genre_explode = games["genre"].explode()

    genre_count = genre_explode.value_counts().reset_index()
    genre_count.columns = ["genre", "count"]

    # 4️. Meistgespieltes Genre holen
    top_genre = genre_count["genre"][0]

    # 5. Genre-Liste vorbereiten (NaN entfernen und splitten)
    total_games["genre"] = (
        total_games["genre"]
        .fillna("")               # Falls NaN-Werte existieren
        .astype(str)              # Sicherstellen, dass alles String ist
        .str.rstrip(";")
        .str.split(";")
    )


    data_filtered = total_games[total_games["genre"].apply(lambda x: top_genre in x)]

    recommendation = data_filtered.sample(10)

    recommendation = recommendation[["name", "released", "price_in_cents_no_discount",	"genre", "categories", "required_age","feature"]]

    return recommendation.sort_values(by="price_in_cents_no_discount", ascending=True)
