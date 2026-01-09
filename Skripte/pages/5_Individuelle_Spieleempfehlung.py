import pandas as pd
from functions.profile import profile
from functions.recommend_games import recommend_games
from functions.load_data import load_all_data
import streamlit as st
# Modell 1

game_data, game_data_0_1, game_image_desc_data , image_and_description_data = load_all_data()

if "data_uploaded_transformed" in st.session_state:

    own_data_merged_with_game_data = st.session_state["own_data_after_merge_before_lists"]
    
    st.header("Individuelle Spieleempfehlung aus Basis der Spiele")
    
    col_gew, col_zeitraum = st.columns(2)
    with col_gew:
        gewichtung_profil = st.checkbox("Möchtest du eine Gewichtung für dein Profil haben?")
    with col_zeitraum:
        zeitraum = st.checkbox("Möchtest du einen Vorschlag auf Basis der letzten 14 Tage?")


    if gewichtung_profil and zeitraum:
        profil = profile(own_data_merged_with_game_data, game_data_0_1, True, last_14_days=True)
    elif gewichtung_profil and not zeitraum:
        profil = profile(own_data_merged_with_game_data,game_data_0_1, True, last_14_days=False)
    elif not gewichtung_profil and zeitraum:
        profil = profile(own_data_merged_with_game_data, game_data_0_1,False, last_14_days=True)
    else:
        profil = profile(own_data_merged_with_game_data, game_data_0_1, False, last_14_days=False)

    st.dataframe(profil)
        

        # Profil bearbeitungsmöglichkeit
    st.divider()
    profil_bearbeitung = st.checkbox("Möchtest du das Profil bearbeiten?", help="Hier können Individuelle Präferenzen berücksichtigt werden.\n Beachte: Werte zwischen 0 und 1 können eingetragen werden.\n 'required_age' hat eine Skala von 0 bis 18 und 'price' kann Werte bis zu 1400 annehmen")
    if profil_bearbeitung:

        # Data Edit
        if "data_edit" not in st.session_state:
            st.session_state.data_edit = profil.copy()


            # Limitierung der Eingabewerte für Alter und Preis
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


        # gegenchek ob es eine Profilbearbeitung gab + Ausgabe des profils
    if not profil_bearbeitung:
        profil = profil
    else:
        profil = st.session_state.data_edit
        
        # verwendetes Profil ausgeben
    st.write("So sieht das Profil für die Berechnung aus:")
    st.dataframe(profil)
    st.divider()

        # --- Modelselection ---

    # wichtig für recommend games Funktion
    # nur möglich, weil gamedata und gamedata01 die gleichen daten haben sonst über index  
    game_data_0_1["positive_reviews"] = game_data["positive_reviews"]
    game_data_0_1["total_reviews"] = game_data["total_reviews"]   

    # Auswahlmöglichkeiten in Selectbox
    euc_cos = "Distanzmodell (teilweise ungenau)"
    rev_euc_cos = "Distanzmodell in Kombination mit Reviews (genauer)"
    filler = "-"

    # Selectbox für Modelle
    select_model = st.selectbox("Wähle das Model für die Prediction:", options=[filler,euc_cos, rev_euc_cos])

    own_data_for_models =  st.session_state["own_data"]
    # Modell 2 Cosinus Ähnlichkeit in Kombination mit euklidischer Distanz.
    if select_model == euc_cos:
        best_game = recommend_games(game_data_0_1,
                                    profil,
                                    set(own_data_for_models["id"]),
                                    use_reviews = False)

        
    # Modell 3 Reviews werden jetzt mit einbezogen.

    if select_model == rev_euc_cos:
        best_game = recommend_games(game_data_0_1,
                                    profil,
                                    set(own_data_for_models["id"]),
                                    use_reviews = True
                                    )

        st.dataframe(best_game)
        if "current_index" not in st.session_state:
            st.session_state.current_index = 0
    
            if st.button("doch lieber ein anderes Spiel?"):
                st.session_state.current_index +=1

            if st.session_state.current_index == len(best_game):
                st.session_state.current_index = 0

        current_game_index = best_game.index[st.session_state.current_index]
        game = game_image_desc_data.loc[current_game_index]

        # Darstellung für den User
        st.image(game["image"], use_container_width=True)
        st.subheader(game["name"], width="stretch")
        st.caption(game["short_description"])
    else:
        st.write("Es ist ein Fehler aufgetreten!")

