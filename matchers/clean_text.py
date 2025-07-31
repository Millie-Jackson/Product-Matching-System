"""
matchers/clean_text.py

Provides a text cleaning function to prepare product names and descriptions
for comparison across different stores.
"""


import re
import unicodedata
  

def clean_text(text: str) -> str:
    """
    Lowercase, normalize, and clean a product string for comparison.
    Removes non-alphanumeric characters and extra spaces.
    """

    # Lowercase everything
    text = text.lower()

    # Normalize weird characters
    text = unicodedata.normalize("NFKD", text)

    # Remove anything that's not a letter, number, or space
    text = re.sub(r"[^a-z0-9\s]", "", text)

    # Replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text).strip()
    
    return text
