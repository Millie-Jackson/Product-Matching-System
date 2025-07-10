"""
product_embedding.py

Generates TF-IDF embeddings for a list of product descriptions and calculates
cosine similarity between them to identify likely matches. Useful for detecting
similar branded or own-brand items in different stores.
"""



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


products = [
    "600g Boneless Chicken Breast",
    "640g Chicken Fillet Pack",
    "Whole Chicken 1.2kg"
]


vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(products)


# Compare first item (query) with others
similarities = cosine_similarity(X[0:1], X[1:])
print(similarities) # -> array([[similarity_score_1, similarity_score_2]])