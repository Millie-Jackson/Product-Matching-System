"""
match_products.py

Uses TF-IDF vectorisation and cosine similarity to find the closest matching product
from a list of candidates based on a user query. Ideal for building product matching tools
across supermarket datasets.
"""


from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def match_product(query, candidates):

    vectorizer = TfidfVectorizer()
    all_text = [query] + candidates
    tfidf = vectorizer.fit_transform(all_text)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    best_idx = sims.argmax()

    return candidates[best_idx], sims[best_idx]


query = "600g Boneless Chicken Breast"
candidates = ["Chicken Breast 640g", "Whole Chicken 1.2kg", "Tofu 400g"]

match, score = match_product(query, candidates)
print("Best Match:", match)
print("Score:", round(score, 2))