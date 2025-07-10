"""
interface.py

Minimal CLI interface for product matching. Takes a user-input query and compares it
to a hardcoded list of supermarket products using TF-IDF similarity. Useful for quick testing
or demo purposes.
"""


from matchers.clean_text import clean_text


examples = [
    "600g Boneless Chicken Breast",
    "Vegan Chicken Strips - 300g!",
    "Tofu, Block (400g)",
]

for product in examples:
    print(f"Original: {product}")
    print(f"Cleaned: {clean_text(product)}\n")
