"""
test_store_matcher.py

Quick test to check store-wise product matching and total price calculation.
"""


from matchers.store_matcher import load_product_data, calculate_total_price


# Sample shopping list (simulates user input)
shopping_list = [
    "600g Chicken Breast",
    "Tofu Block 400g",
    "Cheese Slices"
]


# Load the supermarket dataset
df = load_product_data("data/supermarket_products.csv")

# Run the price calculator
totals, combined = calculate_total_price(shopping_list, df, threshold=0.2)

print("Total Cost Per Store:\n")
print(totals)

print("\nMatched Products Per Store:\n")
print(combined)