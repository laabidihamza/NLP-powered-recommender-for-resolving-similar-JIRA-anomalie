from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

def sentence_embed(sentence):
    embedding = model.encode(sentence)
    return embedding

def calculate_similarity(input_sentence, embeddings):
    similarities = []
    for embedding in embeddings:
        similarity = cosine_similarity(input_sentence.reshape(1, -1), embedding.reshape(1, -1))[0][0]
        similarities.append(similarity)

    return similarities



df = []
for i, (summary, similarity) in enumerate(zip(data["Summary"], sum_similarities)):
    if similarity > similarity_threshold:
        df.append(
            {
                "Summary": summary,
                "EmbeddingsSummary": data["EmbeddingsSummary"][i],
                "Description": data.loc[i, "Description"],
                "Comments": data.loc[i, "Comments"],
            }
        )
new_data = pd.DataFrame.from_records(df)



from sentence_transformers import SentenceTransformer, util

ss_model = SentenceTransformer("multi-qa-mpnet-base-cos-v1")

ss_description_embedding = ss_model.encode(description)

comments_for_similar_descriptions = []
for descript, similarity in sorted_similar_descriptions_and_scores:
    description_index = new_data[new_data["Description"] == descript].index[0]
    comment = new_data.loc[description_index, "Comments"]
    comments_for_similar_descriptions.append((comment))

emb_comments = []
for comment in comments_for_similar_descriptions:
    emb_com = ss_model.encode(comment)
    emb_comments.append(emb_com)

semantic_search = []
for i in emb_comments:
    ss_score = util.semantic_search(ss_description_embedding.reshape(1, -1), i)
    semantic_search.append(ss_score)

pip freeze > requirements.txt
