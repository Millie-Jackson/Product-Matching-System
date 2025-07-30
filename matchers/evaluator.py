"""
matches/evaluator.py

Provides a function to evaluate matcher performance on a labelled test set.
Generates summary statistics and a CSV file with all predictions.
"""


import pandas as pd
import os
from datetime import datetime
from matchers.store_matcher import calculate_total_price, load_product_data


TESTSET_PATH = "data/testset.csv"
PRODUCTS_PATH = "data/supermarket_products.csv"


def run_evaluation(method: str = "tfidf", prefer_value: bool = True, run_both: bool = False):

    df = pd.read_csv(TESTSET_PATH)
    product_df = load_product_data(PRODUCTS_PATH)

    methods_to_run = [method] if not run_both else ["tfidf", "sbert"]
    all_summaries = []
    last_csv_path = None

    for m in methods_to_run:
        results = []
        correct = 0
        total_score = 0

        for _, row in df.iterrows():
            query = row["query"]
            expected = row["expected_match"]

            totals, breakdown = calculate_total_price([query], product_df, threshold=0.0, method=method, prefer_value=prefer_value)
            if breakdown.empty:
                results.append({"query": query, "expected": expected, "predicted": "No Match", "score": 0.0, "store": "-"})
                continue

            top_row = breakdown.sort_values(by="score", ascending=False).iloc[0]
            predicted = top_row["matched_product"]
            score = top_row["score"]
            store = top_row["store"]

            total_score += score
            if predicted == expected:
                correct += 1
            
            results.append({"query": query, "expected": expected, "predictied": predicted, "score": round(score, 3), "store": store})

        accuracy = correct / len(results)
        mean_score = total_score / len(results)

        summary = f"Accuracy: {accuracy:.2%}\nMean Score: {mean_score:.2f}\nMethod: {method.upper()} | Value Mode: {'On' if prefer_value else 'Off'}\n"
        all_summaries.append(summary)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        os.makedirs("reports", exist_ok=True)
        csv_path = f"reports/eval_results_{m}_{'value' if prefer_value else 'basic'}_{timestamp}.csv"
        pd.DataFrame(results).to_csv(csv_path, index=False)
        last_csv_path = csv_path

    return "\n\n".join(all_summaries), last_csv_path
