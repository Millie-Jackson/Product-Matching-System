"""
matchers/quantity_parser.py

Extracts and standardises product quantities (like 600g or 1.2kg) from text.
All values are returned in grams (g) for easy comparison.
"""


import re


def extract_weight(text: str) -> int | None:
    """
    Extract weight from a product string and convert it to grams.
    
    Examples:
    - "600g" → 600
    - "1.2kg" → 1200
    - "1000 g" → 1000

    Returns:
        int: weight in grams, or None if no weight is found
    """

    # Match patterns like "600g", "1.2kg", "1000 g", etc.
    match = re.search(r"(\d+(?:\.\d+)?)\s*(g|kg)", text, flags=re.IGNORECASE)
    if not match:
        return None
    
    value = float(match.group(1))
    unit = match.group(2).lower()
    
    if unit == "kg":
        value *= 1000

    return int(value) # Always return in grams
