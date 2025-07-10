# matchers/tfidf_matcher.py


"""
tfidf_matcher.py

Vectorises product descriptions using TF-IDF and calculates similarity
to find the most relevant match from a candidate list.
"""


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from matchers.clean_text import clean_text


def match_product(query: str, candidates: list[str]) -> tuple[str, float]:

    all_texts = [clean_text(query)] + [clean_text(c) for c in candidates]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Compare first item (query) with all others
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    best_index = similarities.argmax()
    best_score = similarities[best_index]
    best_match = candidates[best_index]

    return best_match, best_score