import argparse
import os
from argparse import Namespace
from tomllib import load

import gradio as gr

from app_api import compute_image
from fractalito.operators import OperatorFactory

UI: dict


def load_parameters() -> Namespace:
    parser = argparse.ArgumentParser(description="fractalito's argument parser")
    parser.add_argument(
        "--language",
        type=str,
        default="en",
        required=False,
        help="language of the interface"
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="share the web app publicly on gradio"
    )
    parser.add_argument(
        "--listen",
        action="store_true",
        help="if set, the server will start listening for external clients (allows to remotely access the web app)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="the port number on which the server will listen for external clients"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="if set, the server will run in debug mode"
    )
    return parser.parse_args()


def build_ui() -> gr.Blocks:
    """Builds the UI"""
    with gr.Blocks() as app:
        gr.Markdown(f"# {UI.get('title')}\n\n{UI.get('description')}")
        gr.Markdown(f"## {UI.get('parameters_title')}\n\n{UI.get('parameters_description')}")
        with gr.Row(equal_height=True):
            gr.Markdown(f"{UI.get('parameters_axis_description')}")
            gr.Markdown(f"{UI.get('parameters_resolution_description')}")
            gr.Markdown(f"{UI.get('parameters_boundary_description')}")
            gr.Markdown(f"{UI.get('parameters_operator_description')}")
        with gr.Row(equal_height=True):
            with gr.Column(variant="default"):
                with gr.Row():
                    xmin = gr.Number(label=UI.get('parameters_xmin_label'), value=-2.0, precision=1)
                    xmax = gr.Number(label=UI.get('parameters_xmax_label'), value=2.0, precision=1)
                with gr.Row():
                    ymin = gr.Number(label=UI.get('parameters_ymin_label'), value=-2.0, precision=1)
                    ymax = gr.Number(label=UI.get('parameters_ymax_label'), value=2.0, precision=1)
            with gr.Column(variant="default"):
                xres = gr.Number(label=UI.get('parameters_xres_label'), value=100, precision=0)
                yres = gr.Number(label=UI.get('parameters_yres_label'), value=100, precision=0)
            with gr.Column(variant="default"):
                boundary = gr.Number(label=UI.get('parameters_boundary_label'), value=2.0, precision=1)
                dual = gr.Checkbox(
                    label=UI.get('parameters_dual_label'),
                    info=UI.get("parameters_dual_description"),
                    value=False
                )
            with gr.Column(variant="default"):
                operator = gr.Dropdown(
                    label=UI.get('parameters_operator_label'),
                    choices=OperatorFactory.get_operators(),
                    value=OperatorFactory.get_operators()[0]
                )
            button = gr.Button(
                value=UI.get('compute_button_label'),
                variant="primary"
            )
        image = gr.Image(
            label=UI.get('image_label'),
            format="png",
            type="numpy",
            width=1024,
            height=1024
        )

        # UI logic
        button.click(
            fn=compute_image,
            inputs=[operator, xmin, xmax, ymax, ymin, xres, yres, boundary, dual],
            # we invert ymin & ymax due to image representation
            outputs=[image]
        )

    return app


if __name__ == "__main__":
    # parse parameters
    parameters = load_parameters()

    # load UI doc
    filepath = os.path.join(os.path.dirname(__file__), "fractalito", "data", "locales", f"{parameters.language}.toml")
    with open(filepath, "rb") as fh:
        UI = load(fh)

    # build UI
    app = build_ui()

    # run the app
    app.launch(
        share=parameters.share,
        server_name="0.0.0.0" if parameters.listen else None,
        server_port=parameters.port,
        debug=parameters.debug,
    )
