"""
interface.py

Interactive tool for product matching with a clean layout, live threshold slider,
and working match table + CSV download. Supports shopping lists.
"""


import gradio as gr
import pandas as pd
import tempfile
from datetime import datetime
from matchers.product_matcher import match_product
from matchers.store_matcher import load_product_data, calculate_total_price, match_product_per_store
from matchers.evaluator import run_evaluation


# Load product data
product_df = load_product_data("data/supermarket_products.csv")


def match_shopping_list(shopping_list_text, threshold, method, prefer_value):

    # Split multiline input into individual items
    queries = [line.strip() for line in shopping_list_text.split("\n") if line.strip()]

    # Match and calculate totals
    totals, breakdown = calculate_total_price(queries, product_df, threshold, method, prefer_value)

    # If no results, return empty outputs to avoid crashing
    if totals.empty or breakdown.empty:
        empty_totals = pd.DataFrame(columns=["store", "total_price"])
        empty_breakdown = pd.DataFrame(columns=["query", "matched_product", "store", "price", "score"])
        return empty_totals, empty_breakdown, None, "No matches found. Try lowering the confidence threshold."
        
    # Mark cheapest store(s)    
    min_price = totals["total_price"].min()
    totals["is_cheapest"] = totals["total_price"] == min_price

    # Format winner message
    cheapest_stores = totals[totals["is_cheapest"]]["store"].tolist()
    winner_message = f"Cheapest store: {', '.join(cheapest_stores)}"

    # Save csv for download
    csv_data = pd.merge(breakdown, totals, on="store")
    tfilename = f"matched_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", prefix=tfilename[:-4] + "_", mode="w", encoding="utf-8")
    csv_data.to_csv(tmp_file.name, index=False)
    tmp_file.flush()

    return totals, breakdown, tmp_file.name, winner_message

def run_eval(method, prefer_value, run_both):

    result_text, csv_path = run_evaluation(method, prefer_value, run_both)

    return result_text, csv_path


with gr.Blocks() as demo:
    gr.Markdown("## Shopping List Price Comparison")
    gr.Markdown("Enter your shopping list below. Each line should contain one product item.")

    with gr.Row():
        shopping_input = gr.Textbox(label="Shopping List", lines=8, placeholder="e.g.\n600g Chicken Breast\nTofu Block 400g", scale=2)
        match_button = gr.Button("Compare", scale=1)

    message_output = gr.Textbox(label="Status Message", interactive=False)
    threshold_slider = gr.Slider(0.0, 1.0, value=0.2, step=0.05, label="Confindence Threshold")
    method_dropdown = gr.Dropdown(
        choices=["tfidf", "sbert"], 
        value="tfidf", 
        label="Matching Method",
        info="TF-IDF is fast and works best for exact keyword matches. SBERT is smarter and handles similar meanings (e.g. 'fillet' vs 'breast')."
    )

    prefer_value_checkbox = gr.Checkbox(
        label="Prefer Best Value (Price Per gram)",
        value=True
    )

    totals_output = gr.DataFrame(label="Total Price Per Store")
    breakdown_output = gr.DataFrame(label="Item-Level Breakdown",
                                    interactive=False,
                                    visible=True,
                                    datatype=["str", "str", "str", "number", "number", "number", "number"],
                                    headers=["Query", "Match", "Store", "Price", "Confidence", "Weight (g)", "Price per g"]
                                    )
    csv_download = gr.File(label="Download CSV")

    match_button.click(
        fn=match_shopping_list,
        inputs=[shopping_input, threshold_slider, method_dropdown, prefer_value_checkbox],
        outputs=[totals_output, breakdown_output, csv_download, message_output]
    )

    # Allow enter key to trigger button
    shopping_input.submit(
        fn=match_shopping_list,
        inputs=[shopping_input, threshold_slider, method_dropdown, prefer_value_checkbox],
        outputs=[totals_output, breakdown_output, csv_download, message_output]
    )

    gr.Markdown("---")
    gr.Markdown("## Evaluate Accuracy on Test Set")

    eval_method = gr.Dropdown(choices=["tfidf", "sbert"], value="tfidf", label="Evaluation Method")
    eval_value_toggle = gr.Checkbox(label="Prefer Best Value in Evalusation", value=True)
    run_both_toggle = gr.Checkbox(label="Compare TF-IDF vs SBERT", value=False)
    run_eval_button = gr.Button("Run Evaluation")
    eval_output = gr.Textbox(label="Results Summary", lines=10)
    eval_csv = gr.File(label="Download CSV Results")

    run_eval_button.click(
        fn=run_eval,
        inputs=[eval_method, eval_value_toggle, run_both_toggle],
        outputs=[eval_output, eval_csv]
    )


if __name__ == "__main__":
    print("Launching Gradio...")
    demo.launch(share=False, inbrowser=True)