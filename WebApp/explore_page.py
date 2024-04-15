import streamlit as st
import pandas as pd

data_path = (
    "C:/Users/abidi/Documents/ISAMM/Stage - Vermeg/repo/WebApp/df_for_WebApp.pkl"
)
x = pd.read_pickle(data_path)


def show_explore_page():
    st.title("Welcome to our Text Similarity Tester!")
    st.write("This is the explore page")
    st.write("Here you can explore the data")
    st.write("Here are the top 5 most similar issues:")
    data = pd.read_csv("df_for_WebApp.csv")
    for i in range(5):
        st.write(f"Summary: {data['Summary'].iloc[i]}")
        st.write(f"Description: {data['Description'].iloc[i]}")
        st.write("")
