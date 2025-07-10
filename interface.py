"""
interface.py

Minimal CLI interface for product matching. Takes a user-input query and compares it
to a hardcoded list of supermarket products using TF-IDF similarity. Useful for quick testing
or demo purposes.
"""


if __name__ == "__main__":

    query = input("Enter a product: ")
    supermarket_products = ["Chicken Breast 620g", "Whole Chicken 1kg", "Turkey Mince 500g"]
    match, score = match_product(query, supermarket_products)

    print(f"Best match: {match} ({score: .2f})")