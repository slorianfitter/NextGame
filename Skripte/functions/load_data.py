import streamlit as st
import pandas as pd

@st.cache_data

def load_all_data():
    game_data = pd.read_csv(
        "./data/full_data_v1.csv"
    )

    game_data_0_1_part1 = pd.read_csv(
        "./data/full_data_0_1_part1.csv",sep=";"
    )
    game_data_0_1_part2 = pd.read_csv(
        "./data/full_data_0_1_part2.csv", sep=";"
    )

    image_and_description_data = pd.read_csv(
        "./data/image_and_description_data.csv"
    )

    game_data_0_1 = pd.merge(
        game_data_0_1_part1,
        game_data_0_1_part2,
        how="outer"
    )

    game_data_0_1 = game_data_0_1.sort_values(by= "id")

    # price austauschen
    game_data_0_1["price"] = game_data["price"] / 100
    game_data_0_1["required_age"] = game_data["required_age"]
    game_data_0_1 = game_data_0_1.dropna()
    
    # join Image + Beschreibung
    game_image_desc_data = pd.merge(
        game_data,
        image_and_description_data,
        how="left",
        on="id"
    )

    return game_data, game_data_0_1, game_image_desc_data, image_and_description_data
