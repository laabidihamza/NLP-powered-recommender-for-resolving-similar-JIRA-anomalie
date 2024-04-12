import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from search_page import show_search_page
from explore_page import show_explore_page

st.set_page_config(page_title="Text Similarity Search", page_icon="📚")

# st.selectbox("Select a page", ["Home", "About", "Search"])
page = st.sidebar.selectbox("Explore Or Search", ["Search", "Explore"])

if page == "Explore":
    show_explore_page()
else:
    show_search_page()
