"""
matchers/store_matcher.py

Matches user queries to products per store and returns the best available matches
with associated pricing. Also supports full basket price calculation.
"""


import pandas as pd
from matchers.clean_text import clean_text
from matchers.quantity_parser import extract_weight
from matchers.tfidf_matcher import match_product as tfidf_match
from sentence_transformers import SentenceTransformer, util


# Load SBERT model
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")


def load_product_data(path="data/supermarket_products.csv") -> pd.DataFrame:
    """Load and return all available products with store and price info."""

    df = pd.read_csv(path)
    df["cleaned"] = df["product"].apply(clean_text)
    df["weight"] = df["product"].apply(extract_weight)

    return df

def sbert_match_product(query: str, candidates: list[str]) -> tuple[str, float]:
    """
    Find best match using SBERT sentence similarity.
    Returns the candidate string and its similarity score.
    """

    query_embedding = sbert_model.encode(query, convert_to_tensor=True)
    candidate_embeddings = sbert_model.encode(candidates, convert_to_tensor=True)
    
    scores = util.pytorch_cos_sim(query_embedding, candidate_embeddings)[0]
    best_idx = scores.argmax().item()
    best_score = scores[best_idx].item()

    return candidates[best_idx], best_score

def match_product_per_store(query: str, df: pd.DataFrame, threshold: float = 0.2, method: str = "tfidf") -> pd.DataFrame:
    """
    Given a query (e.g. '600g Chicken Breast') and a product dataset,
    return the best match in each store above threshold.
    """

    matched = []

    for store in df["store"].unique():
        subset = df[df["store"] == store].copy()
        if subset.empty:
            continue

        best_match, score = tfidf_match(query, list(subset["product"]))

        if score >= threshold:
            row = subset[subset["product"] == best_match].iloc[0]
            matched.append({
                "store": store,
                "query": query,
                "matched_product": best_match,
                "price": row["price"],
                "score": round(score, 3)
            })

    return pd.DataFrame(matched)

def calculate_total_price(queries: list[str], df: pd.DataFrame, threshold: float = 0.2, method: str = "tfidf") -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Given a list of queries and a product database, return total price per store,
    along with item-level breakdowns.
    """

    all_matches = []

    for query in queries:
        per_store = match_product_per_store(query, df, threshold, method)
        #all_matches.append(per_store)
        if not per_store.empty:
            all_matches.append(per_store)

    # If all are empty
    if not all_matches:
        return pd.DataFrame(columns=["store", "total_price"]), pd.DataFrame(columns=["query", "matched_product", "store", "price", "score"])

    combined = pd.concat(all_matches, ignore_index=True)

    # Defensive: ensure all required columns exist
    if "store" not in combined.columns or "price" not in combined.columns:
        return pd.DataFrame(columns=["store", "total_price"]), pd.DataFrame(columns=["query", "matched_product", "store", "price", "score"])

    totals = combined.groupby("store")["price"].sum().reset_index()
    totals = totals.rename(columns={"price": "total_price", })

    return totals, combined

