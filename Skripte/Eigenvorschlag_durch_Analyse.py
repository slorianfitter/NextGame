import pandas as pd
from functions.Basemodell_v1 import base_recommend
from functions.profile import profile
from functions.cos_similarity import cos_similarity
from functions.euc_distance import euklidische_distanz
from functions.better_reviews import agresti_coull
import streamlit as st
import plotly.express as px
import plotly.io as pio

# Import der notwendigen Daten

game_data = pd.read_csv("/mount/src/nextgame/data/full_data_v1.csv")


game_data_0_1_part1 = pd.read_csv("/mount/src/nextgame/data/full_data_0_1_part1.csv", sep=";")
game_data_0_1_part2 = pd.read_csv("/mount/src/nextgame/data/full_data_0_1_part2.csv",sep=";")
game_data_0_1 = pd.merge(game_data_0_1_part1,game_data_0_1_part2,how="outer")
game_data_0_1 = game_data_0_1.sort_values(by="id")
image_and_description_data = pd.read_csv("/mount/src/nextgame/data/image_and_description_data.csv")


st.header("App für eine Spielempfehlung auf Basis deines Profils")
uploaded_file = st.file_uploader("", type=["csv"])

if uploaded_file is not None:
    uploaded_file = pd.read_csv(uploaded_file)
    uploaded_file = uploaded_file.rename(columns={"appid": "id"})

    own_data = uploaded_file.copy()
    own_data = own_data.rename(columns={"appid": "id"})
    own_data = own_data[["id","playtime_forever","rtime_last_played","playtime_2weeks"]]

    own_data_merged_with_game_data= pd.merge(own_data, game_data, how="left", on="id")

    # Die Spieldaten sind nun mit den Userdaten gemerged. Dadurch haben wir Zugriff auf alles mögliche 



    own_data_merged_with_game_data = own_data_merged_with_game_data.dropna(subset=["required_age"])


    data = own_data_merged_with_game_data.copy()

    # einige Anpassungen der Daten für später
    data["rtime_last_played"] = pd.to_datetime(data["rtime_last_played"], unit="s")
    data = data[["id","name","price","required_age","playtime_forever","playtime_2weeks","rtime_last_played","released", "genre","categories", "tags","feature"]]
    # Kategorien
    data["categories"] = (
        data["categories"].fillna("NA")
        .str.rstrip(";")
        .str.split(";")
        .apply(lambda lst: [x.strip() for x in lst])
    )

    # Genre
    data["genre"] = (
        data["genre"].fillna("NA")
        .str.rstrip(";")
        .str.split(";")
        .apply(lambda lst: [x.strip() for x in lst])
    )

    # Tags
    data["tags"] = (
        data["tags"].fillna("NA")
        .str.rstrip(";")
        .str.split(";")
        .apply(lambda lst: [x.strip() for x in lst])
    )


    # Hier beginnen wir mit dem Streamlit layout
    st.set_page_config(page_title="Steam Dashboard",
                    layout="wide")

    # ---- Streamlit Layout ----
    st.set_page_config(page_title="Steam Dashboard", layout="wide")

    # ---- Session State initialisieren (vor Filterung!) ----
    if "selected_genres" not in st.session_state:
        st.session_state.selected_genres = []
    if "selected_categories" not in st.session_state:
        st.session_state.selected_categories = []
    if "selected_tags" not in st.session_state:
        st.session_state.selected_tags = []

    # ---- Filter-Form ----
    with st.form("filter_data"):
        # Explodierte Listen für Filteroptionen
        genre_finished_filter = data["genre"].explode().unique()
        category_finished_filter = data["categories"].explode().unique()
        tags_finished_filter = data["tags"].explode().unique()

        st.header("Schauen wir uns doch mal an, was du so die letzte Zeit auf Steam getrieben hast")
        st.divider()

        # Filter-Auswahl in 3 Spalten
        col1, col2, col3 = st.columns(3)
        with col1:
            genre_input = st.multiselect("Genres:", genre_finished_filter, default=st.session_state.selected_genres)
        with col2:
            category_input = st.multiselect("Categories", category_finished_filter, default=st.session_state.selected_categories)
        with col3:
            tags_input = st.multiselect("Tags:", tags_finished_filter, default=st.session_state.selected_tags)

        st.divider()
        st.text("Liste der ausgewählten Filter:", help="Filter können in der Seitenleiste ausgewählt werden")
        col1_gen, col2_cat, col3_tag = st.columns(3)
        with col1_gen:
            st.write("ausgewählte Genres:", genre_input)
        with col2_cat:
            st.write("ausgewählte Kategorien:", category_input)
        with col3_tag:
            st.write("ausgewählte Tags:", tags_input)

        st.divider()
        save_filter = st.form_submit_button("Filter anwenden")

    # ---- Session State aktualisieren bei Button-Klick ----
    if save_filter:
        st.session_state.selected_genres = genre_input
        st.session_state.selected_categories = category_input
        st.session_state.selected_tags = tags_input

    # ---- DataFrame filtern ----
    data_filtered = data.copy()

    if st.session_state.selected_genres:
        data_filtered = data_filtered[
            data_filtered["genre"].apply(lambda x: set(st.session_state.selected_genres).issubset(x))
        ]

    if st.session_state.selected_categories:
        data_filtered = data_filtered[
            data_filtered["categories"].apply(lambda x: set(st.session_state.selected_categories).issubset(x))
        ]

    if st.session_state.selected_tags:
        data_filtered = data_filtered[
            data_filtered["tags"].apply(lambda x: set(st.session_state.selected_tags).issubset(x))
        ]

    # ---- Input Data anzeigen ----
    view = st.selectbox(
        "Möchtest du deine Daten sehen?",
        ["-", "Die ersten 6 Einträge", "alle Daten"]
    )

    if view == "Die ersten 6 Einträge":
        st.dataframe(data_filtered.head())
    elif view == "Alle Daten":
        st.dataframe(data_filtered)



    st.divider()

    # ---- Most Played game x top games -----

    data_filtered = pd.merge(data_filtered, image_and_description_data, how="left", on="id")
    data_filtered = data_filtered.sort_values(by="playtime_forever", ascending=False)
    data_filtered["playtime_forever"] = round(data_filtered["playtime_forever"] / 60,2)
    data_filtered["playtime_2weeks"] = round(data_filtered["playtime_2weeks"]/60,2)

    col1_top_game , col2_top_game = st.columns([1.5,1])


    with col1_top_game:
        top_game = data_filtered.iloc[0]
        st.metric(
            label=f"Your #1 game - {top_game['playtime_forever']} Std.",
            value=f"{top_game["name"]}"
        )
            
        #get image
        image_top_game = top_game["image"]
        st.image(image_top_game, use_container_width= True)

    with col2_top_game:
        top_games = data_filtered[1:10]  

        cols = st.columns(3)  # 3 columns per row

        for index, (_, row) in enumerate(top_games.iterrows()):
            with cols[index % 3]:
                st.image(row["image"], use_container_width=True)
                st.caption(f"{row['name']} - {row['playtime_forever']} Std.")




    st.divider()


    # ----  Metric Information ----

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
            title="Genres, die am meisten gespielt werden"
        )
        st.plotly_chart(fig1, use_container_width=True)


    with col2_metrics:

        total_time = 14*24

        played_time = round(data_filtered["playtime_2weeks"].sum())

        junky_factor = played_time/ total_time

        games_played_last_weeks = data_filtered[data_filtered["playtime_2weeks"]>0]

        pie1 = px.pie(games_played_last_weeks,names="name", 
                    values="playtime_2weeks", 
                    title=f"Spielzeit der letzten 2 wochen - {played_time} Std.")

        st.plotly_chart(pie1, use_container_width=True)
    
        

    with col3_metrics:
        fig2 = px.bar(
            category_finished_filter,
            x="count",
            y="categories",
            title="Kategorien, die am meisten gespielt werden"
        )
        st.plotly_chart(fig2, use_container_width=True)


    st.divider()



