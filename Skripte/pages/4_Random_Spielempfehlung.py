import pandas as pd
from functions.load_data import load_all_data
from functions.recommend_games import base_recommend
import streamlit as st
# Modell 1


if "data_uploaded_transformed" in st.session_state:

    game_data, game_data_0_1, game_image_desc_data , image_and_description_data = load_all_data()


    base_recommend_data_profile = st.session_state["own_data_after_merge_before_lists"]
    
    st.header("Random Spieleempfehlung", help="Diese Empfehlung gibt Spiele aus einer Kombination der meistgespielten Genres, Tags und Kategorien")
    st.divider()
    if st.button("Drück mich"):
        base = base_recommend(base_recommend_data_profile, game_data)


        random_games = pd.merge(base, image_and_description_data, how="left", on="id")


        cols = st.columns(3)  # 3 columns per row

        for index, (_, row) in enumerate(random_games.iterrows()):
            with cols[index % 3]:
                st.image(row["image"], use_container_width=True)
                st.caption(f"{row['name']}")
    
