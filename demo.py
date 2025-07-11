"""
interface.py

Minimal CLI interface for product matching. Takes a user-input query and compares it
to a hardcoded list of supermarket products using TF-IDF similarity. Useful for quick testing
or demo purposes.
"""


from matchers.clean_text import clean_text
from matchers.tfidf_matcher import match_product
from matchers.quantity_parser import extract_weight
from matchers.product_matcher import match_product as full_match


query = "600g Chicken Breast"

products = [
    "600g Boneless Chicken Breast",
    "Chicken Fillet 640g",
    "Whole Chicken 1.2kg",
    "Vegan Chicken Strips - 300g!",
    "Tofu, Block (400g)",
    "Pack of Cheese Slices (no weight)",
    "Chicken Thighs 600g",
]

for product in products:

    cleaned = clean_text(product)
    weight = extract_weight(cleaned)
    weight_str = f"{weight}g" if weight is not None else "No weight found"

    print(f"Original:      {product}")
    print(f"Cleaned:       {cleaned}")
    print(f"Parsed weight: {weight_str}\n")

best, score = full_match(query, products)

print(f"\nQuery:        {query}")
print(f"Best match:   {best}")
print(f"Match score:  {score}")
