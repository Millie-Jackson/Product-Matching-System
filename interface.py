# interface.py


"""
interface.py

Interactive tool for product matching with a clean layout, live threshold slider,
and working match table + CSV download. Keeps interface separate from evaluation reporting.
"""


import gradio as gr
import pandas as pd
import tempfile
from matchers.product_matcher import match_product


# Dummy product list
products = [
    "600g Boneless Chicken Breast",
    "Chicken Fillet 640g",
    "Whole Chicken 1.2kg",
    "Vegan Chicken Strips - 300g!",
    "Tofu, Block (400g)",
    "Pack of Cheese Slices (no weight)",
    "Chicken Thighs 600g",
]


def match_all(query, threshold):

    results = []

    for product in products:
        match, score = match_product(query, [product])
        results.append({
            "Candidate": product,
            "Match Score": round(score, 3),
            "Is Predicted Match": match == product
        })

    df = pd.DataFrame(results).sort_values(by="Match Score", ascending=False).reset_index(drop=True)
    df_filtered = df[df["Match Score"] >= threshold].copy()

    csv_bytes = df_filtered.to_csv(index=False).encode("utf-8")

    return df_filtered, ("matches.csv", csv_bytes)

with gr.Blocks() as demo:
    gr.Markdown("## Product Matcher with Results Table")
    gr.Markdown("Enter a product and view ranked matches across stores.")

    query_input = gr.Textbox(label="Product", placeholder="e.g. 600g Chicekn Breast")
    threshold_slider = gr.Slider(0.0, 1.0, value=2.0, step=0.05, label="Confindence Threshold")
    results_table = gr.Dataframe(label="Top Matches")
    csv_download = gr.File(label="Download CSV")

    run_button = gr.Button("Matches")

    run_button.click(fn=match_all, inputs=query_input, outputs=[results_table, csv_download])

if __name__ == "__main__":
    print("Launching Gradio...")
    demo.launch(share=False, inbrowser=True)