from flask import current_app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from sentence_transformers import SentenceTransformer


def calculate_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer(
        use_idf=True,
        norm='l2',
        ngram_range=(1, 2),
        sublinear_tf=True,
        analyzer='word'
    )
    tfidf = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])
    current_app.logger.info(f"Cosine similarity: {similarity[0][0]}")
    return similarity[0][0]

# def calculate_cosine_similarity_with_embeddings(text1, text2):
#     model = SentenceTransformer('all-MiniLM-L6-v2')

#     embeddings1 = model.encode(text1)
#     embeddings2 = model.encode(text2)
#     similarity = cosine_similarity([embeddings1], [embeddings2])
#     return similarity[0][0]
