# evaluate.py


"""
evaluate.py

Compares product matching predictions to a known dataset and calculates accuracy.
Also saves a markdown report with the results.
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
    else: 
        mismatches.append((query, expected, predicted, score))

accuracy = correct / len(df)
mean_score = total_score / len(df)

# Console output
print(f"Accuracy: {accuracy:.2%}")
print(f"Mean match score: {mean_score:.2f}")
print("\nMismatches:")
for q, exp, pred, s in mismatches:
    print(f"- Query: {q}\n  Expected: {exp}\n  Predicted: {pred} (score: {s:.2f})\n")


# Markdown report
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
report_lines = [
    f"# Product Matching Evaluation Report ({timestamp})\n",
    f"**Accuracy**: {accuracy:.2%}\n",
    f"**Mean Match Score**: {mean_score:.2f}\n",
    "\n## Mismatches:\n"
]

for q, exp, pred, s in mismatches:
    report_lines.append(f"- **Query**: '{q}'\n  - Expected: '{exp}'\n    - Predicted: '{pred}'\n    - Score: '{s:.2f}'\n")

# Save report
os.makedirs("reports", exist_ok=True)
report_path = f"reports/product_matching_report_{timestamp}.md"
with open (report_path, "w") as f:
    f.write("\n".join(report_lines))

print(f"\n Report saved to {report_path}")