# interface.py


import gradio as gr
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


def match_interface(query):
    
    best_match, score = match_product(query, products)

    return f"Best match: {best_match}\n Score: {score: .2f}"

demo = gr.Interface(
    fn=match_interface,
    inputs=gr.Textbox(lines=1, placeholder="e.g. 600g Chicken Breast"),
    outputs="text",
    title="Product Matcher",
    description="Enter a shopping list item and find the most similar product from a dummy supermarket dataset.",
    examples=[
        ["600g Chicken Breast"],
        ["Tofu 400g"],
        ["1kg Whole Chicken"],
        ["Cheddar Cheese Slices"],
    ]
)


if __name__ == "__main__":
    print("Launching Gradio...")
    demo.launch(share=False, inbrowser=True)