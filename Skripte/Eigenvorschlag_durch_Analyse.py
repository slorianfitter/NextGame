import pandas as pd
import os
from functions.Basemodell_v1 import base_recommend
from functions.profile import profile
from functions.cos_similarity import cos_similarity
from functions.euc_distance import euklidische_distanz
from functions.better_reviews import agresti_coull
import streamlit as st
import plotly.express as px
import plotly.io as pio

st.write("Working dir:", os.getcwd())
st.write("Files in root:", os.listdir())
st.write("Files in data:", os.listdir("data") if os.path.exists("data") else "data folder not found")
st.write("Files in functions:", os.listdir("functions") if os.path.exists("functions") else "functions folder not found")

# Import der notwendigen Daten




