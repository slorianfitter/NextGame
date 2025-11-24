import pandas as pd
import numpy as np
import requests
import time
import os

# CSV mit allen App-IDs laden
base_steam = pd.read_csv("../../data/spiele_ids_steam.csv")


required_info = []  # -> Base für alle notwendigen Infos, die ich aktuell brauche 
additional_info = [] # -> Base für alle zusätzlichen Infos, brauchbar für das frontend zum Display
exceptions = []  # Daten auffangen weil Daten in Steamapi teilweise fehlen. -> Will ich nicht verlieren



# Original data
file_path_required_info = "../../data/required_info.csv"
file_path_additional_info = "../../data/additional_info.csv"
file_path_exception_data = "../../data/exception_data.csv"
file_path_current_index = "../../data/current_index.csv"

# Advanced Data, for data completion 
file_path_second_index = "../../data/second_index.csv"
file_path_second_required_info = "../../data/second_required_info.csv"
file_path_second_additional_info = "../../data/second_additional_info.csv"
file_path_second_exception_data = "../../data/second_exception_data.csv"

#-------------------------------------------
# Modifikator für first and second pass!!!!
#-------------------------------------------

second_data_get = True


if second_data_get:
    required_info_csv = pd.read_csv(file_path_required_info) # csv aus first crawl
    ids = required_info_csv["id"]
    if os.path.exists(file_path_second_index):
        try:
            current_index_df = pd.read_csv(file_path_second_index)
            if not current_index_df.empty:
                index = int(current_index_df.iloc[-1,0]) +1 
                print(f"Fortgesetzt bei Index {index}")
            else:
                index = 0
        except Exception:
            index = 0
    else:
        index = 0

# Backup Index falls es zu abbrüchen kommt. Gleichzeitig werden während der Schleife auch regelmäßig backups gemacht.
else: 
    ids = base_steam["appid"]
    try:
        current_index_df = pd.read_csv(file_path_current_index)
        if not current_index_df.empty:
            index = int(current_index_df.iloc[-1,0]) +1 
            print(f"Fortgesetzt bei Index {index}")
        else:
            index = 0
    except Exception:
        index = 0


current_index = index # initialisierung

# Schleife für die API -> für jeden Durchgang mind. 3 Sekunden. Da rund 270 Tausend Datenpunkte zu checken braucht die Schleife ca. 9 1/2 Tage 

