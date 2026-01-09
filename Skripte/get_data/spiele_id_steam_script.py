import requests
import pandas as pd
import time
key = "3861800C377A21789C2C6BA317DCAF13"





spiele = []

for i in range(400):
    last_appid = spiele[-1]["appid"] if spiele else 0
    url = f"https://api.steampowered.com/IStoreService/GetAppList/v0001/?key={key}&include_dlc=false&last_appid={last_appid}"

    res = requests.get(url).json()
    apps = res.get("response", {}).get("apps", [])

    if not apps:
        print("Keine neuen Apps gefunden. Schleife beendet.")
        break

    # gesamte App-Dictionaries hinzufügen
    spiele.extend(apps)
    print(f"{len(apps)} Apps geladen, insgesamt {len(spiele)}.")
    time.sleep(3)
# DataFrame aus der Liste von Dictionaries
df = pd.DataFrame(spiele)

# CSV schreiben
df.to_csv("D:/Projekte/spielvorschlag/spiele_ids_steam_2.csv", index=False)
print(f"Datei wurde geschrieben. Insgesamt {len(spiele)} Apps.")
