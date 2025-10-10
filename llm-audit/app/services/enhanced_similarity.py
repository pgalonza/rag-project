# import spacy
# import nltk
# nltk.download('wordnet')
# from nltk.corpus import wordnet
# from collections import Counter
# import numpy as np

# #Load spaCy model
# nlp = spacy.load("ru_core_news_sm")


# def get_synonyms(word):
#     synonyms = set()
#     for syn in wordnet.synsets(word):
#         for lemma in syn.lemmas():
#             synonyms.add(lemma.name())
#     return synonyms

# def preprocess_text(text):
#     doc = nlp(text.lower())
#     lemmatized_words = []
#     for token in doc:
#         if token.is_stop or token.is_punct:
#             continue
#         lemmatized_words.append(token.lemma_)
#     return lemmatized_words

# def expand_with_synonyms(words):
#     expanded_words = words.copy()
#     for word in words:
#         expanded_words.extend(get_synonyms(word))
#     return expanded_words

# def calculate_enhanced_similarity(text1, text2):
#     # Preprocess and tokenize texts
#     words1 = preprocess_text(text1)
#     words2 = preprocess_text(text2)

#     # Expand with synonyms
#     words1_expanded = expand_with_synonyms(words1)
#     words2_expanded = expand_with_synonyms(words2)

#     # Count word frequencies
#     freq1 = Counter(words1_expanded)
#     freq2 = Counter(words2_expanded)

#     # Create a set of all unique words
#     unique_words = set(freq1.keys()).union(set(freq2.keys()))

#     # Create frequency vectors
#     vector1 = [freq1[word] for word in unique_words]
#     vector2 = [freq2[word] for word in unique_words]

#     # Convert lists to numpy arrays
#     vector1 = np.array(vector1)
#     vector2 = np.array(vector2)

#     # Calculate cosine similarity
#     ces_cosine_similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

#     return ces_cosine_similarity