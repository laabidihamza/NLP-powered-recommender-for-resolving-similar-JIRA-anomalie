import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# from supabase import create_client, Client

# from dotenv import load_dotenv
# load_dotenv()

# import os

from search_page import show_search_page
from explore_page import show_explore_page

# url = os.environ.get("supabaseUrl")
# key = os.environ.get("supabaseKey")

# client = create_client(url, key)

# data_path = (
#     "C:/Users/abidi/Documents/ISAMM/Stage - Vermeg/repo/WebApp/df_for_WebApp.pkl"
# )
data_path = "df_for_WebApp.pkl"
data = pd.read_pickle(data_path)

st.set_page_config(page_title="Text Similarity Search", page_icon="📚")

# st.selectbox("Select a page", ["Home", "About", "Search"])
page = st.sidebar.selectbox("Explore Or Search", ["Search", "Explore"])

if page == "Explore":
    show_explore_page()
else:
    show_search_page(data)
