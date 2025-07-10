"""
interface.py

Minimal CLI interface for product matching. Takes a user-input query and compares it
to a hardcoded list of supermarket products using TF-IDF similarity. Useful for quick testing
or demo purposes.
"""


from matchers.clean_text import clean_text
from matchers.tfidf_matcher import match_product


query = "600g Chicken Breast"
products = [
    "600g Boneless Chicken Breast",
    "Chicken Fillet 640g",
    "Whole Chicken 1.2kg",
    "Vegan Chicken Strips - 300g!",
    "Tofu, Block (400g)",
]

'''for product in products:
    print(f"Original: {product}")
    print(f"Cleaned: {clean_text(product)}\n")'''

best_match, score = match_product(query, products)

print(f"Query: {query}")
print(f"Best Match: {best_match}")
print(f"Similarity Score: {score:.2f}")
