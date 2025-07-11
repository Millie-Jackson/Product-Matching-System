# matcher/product_matcher.py


"""
product_matcher.py

Combines name similarity and quantity matching to select the best product.
Optionally penalises matches with large size differences.
"""


from matchers.clean_text import clean_text
from matchers.quantity_parser import extract_weight
from matchers.tfidf_matcher import match_product as tfidf_only_match
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def match_product(query: str, candidates: list[str], weight_penalty: float = 0.001) -> tuple[str, float]:
    """
    Finds the best matching product using both text similarity and weight difference.
    A small penalty is subtracted based on the absolute size difference (in grams).
    """

    query_weight = extract_weight(clean_text(query))
    best_match = None
    best_score = -1

    for candidate in candidates:

        candidate_weight = extract_weight(clean_text(candidate)) 
        match_text, score = tfidf_only_match(query, [candidate]) # -> (match, similarity)

        if query_weight and candidate_weight:
            diff = abs(query_weight - candidate_weight)
            score -= diff * weight_penalty # penalise larger size mismatches

        if score > best_score:
            best_score = score
            best_match = candidate

    return best_match, round(best_score, 4)
