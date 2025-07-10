# matchers/clean_text.py


"""
clean_text.py

Provides a text cleaning function to prepare product names and descriptions
for comparison across different stores.
"""


import re
import unicodedata
  

def clean_text(text: str) -> str:

    # Lowercase everything
    text = text.lower()

    # Normalize weird characters
    text = unicodedata.normalize("NFKD", text)

    # Remove anything that's not a letter, number, or space
    text = re.sub(r"[^a-z0-9\s]", "", text)

    # Replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text).strip()
    
    return text


example = "600g Boneless Chicken Breast - Pack of 2"
print(clean_text(example)) # -> '600g boneless chicken breast pack of 2