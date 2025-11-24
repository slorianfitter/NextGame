## In diesem Skript werden alle gesammelten Daten zusammengefügt und nochmals aufbereitet. 
## An einigen stellen sind Typos durch die Umlaute in der Sprache. Diese werden seperat direkt in der excel Datei bearbeitet.

# Pakete laden

import pandas as pd

# Import der Basis und leichte Anpassung.

base = pd.read_csv("../../data/wanted_information.csv")

# Zwei nicht benötigte Spalten können ganz entfernt werden.
# total_steam_reviews_with_game wird später durch die ganzen Reviews ersetzt. Unnamed: 0 ist ein fehler durchs speichern #index = False

base=base.drop(labels =["Unnamed: 0", "total_steam_reviews_with_game"], axis=1)
base =base.rename(columns={"categories": "category"})

#Import der Reviews und Tags
RaT = pd.read_csv("../../data/review_alltime.csv")
merged_df = pd.merge(RaT,base, on="id", how="left") # horizonta
 

#Tags
merged_df["tags"] = merged_df["tags"].fillna("NA").str.strip().str.split(";")

tags_explode = merged_df["tags"].explode().str.strip()
tags_list = list(tags_explode.unique())

pd.Series(tags_list, name="tag_name").to_csv("../../data/all_tags_for_games.csv", index=False)

tags_df = pd.crosstab(tags_explode.index, tags_explode)
tags_df = tags_df.add_prefix("TAG_")



#feature
merged_df["feature"] =merged_df["feature"].fillna("NA").str.strip().str.split(";")
feature_explode =merged_df["feature"].explode().str.strip()
feature_list = list(feature_explode.unique())

pd.Series(feature_list, name="feature_name").to_csv("../../data/alle_features_bei_steam.csv", index=False)

feature_df = pd.crosstab(feature_explode.index, feature_explode)
feature_df = feature_df.add_prefix("FEATURE_")



#genre
merged_df["genre"] =merged_df["genre"].fillna("NA").str.strip().str.split(";")
genre_explode =merged_df["genre"].explode().str.strip()
genre_list = list(genre_explode.unique())

pd.Series(genre_list, name="genre_name").to_csv("../../data/alle_genres_bei_steam.csv", index=False)

genre_df = pd.crosstab(genre_explode.index, genre_explode)
genre_df = genre_df.add_prefix("GENRE_")



#category
merged_df["category"] =merged_df["category"].fillna("NA").str.strip().str.split(";")
category_explode =merged_df["category"].explode().str.strip()
category_list = list(category_explode.unique())

pd.Series(category_list, name="category_name").to_csv("../../data/alle_categories_bei_steam.csv", index=False)

category_df = pd.crosstab(category_explode.index, category_explode)
category_df = category_df.add_prefix("CATEGORY_")
# Alles in eine Tabelle
onehot_df = pd.concat([genre_df, category_df, tags_df, feature_df],axis=1)

# Anpassung der onehots
onehot_df.columns = onehot_df.columns.str.replace(" ", "_", regex=False)
onehot_df.columns = onehot_df.columns.str.replace("__+", "_", regex=False)
merged_df = merged_df.drop(labels=["category", "feature","tags","genre"], axis=1)
merged_df = pd.concat([merged_df, onehot_df], axis=1) # vertikal

finished = merged_df
finished.to_csv("../../data/full_data.csv", index=False) # Schnellster und einfachster weg. Mit Excel hat es nicht gegklappt bzw. hat ewig gedauert.
                                                                              # Schneller ging es dann mit öffnen und exportieren. Vorteil: Daten sind nun als csv und xslx vorhanden.
                                                                              # Nachteil: ich musste selbst nochmal klicken.

#finished.to_excel("../data/full_data.xlsx", engine="xlsxwriter", index=False)