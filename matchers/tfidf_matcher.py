# matchers/tfidf_matcher.py


"""
tfidf_matcher.py

Vectorises product descriptions using TF-IDF and calculates similarity
to find the most relevant match from a candidate list.
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