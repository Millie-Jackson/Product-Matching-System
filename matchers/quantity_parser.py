# matchers/quantity_parser.py


"""
quantity_parser.py

Extracts and standardises product quantities (like 600g or 1.2kg) from text.
All values are returned in grams (g) for easy comparison.
"""


import re


def extract_weight(text: str) -> int | None:
    """
    Extracts weight from a product string and converts it to grams.
    Returns None if no weight is found.
    """

    # Match patterns like "600g", "1.2kg", "1000 g", etc.
    match = re.search(r"(\d+(?:\.\d+)?)\s*(g|kg)", text)
    if not match:
        return None
    
    value, unit = float(match.group(1)), match.group(2)
    if unit == "kg":
        value *= 1000

    return int(value) # Always return in grams
