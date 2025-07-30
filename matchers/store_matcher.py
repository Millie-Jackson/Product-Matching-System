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
    """Load and return all available products with store and pricing info."""

    df = pd.read_csv(path)

    # Clean & extract weight
    df["cleaned"] = df["product"].apply(clean_text)
    df["weight"] = df["product"].apply(extract_weight)

    # Handle missing weights 1
    df["weight"] = df["weight"].fillna(1)

    # Calculate price per gram
    df["price_per_gram"] = df["price"] / df["weight"]

    return df

def sbert_match(query: str, candidates: list[str]) -> tuple[str, float]:
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

def match_product_per_store(query: str, df: pd.DataFrame, threshold: float = 0.2, method: str = "tfidf", prefer_value=True) -> pd.DataFrame:
    """
    Given a query (e.g. '600g Chicken Breast') and a product dataset,
    return the best match in each store above threshold.
    """

    matched = []

    for store in df["store"].unique():
        store_df = df[df["store"] == store]
        candidates = store_df["product"].tolist()

        if method == "sbert":
            best_match, score = sbert_match(query, candidates)
        else:
            best_match, score = tfidf_match(query, candidates)

        if score >= threshold:
            row = store_df[store_df["product"] == best_match].iloc[0]
            matched.append({
                "query": query,
                "matched_product": row["product"],
                "store": row["store"],
                "price": row["price"],
                "score": round(score, 3),
                "weight": row["weight"],
                "price_per_gram": round(row["price_per_gram"], 5)
            })
    # Preference for cheaper price per gram if multiple matches for same store
    if prefer_value:
        result_df = pd.DataFrame(matched).sort_values(by=["score", "price_per_gram"], ascending=[False, True])
    else:
        result_df = pd.DataFrame(matched).sort_values(by=["score"], ascending=False)

    return result_df.sort_values(by=["score", "price_per_gram"], ascending=[False, True]).reset_index(drop=True)

def calculate_total_price(queries: list[str], df: pd.DataFrame, threshold: float = 0.2, method: str = "tfidf", prefer_value=True) -> tuple[pd.DataFrame, pd.DataFrame]:
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

