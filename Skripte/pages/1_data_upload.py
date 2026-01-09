import streamlit as st
import pandas as pd
from functions.load_data import load_all_data

st.set_page_config(page_title="Steam Dashboard", layout="wide")

game_data, game_data_0_1, game_image_desc_data , image_and_description_data = load_all_data()


with st.form("data_upload"):
    st.header("Beginnen wir mit einer Analyse deines Profils und enden mit einer Empfehlung für das nächste Spiel")
    uploaded_file = st.file_uploader("", type=["csv"])
    daten_laden = st.form_submit_button("Daten laden")

if uploaded_file is not None:
    try:
        uploaded_csv = pd.read_csv(uploaded_file)
        uploaded_df = uploaded_csv.rename(columns={"appid": "id"}) 

        # Daten in session_state speichern
        st.session_state["uploaded_df"] = uploaded_csv
        st.session_state["own_data"] = uploaded_df    

        own_data_page1 = st.session_state.own_data.drop(labels=["content_descriptorids"], axis=1)
        game_data_without_name = game_data.drop(labels=["name"], axis=1)
        
        # Leftjoin der Spieldaten mit den Userdaten für Profilvorbereitung und Analyse
        own_data_merged_with_game_data= pd.merge(own_data_page1, game_data_without_name, how="left", on="id")
        # Spiele ohne Alter werden gedroppt. -> Können nicht mehr auf Steam gekauft werden. 
        own_data_merged_with_game_data = own_data_merged_with_game_data.dropna(subset=["required_age"]) 

        #umbenennen der variable
        data = own_data_merged_with_game_data
        
        ## zwischenspeichern. Notwendig für die random games (model 1)
        st.session_state["own_data_after_merge_before_lists"] = data.copy()

        #Umwandeln in Datum
        data["rtime_last_played"] = pd.to_datetime(data["rtime_last_played"], unit="s")


        # Kategorien, Genre und Tags in strings gespeichert. Muss seperiert werden. 
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

        data["feature"] = (
            data["feature"].fillna("NA")
            .str.rstrip(";")
            .str.split(";")
            .apply(lambda lst: [x.strip() for x in lst])
        )
        st.session_state["data_uploaded_transformed"] = data

        own_data_page1 = st.session_state["data_uploaded_transformed"]
    
    except ValueError:
        st.header("Bitte benutze die richtige CSV")



if "data_uploaded_transformed" in st.session_state:
    st.divider()  
    own_data_page1 = st.session_state["data_uploaded_transformed"]

    view_first = st.selectbox(
    "Möchtest du die hochgeladenen Daten sehen?",
    ["-", "Die ersten 6 Einträge", "alle Daten"],
    help="Damit du die Daten sehen kannst, musst du mindestens einmal Daten hochgeladen haben"
    )
    
    if view_first == "Die ersten 6 Einträge":
        st.dataframe(
            own_data_page1.head()
            )
    
    if view_first == "Alle Daten":
        st.dataframe(
            own_data_page1
        )

