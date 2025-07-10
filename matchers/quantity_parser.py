# Parse & Normalise Quantities


import re


def extract_weight(text):

    match = re.search(r"(\d+)(g|kg)", text.lower())
    if not match:
        return None
    
    value, unit = int(match[1]), match[2]
    if unit == "kg":
        value *= 1000

    return value # Always return in grams


print(extract_weight("600g Boneless chicken Breast")) # -> 600
print(extract_weight("1.2kg Whole Chicken"))          # -> 1200