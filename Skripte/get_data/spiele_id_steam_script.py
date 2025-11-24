import requests
import pandas as pd

url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

res = requests.get(url).json()

spiele = res["applist"]["apps"]

# Stunden-Spalte hinzufügen
df = pd.DataFrame(spiele)

# Excel-Datei schreiben
df.to_csv("D:/Projekte/spielvorschlag/spiele_ids_steam_2.csv", index=False)

print("Datei wurde geschrieben")
