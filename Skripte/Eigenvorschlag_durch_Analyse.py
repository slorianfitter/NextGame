import pandas as pd
from functions.Basemodell_v1 import base_recommend


# Import data

own_data = pd.read_csv("D:/Projekte/spielvorschlag/data/eigene_steam_daten.csv")
game_data = pd.read_csv("D:/Projekte/spielvorschlag/data/wanted_information.csv")
image_data = pd.read_csv("D:/Projekte/spielvorschlag/data/second_additional_info.csv")

# both have the same key "id" so we gonna join them together to know what kind of category i played over the last years on steam 
# and how long i played these categories

own_data = own_data[["appid","playtime_forever","rtime_last_played","playtime_2weeks"]]
own_data2 = own_data.rename(columns={"appid": "id"})
own_data_merged = pd.merge(own_data2, game_data, how="left", on="id")
print(own_data_merged)


# we now have combined the data but apparently we got some nas in the age column. 
# After i checked the ids i can confirm that theses ids are not listed in the appid list type = game that i crawled from steam.
# That is in fact fatal for the complete process because i now know that steam has some huge gaps in their documentation 
# although most of the games are listed in the shop and have accessible api


# We simply just drop these rows, because we cant use them. If there is no age, there will be no other useful data except the name and id.
# We could just implement an html request and grab the required information. 
# This takes time and obviously i dont want to wait minutes for an reqeuest.



data = own_data_merged.dropna(subset=["required_age"])

data["rtime_last_played"] = pd.to_datetime(data["rtime_last_played"], unit="s")


data = data[["id","name","required_age","playtime_forever","playtime_2weeks","rtime_last_played","released", "price_in_cents_no_discount", "genre","categories","feature"]]


data["categories"] = data["categories"].str.rstrip(";").str.split(";")
data["genre"] = data["genre"].str.rstrip(";").str.split(";")



## Lets begin with the Dashboard of my own Steamprofile

import streamlit as st
import plotly.express as px
import plotly.io as pio


st.set_page_config(page_title="Steam Dashboard",
                   layout="wide")



# ---- Sidebar element filter ----

st.sidebar.header("Select Filter Options")
st.sidebar.info("You can select multiple filter")


genre = data["genre"].copy()
genre_explode = genre.explode()
genre_finished_filter = genre_explode.unique()


category = data["categories"].copy()
category_explode = category.explode()
category_finished_filter = category_explode.unique()


selected_genres = st.sidebar.multiselect("Genres:", genre_finished_filter)
selected_categories = st.sidebar.multiselect("Categories", category_finished_filter)

# ----------------

# ---- Header ----

st.header("Let's see what you played the last few years on Steam")
st.divider()

# ----------------


# ---- List Overview of selected filter ----
st.text("List of selected filter options:")
col1_gen, col2_cat = st.columns(2)
with col1_gen:
    st.write("Selected genres:",selected_genres)
with col2_cat:
    st.write("Selected categories",selected_categories)

st.divider()
# ----------------


# ---- Data filter ----

if selected_genres:
    data_filtered= data[data["genre"].apply(lambda x: set(selected_genres).issubset(x))]
else:
    data_filtered = data


if selected_categories:
    data_filtered = data_filtered[data_filtered["categories"].apply(lambda x: set(selected_categories).issubset(x))]


# ---- Input Data ----

view = st.selectbox(
    "You want to see your input data?",
    ["No", "First 6 rows", "All data"]
)

if view == "First 6 rows":
    st.dataframe(data_filtered.head())
elif view == "All data":
    st.dataframe(data_filtered)

st.divider()

# ----------------

# ---- Most Played game x top games -----

data_filtered = pd.merge(data_filtered, image_data, how="left", on="id")
data_filtered = data_filtered.sort_values(by="playtime_forever", ascending=False)
data_filtered["playtime_forever"] = round(data_filtered["playtime_forever"] / 60,2)
data_filtered["playtime_2weeks"] = round(data_filtered["playtime_2weeks"]/60,2)

col1_top_game , col2_top_game = st.columns([1.5,1])


with col1_top_game:
    top_game = data_filtered.iloc[0]
    st.metric(
        label=f"Your #1 game - {top_game['playtime_forever']} h",
        value=f"{top_game["name"]}"
    )
        
    #get image
    image_top_game = top_game["image"]
    st.image(image_top_game, use_container_width= True)

with col2_top_game:
    top_games = data_filtered[1:13]  

    cols = st.columns(3)  # 3 columns per row

    for index, (_, row) in enumerate(top_games.iterrows()):
        with cols[index % 3]:
            st.image(row["image"], use_container_width=True)
            st.caption(f"{row['name']} - {row['playtime_forever']}h")




st.divider()


# ----  More Metric Information ----

col1_metrics, col2_metrics, col3_metrics = st.columns(3)


genre = data_filtered["genre"].copy()
genre_explode = genre.explode().str.strip()
genre_finished_filter = genre_explode.value_counts().reset_index()


category = data_filtered["categories"].copy()
category_explode = category.explode().str.strip()
category_finished_filter = category_explode.value_counts().reset_index()

with col1_metrics:
    fig1 = px.bar_polar(
        genre_finished_filter,
        r="count",
        theta="genre",
        color="count",
        title="Genres you played the most"
    )
    st.plotly_chart(fig1, use_container_width=True)


with col2_metrics:

    total_time = 14*24

    played_time = round(data_filtered["playtime_2weeks"].sum())

    junky_factor = played_time/ total_time

    games_played_last_weeks = data_filtered[data_filtered["playtime_2weeks"]>0]

    pie1 = px.pie(games_played_last_weeks,names="name", 
                  values="playtime_2weeks", 
                  title=f"Total playtime last 2 weeks - {played_time} h")

    st.plotly_chart(pie1, use_container_width=True)
  
    

with col3_metrics:
    fig2 = px.bar(
        category_finished_filter,
        x="count",
        y="categories",
        title="Categories you played the most"
    )
    st.plotly_chart(fig2, use_container_width=True)


st.divider()
st.header("Basemodell_v1: Spieleempfehlung")
st.text("Hier folgt die Anpassung an die Filter. Aktuell ist das Basemodell nur für das am häufigsten auftretende Genre ausgelegt!")
base = base_recommend(own_data)

st.dataframe(base)

