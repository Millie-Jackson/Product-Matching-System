# evaluate.py


"""
Compares product matching predictions to a known dataset and calculates accuracy.
Also saves a markdown report with a clean visual table of all predictions.
"""


import os
import pandas as pd
from datetime import datetime
from matchers.product_matcher import match_product


# Load test set
df = pd.read_csv("data/testset.csv")

# Candidate product list
products = [
    "600g Boneless Chicken Breast",
    "Chicken Fillet 640g",
    "Whole Chicken 1.2kg",
    "Vegan Chicken Strips - 300g!",
    "Tofu, Block (400g)",
    "Pack of Cheese Slices (no weight)",
    "Chicken Thighs 600g",
]

# Evaluation
results = []
correct = 0
total_score = 0
mismatches = []

for _, row in df.iterrows():

    query = row["query"]
    expected = row["expected_match"]
    predicted, score = match_product(query, products)
    
    total_score += score
    if predicted == expected:
        correct += 1

    results.append({
        "Query": query,
        "Expected": expected,
        "Predicted": predicted,
        "Score": round(score, 2)
    })

accuracy = correct / len(results)
mean_score = total_score / len(results)

# Console output
print(f"Accuracy: {accuracy:.2%}")
print(f"Mean match score: {mean_score:.2f}")
print("\nPredictions:")
for r in results:
    print(f"- {r['Query']}\n -> Expected: {r['Expected']}\n -> Predicted: {r['Predicted']} (Score: {r['Score']})\n")

# Markdown report
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
os.makedirs("reports", exist_ok=True)
md_path = f"reports/product_matching_report_{timestamp}.md"

with open(md_path, "w") as f:
    f.write(f"# Product Matching Evaluation Report ({timestamp})\n\n")
    f.write(f"**Accuracy**: {accuracy:.2%}\n\n")
    f.write(f"**Mean Match Score**: {mean_score:.2f}\n\n")
    f.write("## Predictions Table\n\n")
    f.write("| Query | Expected | Predicted | Score |\n")
    f.write("|-------|----------|-----------|--------|\n")
   
    for r in results:
        f.write(f"| {r['Query']} | {r['Expected']} | {r['Predicted']} | {r['Score']} |\n")

print(f"\n Report saved to {md_path}")

# CSV for later analysis
csv_path = f"reports/product_matching_predictions_{timestamp}.csv"
pd.DataFrame(results).to_csv(csv_path, index=False)
print(f"\n CSV saved to {csv_path}")