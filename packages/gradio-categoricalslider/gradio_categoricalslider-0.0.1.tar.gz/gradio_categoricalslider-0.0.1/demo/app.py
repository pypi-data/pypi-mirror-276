
import gradio as gr
from gradio_categoricalslider import CategoricalSlider


demo = gr.Interface(
    lambda x: x,
    # interactive version of your component
    CategoricalSlider(categories=[("A", 1), ("B", 2), ("C", 3)]),
    None,  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


if __name__ == "__main__":
    demo.launch()
