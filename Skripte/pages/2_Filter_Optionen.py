import streamlit as st
st.set_page_config(page_title="Steam Dashboard", layout="wide")
from functions.load_data import load_all_data
import pandas as pd

game_data, game_data_0_1, game_image_desc_data , image_and_description_data = load_all_data()






if "uploaded_df" in st.session_state:
    # ---- Filter-Form ----
        # Erstellung von Listen für die Filter. Sichtbare Listen für den User
    if "selected_genres" not in st.session_state:
        st.session_state.selected_genres = []
    if "selected_categories" not in st.session_state:
        st.session_state.selected_categories = []
    if "selected_tags" not in st.session_state:
        st.session_state.selected_tags = []  

    
    data = st.session_state["data_uploaded_transformed"]

    with st.form("filter_data"):
            # Explodierte Listen für Filteroptionen
            genre_finished_filter = sorted(data["genre"].explode().unique())
            category_finished_filter = sorted(data["categories"].explode().unique())
            tags_finished_filter = sorted(data["tags"].explode().unique())

            st.header("Filteroptionen für deinen Daten")

            # Filter-Auswahl in 3 Spalten. Filter wird für alle Metriken angewendet.

            col1, col2, col3 = st.columns(3)
            with col1:
                genre_input = st.multiselect("Genres:", genre_finished_filter, default=st.session_state.selected_genres)
            with col2:
                category_input = st.multiselect("Categories", category_finished_filter, default=st.session_state.selected_categories)
            with col3:
                tags_input = st.multiselect("Tags:", tags_finished_filter, default=st.session_state.selected_tags)

            st.divider()

            st.text("Liste der ausgewählten Filter:")
            # Listen für die Ausgewählten Filter, damit der User sehen kann, was er gewählt hat        
            col1_gen, col2_cat, col3_tag = st.columns(3)
            with col1_gen:
                st.write("ausgewählte Genres:", genre_input)
            with col2_cat:
                st.write("ausgewählte Kategorien:", category_input)
            with col3_tag:
                st.write("ausgewählte Tags:", tags_input)

            st.divider()
            # Speicherung der Filter
            save_filter = st.form_submit_button("Filter anwenden")

        # ---- Session State aktualisieren bei Button-Klick ----
        
            if save_filter:
                #Laden der Filter in die Session
                st.session_state.selected_genres = genre_input
                st.session_state.selected_categories = category_input
                st.session_state.selected_tags = tags_input

            # ---- DataFrame filtern ----
            # Filterung der Spiele basierend auf dem ausgewählten Filter
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
    "Möchtest du die gefilterten Daten sehen?",
    ["-", "Die ersten 6 Einträge", "alle Daten"]
    )

    if view == "Die ersten 6 Einträge":
        st.dataframe(data_filtered.head())
    elif view == "Alle Daten":
        st.dataframe(data_filtered)


    st.session_state["data_filtered"] = data_filtered
else:
    st.warning("Keine Datei hochgeladen! Bitte gehe zurück zu Seite 1 und lade eine CSV hoch.")

