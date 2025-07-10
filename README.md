# 🛒 Product Matching System: Smarter Shopping List Comparisons

## 💡 Project Summary

This project demonstrates a smart matching system that compares products across different supermarkets — even when names, sizes, and packaging vary. It solves a real-world freelance use case: helping users build shopping lists and find the best total price across stores.

When a user adds an item like “600g chicken breast,” the system finds the closest equivalent product in each supermarket, handling own-brand variations and size mismatches.

---

## 🚀 Features

- ✅ Clean and normalise product names
- ✅ Extract and compare product quantities (e.g., “1.2kg” vs. “600g”)
- ✅ Calculate similarity using TF-IDF vectorisation
- ✅ Match user queries to the most similar item in a candidate list
- ✅ Lightweight CLI tool for testing and demonstration

---

## 📁 File Descriptions

| File | Description |
|------|-------------|
| `01_clean_text.py` | Tidies up product names by removing symbols, lowercasing, and standardising formatting |
| `02_product_embedding.py` | Turns product descriptions into vectors using TF-IDF and compares them by similarity |
| `03_quantity_parser.py` | Extracts and normalises product size (e.g., always outputs weight in grams) |
| `04_match_products.py` | Finds the best matching product based on name and size similarity |
| `05_optional_interface.py` | Basic interactive command-line interface for manual testing |

---

## 📊 Sample Output

**Query:** `600g Boneless Chicken Breast`  
**Candidate List:**
- Chicken Breast 640g  
- Whole Chicken 1.2kg  
- Tofu 400g

**Output:** Best match: Chicken Breast 640g (0.84 similarity)

---

## 🔧 Tech Stack

- Python 3
- `scikit-learn` for text vectorisation and similarity
- `re` for pattern matching
- Optional: `streamlit` or `gradio` for interactive demo (future upgrade)

---

## 🧠 Learning Highlights

- Applied natural language processing (NLP) to real-world product matching
- Built a reusable product comparison pipeline
- Balanced structured data (e.g. size) and unstructured data (e.g. names) in matching logic

---

## 🧩 Possible Extensions

- 🔍 Add sentence embeddings (e.g. `sentence-transformers`) for smarter matching
- 🧪 Add accuracy metrics and test datasets
- 🛍️ Build a mini web app for interactive shopping list comparison
- 🌍 Integrate with real supermarket APIs or datasets

---

## 🗂️ Folder Structure