# Hauptschleife
for number in ids[index:]:




    try:

        time.sleep(1.5)  # wichtig, um Steam nicht zu überlasten 
        print(f"Aktuell bei ID Nummer: {current_index} von möglichen {len(ids)} IDs")
        url = f"https://store.steampowered.com/api/appdetails?appids={number}&l=german"
        res = requests.get(url).json()
        app_data = res[str(number)]
        # prüfen, ob gültig
        if not app_data["success"]:
            continue

        data = app_data["data"]

        if data.get("type") != "game":
            continue

        # Ratings mit Fallback-Logik, weil die Altersempfehlungen / Beschränkungen nicht einheitlich sind. Diese werden aber auch nicht alle ergebnisse liefern. 
        # Also habe ich mir ein Fallback bei den exceptions gebaut um die IDs nicht zu verlieren, denn für das Modell brauche ich soviele Daten wie möglich.
        # Wobei man hier schon davon ausgehen kann, dass wenn das Alter fehlt, es kein relevanten Spiel sein wird. Zumindest nicht für den Großteil der Community


        #-------------------------------------
        # Ratings 
        
        ratings = data.get("ratings", {}) or {}
        steam_de = ratings.get("steam_germany", {})
        usk = ratings.get("usk", {})
        

        #-------------------------------------
        # Steam Germany 
        #-------------------------------------

        if steam_de and steam_de.get("required_age"):
            alter_steam_de = steam_de.get("required_age")
            eigenschaften_steam_de_raw = steam_de.get("descriptors", "")
        else:
            alter_steam_de = None
            eigenschaften_steam_de_raw = ""

        eigenschaften_steam_de = [
            x.strip() for x in str(eigenschaften_steam_de_raw)
            .replace(",", ";").replace("\n", ";").split(";")
        ]

        #-------------------------------------
        # USK  
        #-------------------------------------

        if usk and usk.get("rating"):
            alter_usk = usk.get("rating")
            eigenschaften_usk_raw = usk.get("descriptors", "")
        else:
            alter_usk = None
            eigenschaften_usk_raw = ""

        eigenschaften_usk = [
            x.strip() for x in str(eigenschaften_usk_raw)
            .replace(",", ";").replace("\n", ";").split(";")
        ]



        # Originalpreise bekommen.
        price_overview= data.get("price_overview", None)

        if price_overview:
            price = price_overview.get("initial", None)
        else:
            price = None


        # Ergebnis speichern
        required_info.append({
            "id": number,
            "alter_usk": alter_usk,
            "eigenschaften_usk": "; ".join(eigenschaften_usk),
            "alter_steam": alter_steam_de,
            "eigenschaften": "; ".join(eigenschaften_steam_de),
            "genre": "; ".join([g["description"] for g in data.get("genres", [])]),
            "categories": "; ".join([c["description"] for c in data.get("categories", [])]),
            "released": data.get("release_date", {}).get("date", None),
            "original_price": price,
            "is_free": data.get("is_free", False),
            "recommendations": data.get("recommendations", {}).get("total", None)
        })
        
        additional_info.append({
            "id": number,
            "image": data.get("header_image", None),
            "detailed_description": data.get("detailed_description", None),
            "short_description": data.get("short_description", None)
        })  
        
        print("Spieledaten Hinzugefügt!!!")

    except Exception as e: 
        print(f"Fehler bei {number}: {e}")
        exceptions.append(number)
        time.sleep(30)

    

    finally: # Autosave 
        current_index +=1
        if not second_data_get:
            if (current_index > 0 and current_index % 100 == 0) or (current_index == (len(ids))):
                required_info = pd.DataFrame(required_info)
                additional_info = pd.DataFrame(additional_info)
                exceptions_df = pd.DataFrame(exceptions, columns=["id"])

                # Autosave required information
                if not os.path.exists(file_path_required_info):
                    required_info.to_csv(file_path_required_info, index=False)
                else:
                    req1 = pd.read_csv(file_path_required_info)
                    req = pd.concat([req1, required_info], ignore_index=True).drop_duplicates()
                    req.to_csv(file_path_required_info, index=False)


                # Autosave additional information
                if not os.path.exists(file_path_additional_info):
                    additional_info.to_csv(file_path_additional_info, index = False)
                else:
                    add1 = pd.read_csv(file_path_additional_info)
                    req2 = pd.concat([add1, additional_info], ignore_index=True).drop_duplicates()
                    req2.to_csv(file_path_additional_info, index=False)

                # Autosave der exceptions
                if os.path.exists(file_path_exception_data) and os.path.getsize(file_path_exception_data) > 0:
                    try:
                        excp1 = pd.read_csv(file_path_exception_data)
                    except pd.errors.EmptyDataError:
                        excp1 = pd.DataFrame(columns=["id"])
                else:
                    excp1 = pd.DataFrame(columns=["id"])

                req3 = pd.concat([excp1, exceptions_df], ignore_index=True).drop_duplicates()
                req3.to_csv(file_path_exception_data, index=False)


                # Autosave des Index
                pd.DataFrame({"current_index": [current_index]}).to_csv(
                    file_path_current_index, index=False
                )
                
                required_info = []
                additional_info = []
                exceptions = []
                print(f"Autosave bei index {current_index} ✅")
            

        else:
            if (current_index > 0 and current_index % 100 == 0) or (current_index == (len(ids))):
                required_info = pd.DataFrame(required_info)
                additional_info = pd.DataFrame(additional_info)
                exceptions_df = pd.DataFrame(exceptions, columns=["id"])

                # Autosave required information
                if not os.path.exists(file_path_second_required_info):
                    required_info.to_csv(file_path_second_required_info, index=False)
                else:
                    req1 = pd.read_csv(file_path_second_required_info)
                    req = pd.concat([req1, required_info], ignore_index=True).drop_duplicates()
                    req.to_csv(file_path_second_required_info, index=False)


                # Autosave additional information
                if not os.path.exists(file_path_second_additional_info):
                    additional_info.to_csv(file_path_second_additional_info, index = False)
                else:
                    add1 = pd.read_csv(file_path_second_additional_info)
                    req2 = pd.concat([add1, additional_info], ignore_index=True).drop_duplicates()
                    req2.to_csv(file_path_second_additional_info, index=False)

                # Autosave der exceptions
                if os.path.exists(file_path_second_exception_data) and os.path.getsize(file_path_second_exception_data) > 0:
                    try:
                        excp1 = pd.read_csv(file_path_second_exception_data)
                    except pd.errors.EmptyDataError:
                        excp1 = pd.DataFrame(columns=["id"])
                else:
                    excp1 = pd.DataFrame(columns=["id"])

                req3 = pd.concat([excp1, exceptions_df], ignore_index=True).drop_duplicates()
                req3.to_csv(file_path_second_exception_data, index=False)


                # Autosave des Index
                pd.DataFrame({"current_index": [current_index]}).to_csv(
                    file_path_second_index, index=False
                )

                required_info = []
                additional_info = []
                exceptions = []
                print(f"Autosave bei index {current_index} ✅")
        
        