import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def main():
    st.title("Welcome to our Text Similarity Tester!")
    st.write("This is the main page")

    summary = st.text_input(
        "Enter your summary here:",
        max_chars=150,
        placeholder="Authentication  problem ...",
        disabled=False,
        label_visibility="visible",
    )

    st.write(f"You wrote {len(summary)} characters.")

    description = st.text_area(
        "Enter your descriptionn here:",
        height=50,
        max_chars=500,
        placeholder="Authentication  problem ...",
        disabled=False,
        label_visibility="visible",
    )

    st.write(f"You wrote {len(description)} characters.")

    searchB = st.button("Search for similar issues")
