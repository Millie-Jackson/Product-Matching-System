"""
matchers/tfidf_matcher.py

Uses TF-IDF vectorisation to find the most similar match to a query
from a list of candidate product descriptions.
"""


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from matchers.clean_text import clean_text


def match_product(query: str, candidates: list[str]) -> tuple[str, float]:
    """Return the most similar product and its similarity score."""
    
    all_texts = [clean_text(query)] + [clean_text(c) for c in candidates]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Compare first item (query) with all others
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    best_index = similarities.argmax()
    best_score = similarities[best_index]
    best_match = candidates[best_index]

    return best_match, best_score