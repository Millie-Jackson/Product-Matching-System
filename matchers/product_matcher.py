"""
matchers/product_matcher.py

Combines name similarity and quantity matching to select the best product.
Optionally penalises matches with large size differences.
"""


from matchers.clean_text import clean_text
from matchers.quantity_parser import extract_weight
from matchers.tfidf_matcher import match_product as tfidf_only_match


def match_product(query: str, candidates: list[str], weight_penalty: float = 0.001) -> tuple[str, float]:
    """
    Find the best matching product from a list using TF-IDF and optional weight penalty.

    - Uses TF-IDF similarity between the cleaned query and each candidate.
    - If both query and candidate have weights (e.g. 600g vs 500g), applies a penalty
      based on their absolute weight difference.
    
    Args:
        query (str): The product being searched.
        candidates (list[str]): List of candidate product names.
        weight_penalty (float): Penalty per gram difference in weight (default: 0.001).

    Returns:
        tuple[str, float]: The best matching product and its adjusted similarity score.
    """

    query_weight = extract_weight(clean_text(query))
    best_match = None
    best_score = -1.0

    for candidate in candidates:

        candidate_weight = extract_weight(clean_text(candidate)) 
        matched_text, score = tfidf_only_match(query, [candidate]) # -> (match, similarity)

        if query_weight is not None and candidate_weight is not None:
            weight_diff = abs(query_weight - candidate_weight)
            score -= weight_diff * weight_penalty # penalise larger size mismatches

        if score > best_score:
            best_score = score
            best_match = candidate

    return best_match, round(best_score, 4)
