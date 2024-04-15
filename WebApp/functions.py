import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")


def col_embeds(df):
    embeddings = []

    # Iterate through each row of the column
    for i in df:
        # Encode the sentence using the SBERT model
        embedding = model.encode(i)
        # Append the embedding to the list
        embeddings.append(embedding)

    return embeddings


def sentence_embed(sentence):
    embedding = model.encode(sentence)
    return embedding


def calculate_similarity(input_sentence, embeddings):
    # input_embedding = model.encode(input_sentence)

    similarities = []
    for embedding in embeddings:
        similarity = cosine_similarity(
            input_sentence.reshape(1, -1), embedding.reshape(1, -1)
        )[0][0]
        similarities.append(similarity)

    return similarities
