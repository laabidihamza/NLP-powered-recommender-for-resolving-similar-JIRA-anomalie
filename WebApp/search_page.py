import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity

# from functions import col_embeds, calculate_similarity, sentence_embed

model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
ss_model = SentenceTransformer("multi-qa-mpnet-base-cos-v1")

data_path = (
    "C:/Users/abidi/Documents/ISAMM/Stage - Vermeg/repo/WebApp/df_for_WebApp.pkl"
)
# data_path = "C:/Users/abidi/Documents/ISAMM/Stage - Vermeg/repo/Models_and_similarity_test/cleaned_data.csv"
data = pd.read_pickle(data_path)


def sentence_embed(sentence):
    embedding = model.encode(sentence)
    return embedding


@st.cache_data
def col_embed(df):
    embeddings = []
    for i in df:
        # Encode the sentence using the SBERT model
        embedding = model.encode(i)
        # Append the embedding to the list
        embeddings.append(embedding)
    return embeddings


@st.cache_data
def calculate_similarity(input_sentence, embeddings):
    similarities = []
    for embedding in embeddings:
        similarity = cosine_similarity(
            input_sentence.reshape(1, -1), embedding.reshape(1, -1)
        )[0][0]
        similarities.append(similarity)

    return similarities


def show_search_page():
    st.title("Welcome to our Text Similarity Tester!")

    summary = st.text_input(
        "Enter your summary here:",
        max_chars=150,
        placeholder="Exp: Authentication  problem ...",
        disabled=False,
        label_visibility="visible",
    )

    description = st.text_area(
        "Enter your descriptionn here:",
        height=50,
        max_chars=500,
        placeholder="Exp: I have authentication  problem ...",
        disabled=False,
        label_visibility="visible",
    )

    searchB = st.button("Search for similar issues")

    # @st.cache
    # def load_model():
    #     model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
    #     return model

    # model = load_model()

    # data['EmbeddingsSummary'] = col_embed(data['Summary'])

    if searchB:
        st.write("Searching for similar issues ...")
        st.write("Here are the top 5 most similar issues:")

        summary_embedding = sentence_embed(summary)
        sum_similarities = calculate_similarity(
            summary_embedding, data["EmbeddingsSummary"]
        )
        st.write("done")

        # Store summaries with similarity > 0.7 and their scores in a list
        similar_summaries_and_scores = []
        for summary, similarity in zip(data["Summary"], sum_similarities):
            if similarity > 0.5:
                similar_summaries_and_scores.append((summary, similarity))

        # Sort similar summaries by similarity score (highest first)
        sorted_similar_summaries_and_scores = sorted(
            similar_summaries_and_scores, key=lambda x: x[1], reverse=True
        )

        # Print top 5 similar sentences and their scores
        for i, (summary, similarity) in enumerate(sorted_similar_summaries_and_scores):
            if len(sum_similarities) == 0:
                st.write("No similar tickets found.")
            if i == 5:
                break  # Print only the top 5
            st.write(f"Similar summary: {summary}")
            st.write(f"Similarity: {similarity:.4f}")

        st.write("done for sum similarities")

        df = []
        for i, (summary, similarity) in enumerate(
            zip(data["Summary"], sum_similarities)
        ):
            if similarity > 0.5:
                df.append(
                    {
                        "Summary": summary,
                        "EmbeddingsSummary": data["EmbeddingsSummary"][i],
                        "Description": data.loc[i, "Description"],
                        "Comments": data.loc[i, "Comments"],
                    }
                )
        new_data = pd.DataFrame.from_records(df)
        new_data["Description"] = new_data["Description"].astype(str)
        new_data["EmbeddingsDescription"] = col_embed(new_data["Description"])
        st.write("done with description embeddings")
        st.write(type(new_data["EmbeddingsSummary"][0]))
        st.write(type(new_data["EmbeddingsDescription"][0]))
        description_embedding = sentence_embed(description)
        st.write(type(description_embedding))
        # Calculate similarity scores
        des_similarities = calculate_similarity(
            description_embedding, new_data["EmbeddingsDescription"]
        )
        # Store descriptions with similarity > 0.7 and their scores in a list
        similar_descriptions_and_scores = []
        for Description, similarity in zip(new_data["Description"], des_similarities):
            if similarity > 0.5:
                similar_descriptions_and_scores.append((Description, similarity))
        # Sort similar descriptions by similarity score (highest first)
        sorted_similar_descriptions_and_scores = sorted(
            similar_descriptions_and_scores, key=lambda x: x[1], reverse=True
        )
        # Print top 5 similar sentences and their scores
        for i, (Description, similarity) in enumerate(
            sorted_similar_descriptions_and_scores
        ):
            if len(des_similarities) == 0:
                st.write("No similar tickets found.")
            if i == 5:
                break  # Print only the top 5
            print(
                f"Similar Description: {Description} \n , Similarity: {similarity:.4f} \n"
            )
        st.write("done with des similarities")
        ss_description_embedding = ss_model.encode(description)
        comments_for_similar_descriptions = []
        for descript, similarity in similar_descriptions_and_scores:
            # Find the index of the matching description in the original DataFrame
            description_index = new_data[new_data["Description"] == descript].index[0]
            # Extract the corresponding comment
            comment = new_data.loc[description_index, "Comments"]
            # Append a tuple (description, similarity, comment) to the comments list
            comments_for_similar_descriptions.append((comment))
        emb_coms = []
        for comment in comments_for_similar_descriptions:
            emb_com = ss_model.encode(comment)
            emb_coms.append(emb_com)
        s_search = []
        for i in emb_coms:
            ss_score = util.semantic_search(ss_description_embedding.reshape(1, -1), i)
            s_search.append(ss_score)
        s_search1 = []
        for i in s_search:
            for j in i:
                s_search1.append(i)
        for i, sublist in enumerate(s_search):
            st.write(f"Sentence {i+1} similar descriptions:")
            for item in sublist:
                for j in item:
                    corpus_id = j["corpus_id"]
                    score = j["score"]
                    comment = comments_for_similar_descriptions[i][
                        corpus_id
                    ]  # Access comment by corpus_id
                    st.write(f"\t Score: {score:.2f}, \n Comment: {comment}")