# Modell 1
    st.header("Random Spieleempfehlung", help="Diese Empfehlung gibt Spiele aus einer Kombination der meistgespielten Genres, Tags und Kategorien")
    if st.button("Drück mich"):
        base = base_recommend(own_data_merged_with_game_data, game_data)


        random_games = pd.merge(base, image_and_description_data, how="left", on="id")


        cols = st.columns(3)  # 3 columns per row

        for index, (_, row) in enumerate(random_games.iterrows()):
            with cols[index % 3]:
                st.image(row["image"], use_container_width=True)
                st.caption(f"{row['name']}")

    st.divider()



    # Profil erstellung

    st.header("Individuelle Spieleempfehlung aus Basis der Spiele")
    
    col_gew, col_zeitraum = st.columns(2)
    with col_gew:
        gewichtung_profil = st.checkbox("Möchtest du eine Gewichtung für dein Profil haben?")
    with col_zeitraum:
        zeitraum = st.checkbox("Möchtest du einen Vorschlag auf Basis der letzten 14 Tage?")

    profil_daten = pd.merge(own_data, game_data_0_1, how="left", on="id")
    if gewichtung_profil and zeitraum:
        profil = profile(profil_daten, True, last_14_days=True)
    elif gewichtung_profil and not zeitraum:
        profil = profile(profil_daten, True, last_14_days=False)
    elif not gewichtung_profil and zeitraum:
        profil = profile(profil_daten, False, last_14_days=True)
    else:
        profil = profile(profil_daten, False, last_14_days=False)

    st.dataframe(profil)
    st.divider()
    profil_bearbeitung = st.checkbox("Möchtest du das Profil bearbeiten?", help="Hier können Individuelle Präferenzen berücksichtigt werden.\n Beachte: Werte zwischen 0 und 1 können eingetragen werden.\n 'required_age' hat eine Skala von 0 bis 18 und 'price' kann Werte bis zu 1400 annehmen")
    if profil_bearbeitung:

        if "data_edit" not in st.session_state:
            st.session_state.data_edit = profil.copy()

        with st.form("edit_form"):
            column_config = {
                "required_age": st.column_config.NumberColumn(
                    "required_age",
                    min_value=0,
                    step=0.001,
                    max_value =18
                ),
                "price": st.column_config.NumberColumn(
                    "price",
                    min_value=0.0,
                    step=0.01,
                    max_value = game_data["price"].max()
                )
            }

            # Alle anderen Spalten z. B. 0–1
            for col in st.session_state.data_edit.columns:
                if col not in column_config:
                    column_config[col] = st.column_config.NumberColumn(
                        col,
                        min_value=0.0,
                        max_value=1.0,
                        step=0.01
                    )

            data_edit = st.data_editor(
                st.session_state.data_edit,
                key="editor",
                use_container_width=True,
                column_config=column_config
            )

            # Button
            save = st.form_submit_button("Änderungen übernehmen")

        # Nach Submit übernehmen wir die Änderungen
        if save:
            st.session_state.data_edit = data_edit
            st.success("Änderungen gespeichert!")
    
    st.divider()
    st.write("So sieht das Profil für die Berechnung aus:")

    if not profil_bearbeitung:
        profil

        profil = profil
    else:
        st.session_state.data_edit
        profil = st.session_state.data_edit
    


    st.divider()

    
    # Modell 2 Cosinus Ähnlichkeit in Kombination mit euklidischer Distanz.


    #join der spieldaten und image_daten:
    game_image_desc_data = pd.merge(game_data, image_and_description_data, "left", on="id")
    # Davor müssen aber Preis und Alter normalisiert werden, da diese sonst das ausschlaggebene Argument sind
    euc_cos = "Distanzmodell (teilweise ungenau)"
    rev_euc_cos = "Distanzmodell in Kombination mit Reviews (genauer)"
    filler = "-"

    select_model = st.selectbox("Wähle das Model für die Prediction:", options=[filler,euc_cos, rev_euc_cos])
    if select_model == euc_cos:
        game_data_norm = game_data_0_1.copy()
        profil_norm = profil.copy()

        alter_max = game_data_norm["required_age"].max()
        game_data_norm["required_age"] = 1 - (alter_max - game_data_norm["required_age"]) / alter_max
        profil_norm["required_age"] = 1 - (alter_max - profil_norm["required_age"]) / alter_max

        preis_max = game_data_norm["price"].max()
        game_data_norm["price"] = 1 - (preis_max - game_data_norm["price"]) / preis_max
        profil_norm["price"] = 1 - (preis_max - profil_norm["price"]) / preis_max

        cos = cos_similarity(profil_norm, game_data_norm)
        filter_cos_sim = 0.6
        cos_filtered = cos[cos["cosine_similarity"] > filter_cos_sim]

        game_data_filtered = game_data_0_1.loc[cos_filtered.index]


        euc_dist = euklidische_distanz(profil_norm, game_data_filtered)

        top_indices = euc_dist.head(20).index
        game_predicition_cos_euc = game_data_filtered.loc[top_indices]
        game_predicition_cos_euc = game_predicition_cos_euc[~game_predicition_cos_euc["id"].isin(own_data["id"])]
        euc_dist = euc_dist[euc_dist.index.isin(game_predicition_cos_euc.index)]


        best_game = pd.Series(euc_dist["euc_distance"], name="best_fit").sort_values(ascending=False)


        if "current_index" not in st.session_state:
            st.session_state.current_index = 0
        
        if st.button("doch lieber ein anderes Spiel?"):
            st.session_state.current_index +=1

            if st.session_state.current_index >= len(best_game):
                st.session_state.current_index = 0


        current_game_index = best_game.index[st.session_state.current_index]
        game = game_image_desc_data.iloc[current_game_index]


        st.image(game["image"], use_container_width=True)
        st.subheader(game["name"], width="stretch")
        st.caption(game["short_description"])

        


