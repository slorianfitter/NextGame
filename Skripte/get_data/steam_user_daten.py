import requests
import pandas as pd

url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=3861800C377A21789C2C6BA317DCAF13&steamid=76561198798886462&include_appinfo=1&include_played_free_games=1&format=json"

res = requests.get(url).json()
games = res["response"]["games"]

df = pd.DataFrame(games)

# Stunden-Spalte hinzufügen
df["hours_played"] = (df["playtime_forever"] / 60).round(2)

# Excel-Datei schreiben
df.to_csv("D:/Projekte/spielvorschlag/data/eigene_steam_daten.csv", index=False)

print("CSV-Datei erstellt: eigene_steam_daten.csv")
