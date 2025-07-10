"""
clean_text.py

Simple text cleaning function for product titles and descriptions.
Lowercases, removes punctuation/special characters, and normalises whitespace.
Useful as a preprocessing step for product matching pipelines.
"""


import re
import unicodedata
  

def clean_text(text):

    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    
    return text


example = "600g Boneless Chicken Breast - Pack of 2"
print(clean_text(example)) # -> '600g boneless chicken breast pack of 2