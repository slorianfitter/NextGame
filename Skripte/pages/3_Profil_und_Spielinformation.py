import pandas as pd
from functions.load_data import load_all_data
import streamlit as st
import plotly.express as px
import plotly.io as pio


game_data, game_data_0_1, game_image_desc_data , image_and_description_data = load_all_data()


st.session_state.data_filter_merged = pd.merge(st.session_state.data_filtered, image_and_description_data, how = "left", on = "id")
data_filter_merged = st.session_state["data_filter_merged"].sort_values(by = "playtime_forever", ascending = False)

data_filter_merged["playtime_forever"] = round(data_filter_merged["playtime_forever"] / 60 , 2)
data_filter_merged["playtime_2weeks"] = round(data_filter_merged["playtime_2weeks"]/60 , 2)

col1_top_game , col2_top_game = st.columns([1.5,1])

with col1_top_game:
    # top game
    top_game = data_filter_merged.iloc[0]
    st.metric(
        label=f"Dein #1 Game - {top_game['playtime_forever']} Std.",
        value=f"{top_game["name"]}"
    )
        
    #get image
    image_top_game = top_game["image"]
    st.image(image_top_game, use_container_width= True)

with col2_top_game:
    # die restlichen Platzierungen
    top_games = data_filter_merged[1:10]  

    cols = st.columns(3)  # 3 columns per row

    for index, (_, row) in enumerate(top_games.iterrows()):
        with cols[index % 3]:
            st.image(row["image"], use_container_width=True)
            st.caption(f"{row['name']} - {row['playtime_forever']} Std.")

st.divider()


# ----  Metric Information ----

col1_metrics, col2_metrics, col3_metrics = st.columns(3)


genre = data_filter_merged["genre"].copy()
genre_explode = genre.explode().str.strip()
genre_finished_filter = genre_explode.value_counts().reset_index()


category = data_filter_merged["categories"].copy()
category_explode = category.explode().str.strip()
category_finished_filter = category_explode.value_counts().reset_index()

# Barplot für die Genres
with col1_metrics:
    fig1 = px.bar_polar(
        genre_finished_filter,
        r="count",
        theta="genre",
        color="count",
        title="Genres, die am meisten gespielt werden"
    )
    st.plotly_chart(fig1, use_container_width=True)

# Pie chart für die gespielten Stunden der letzten 2 Wochen
with col2_metrics:

    total_time = 14*24

    played_time = round(data_filter_merged["playtime_2weeks"].sum())

    junky_factor = played_time/ total_time

    games_played_last_weeks = data_filter_merged[data_filter_merged["playtime_2weeks"]>0]

    pie1 = px.pie(games_played_last_weeks,names="name", 
                values="playtime_2weeks", 
                title=f"Spielzeit der letzten 2 wochen - {played_time} Std.")

    st.plotly_chart(pie1, use_container_width=True)

    
# Bar-plot für die gespielten Kategorien
with col3_metrics:
    fig2 = px.bar(
        category_finished_filter,
        x="count",
        y="categories",
        title="Kategorien, die am meisten gespielt werden"
    )
    st.plotly_chart(fig2, use_container_width=True)