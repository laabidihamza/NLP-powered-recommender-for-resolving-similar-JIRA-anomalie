import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
from functions import col_embed, calculate_similarity, sentence_embed

model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

data_path = (
    "C:/Users/abidi/Documents/ISAMM/Stage - Vermeg/repo/WebApp/df_for_WebApp.csv"
)
data = pd.read_csv(data_path)


def show_search_page():
    st.title("Welcome to our Text Similarity Tester!")

    summary = st.text_input(
        "Enter your summary here:",
        max_chars=150,
        placeholder="Authentication  problem ...",
        disabled=False,
        label_visibility="visible",
    )

    description = st.text_area(
        "Enter your descriptionn here:",
        height=50,
        max_chars=500,
        placeholder="Authentication  problem ...",
        disabled=False,
        label_visibility="visible",
    )

    searchB = st.button("Search for similar issues")

    # @st.cache
    # def load_model():
    #     model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
    #     return model

    # model = load_model()

    if searchB:
        st.write("Searching for similar issues ...")
        st.write("Here are the top 5 most similar issues:")

        # Calculate the similarity between the input and the data
        def sentence_embeds(sentence):
            embedding = model.encode(sentence)
            return embedding

        summary_embedding = sentence_embeds(summary)
        sum_similarities = calculate_similarity(summary_embedding, data["Summary"])
        st.write(sum_similarities)
        st.write(summary_embedding)
        # # Sort the data by similarity
        # data = data.sort_values(by="similarity", ascending=False)

        # # Display the top 5 most similar issues
        # for i in range(5):
        #     st.write(f"Similarity: {data['similarity'].iloc[i]}")
        #     st.write(f"Summary: {data['Summary'].iloc[i]}")
        #     st.write(f"Description: {data['Description'].iloc[i]}")
        #     st.write("")

        # Store summaries with similarity > 0.7 and their scores in a list
        # similar_summaries_and_scores = []
        # for summary, similarity in zip(data["Summary"], sum_similarities):
        #     if similarity > 0.5:
        #         similar_summaries_and_scores.append((summary, similarity))

        # # Sort similar summaries by similarity score (highest first)
        # sorted_similar_summaries_and_scores = sorted(
        #     similar_summaries_and_scores, key=lambda x: x[1], reverse=True
        # )

        # # Print top 5 similar sentences and their scores
        # for i, (summary, similarity) in enumerate(sorted_similar_summaries_and_scores):
        #     if len(sum_similarities) == 0:
        #         st.write("No similar tickets found.")
        #     if i == 5:
        #         break  # Print only the top 5
        #     st.write(f"Similar summary: {summary} \n , Similarity: {similarity:.4f} \n")
