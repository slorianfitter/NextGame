# Funktion zur simplen Datenaufbereitung
import pandas as pd


def clean_and_prepare_data(df:pd.DataFrame, total_games):

    df = df[["id","playtime_forever","playtime_2weeks","rtime_last_played"]]

    merged_data = pd.merge(df, total_games, how="left", on="id")
    
    data_temporary = merged_data.dropna(subset=["required_age"]).copy()

    
    # gewünschte spalten wählen
    data = data_temporary[["id","name","required_age","playtime_forever","playtime_2weeks","rtime_last_played","released", "price_in_cents_no_discount", "genre","categories","feature"]]

    # weitere Datenanpassung

    data = data.copy()
    data["rtime_last_played"] = pd.to_datetime(data["rtime_last_played"], unit="s")
    data["categories"] = data["categories"].str.rstrip(";").str.split(";")
    data["genre"] = data["genre"].str.rstrip(";").str.split(";")
    data["hours_played"] = (data["playtime_forever"] / 60).round(2)
    data["playtime_forever"] = round(data["playtime_forever"] / 60,2)
    data["playtime_2weeks"] = round(data["playtime_2weeks"] / 60,2)

    return data