# Modell 3 Reviews werden jetzt mit einbezogen.

    if select_model == rev_euc_cos:

        game_data_norm = game_data_0_1.copy()
        profil_norm = profil.copy()

        alter_max = game_data_norm["required_age"].max()
        game_data_norm["required_age"] = 1 - (alter_max - game_data_norm["required_age"]) / alter_max
        profil_norm["required_age"] = 1 - (alter_max - profil_norm["required_age"]) / alter_max

        preis_max = game_data_norm["price"].max()
        game_data_norm["price"] = 1 - (preis_max - game_data_norm["price"]) / preis_max
        profil_norm["price"] = 1 - (preis_max - profil_norm["price"]) / preis_max

        cos = cos_similarity(profil_norm, game_data_norm)
        filter_cos_sim = 0.6
        cos_filtered = cos[cos["cosine_similarity"] > filter_cos_sim]

        game_data_filtered = game_data_0_1.loc[cos_filtered.index]


        euc_dist = euklidische_distanz(profil_norm, game_data_filtered)

        top_indices = euc_dist.head(20).index
        game_predicition_cos_euc = game_data_filtered.loc[top_indices]
        game_predicition_cos_euc = game_predicition_cos_euc[~game_predicition_cos_euc["id"].isin(own_data["id"])]
        euc_dist = euc_dist[euc_dist.index.isin(game_predicition_cos_euc.index)]


        reviews_game_prediciton = agresti_coull(game_predicition_cos_euc, days_30=False)

        euc_dist_norm = 1- (euc_dist.max()-euc_dist)/euc_dist.max()
        
        p = 0.4
        best_game = (p*euc_dist_norm["euc_distance"] + (1-p)*reviews_game_prediciton) / 2

        best_game = pd.Series(best_game, name="best_fit").sort_values(ascending=False)

        if "current_index" not in st.session_state:
            st.session_state.current_index = 0
        
        if st.button("doch lieber ein anderes Spiel?"):
            st.session_state.current_index +=1

            if st.session_state.current_index >= len(best_game):
                st.session_state.current_index = 0


        current_game_index = best_game.index[st.session_state.current_index]
        game = game_image_desc_data.iloc[current_game_index]


        st.image(game["image"], use_container_width=True)
        st.subheader(game["name"], width="stretch")
        st.caption(game["short_description"])





