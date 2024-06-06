import pandas as pd
import json
import time

import streamlit as st

from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity

# initialize state
if "model" not in st.session_state:
    st.session_state.model = None

if "ss_model" not in st.session_state:
    st.session_state.ss_model = None

@st.cache_data
def load_models():
    st.session_state.model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
    st.session_state.ss_model = SentenceTransformer("multi-qa-mpnet-base-cos-v1")
load_models()

model = st.session_state.model
ss_model = st.session_state.ss_model

def show_search_page(data,supabase,username):

    st.subheader("Find solutions for your JIRA problems.")

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
        max_chars=1600,
        placeholder="Exp: I have authentication  problem ...",
        disabled=False,
        label_visibility="visible",
    )

    # initialize state
    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False

    def callback():
        st.session_state.button_clicked = True

    similarity_threshold = st.slider(
        "Similarity threshold", 0.0, 1.0, 0.5, 0.05, format="%.2f"
    )

    searchB = st.button("Search for similar issues", on_click=callback)

    # @st.cache_data
    def sentence_embed(sentence):
        embedding = model.encode(sentence)
        return embedding

    # @st.cache_data
    def col_embed(df):
        embeddings = []
        for i in df:
            # Encode the sentence using the SBERT model
            embedding = model.encode(i)
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
    
    if searchB:
        if summary and description:

            pl = st.empty()
            pl.write("Searching for similar issues ...")
            summary_embedding = sentence_embed(summary)
            sum_similarities = calculate_similarity(
                summary_embedding, data["EmbeddingsSummary"]
            )
            summary_embedding = summary_embedding.tolist()
            summary_embedding = json.dumps(summary_embedding)

            # Store summaries with similarity > 0.7 and their scores in a list
            similar_summaries_and_scores = []
            for summ, similarity in zip(data["Summary"], sum_similarities):
                if similarity > similarity_threshold:
                    similar_summaries_and_scores.append((summ, similarity))

            # Sort similar summaries by similarity score (highest first)
            sorted_similar_summaries_and_scores = sorted(
                similar_summaries_and_scores, key=lambda x: x[1], reverse=True
            )

            if len(sorted_similar_summaries_and_scores) == 0:
                pl.empty()
                sum_warning_placeholder = st.empty()
                sum_warning_placeholder.warning("No similar tickets found.")
                time.sleep(3)
                sum_warning_placeholder.empty()
            else:
                with st.expander("Show similar summaries"):
                    # Print top 5 similar sentences and their scores
                    for i, (summar, similarity) in enumerate(sorted_similar_summaries_and_scores):
                        if i == 5:
                            break  
                        st.write(f" **Similarity:** {similarity:.4f} ,")
                        st.write(f" **Similar summary:** {summar}")

                df = []
                for i, (summa, similarity) in enumerate(
                    zip(data["Summary"], sum_similarities)
                ):
                    if similarity > similarity_threshold:
                        df.append(
                            {
                                "Summary": summa,
                                "EmbeddingsSummary": data["EmbeddingsSummary"][i],
                                "Description": data.loc[i, "Description"],
                                "Comments": data.loc[i, "Comments"],
                            }
                        )
                new_data = pd.DataFrame.from_records(df)
                new_data["Description"] = new_data["Description"].astype(str)
                with st.spinner("Descriptions embedding ..."):
                    new_data["EmbeddingsDescription"] = col_embed(new_data["Description"])

                description_embedding = sentence_embed(description)

                # Calculate similarity scores
                des_similarities = calculate_similarity(
                    description_embedding, new_data["EmbeddingsDescription"]
                )

                description_embedding = description_embedding.tolist()
                description_embedding = json.dumps(description_embedding)

                response = supabase.table("users").select("user_id").eq("username", username).execute()
                user_data = response.data

                user_id = user_data[0]['user_id']

                # Insert user search into the database
                response = supabase.table("user_search").insert({
                    "user_id": user_id,
                    "summary": summary,
                    "description": description,
                    "embeddingssummary": summary_embedding,  
                    "embeddingsdescription": description_embedding
                }).execute()
                
                # Store descriptions with similarity > 0.7 and their scores in a list
                similar_descriptions_and_scores = []
                for Description, similarity in zip(new_data["Description"], des_similarities):
                    if similarity > similarity_threshold:
                        similar_descriptions_and_scores.append((Description, similarity))
                # Sort similar descriptions by similarity score (highest first)
                sorted_similar_descriptions_and_scores = sorted(
                    similar_descriptions_and_scores, key=lambda x: x[1], reverse=True
                )

                if len(sorted_similar_descriptions_and_scores) == 0:

                    pl.empty()
                    des_warning_placeholder = st.empty()
                    des_warning_placeholder.warning("No similar tickets found.")
                    time.sleep(3)
                    des_warning_placeholder.empty()
                else :
                    with st.expander("Show Similar Descriptions"):
                        # Print top 5 similar sentences and their scores
                        for i, (Description, similarity) in enumerate(sorted_similar_descriptions_and_scores):
                            if i == 5:
                                break  
                            st.write(f" **Similarity:** {similarity:.4f} ,")
                            st.write(f" **Similar Description:** {Description}")

                    ss_description_embedding = ss_model.encode(description)
                    
                    comments_for_similar_descriptions = []
                    for descript, similarity in sorted_similar_descriptions_and_scores:
                        # Find the index of the matching description in the original DataFrame
                        description_index = new_data[new_data["Description"] == descript].index[0]
                        # Extract the corresponding comment
                        comment = new_data.loc[description_index, "Comments"]
                        # Append a tuple (description, similarity, comment) to the comments list
                        comments_for_similar_descriptions.append((comment))

                    emb_coms = []
                    with st.spinner("Comments embedding ..."):
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

                    pl.empty()

                    for i, sublist in enumerate(s_search):
                        st.subheader(f"Sentence {i+1} similar descriptions:")
                        for item in sublist:
                            for j in item:
                                corpus_id = j["corpus_id"]
                                score = j["score"]
                                comment = comments_for_similar_descriptions[i][
                                    corpus_id
                                ]  # Access comment by corpus_id
                                if score > 0.1:
                                    st.write(f"Score: {score:.2f},")
                                    st.write(f"Comment: {comment}")
                                else:
                                    break

                    st.balloons()
                    st.success("Found similar issues")
        else:
            # Placeholder for the warning message
            warning_placeholder = st.empty()
            # warning_shown = st.warning("Please enter a summary and description.")
            warning_placeholder.warning("Please enter a summary and description.")
            time.sleep(3)
            warning_placeholder.empty()
