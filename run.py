import matplotlib.pyplot as plt

import argparse
import sys

from fractalito import compute_image
from fractalito.operators import Mandelbrot as Core


def get_parameters(parameters):
    parser = argparse.ArgumentParser(description="fractalito's argument parser")
    parser.add_argument(
        "--xmin",
        nargs=1,
        type=float,
        default=-2.0,
        help="the minimal considered value in the x-axis when computing the fractal"
    )
    parser.add_argument(
        "--xmax",
        nargs=1,
        type=float,
        default=2.0,
        help="the maximal considered value in the x-axis when computing the fractal"
    )
    parser.add_argument(
        "--ymin",
        nargs=1,
        type=float,
        default=-2.0,
        help="the minimal considered value in the y-axis when computing the fractal"
    )
    parser.add_argument(
        "--ymax",
        nargs=1,
        type=float,
        default=2.0,
        help="the maximal considered value in the y-axis when computing the fractal"
    )
    parser.add_argument(
        "--xres",
        nargs=1,
        type=int,
        default=100,
        help="x-resolution (in pixels) of the fractal image"
    )
    parser.add_argument(
        "--yres",
        nargs=1,
        type=int,
        default=100,
        help="y-resolution (in pixels) of the fractal image"
    )
    parser.add_argument(
        "--parameter",
        nargs=1,
        type=str,
        default=1j,
        help="parameter value of the fractal's associated equation"
    )
    parser.add_argument(
        "--boundary",
        nargs=1,
        type=float,
        default=2.0,
        help="divergence threshold, i.e. the value corresponding to the maximal absolute value a sequence can have"
             "before being considered as divergent."
    )
    return parser.parse_args(parameters)


if __name__ == "__main__":
    # parse parameters
    parameters = get_parameters(parameters=sys.argv[1:])
    print("PARAMETERS:")
    for key, value in vars(parameters).items():
        print(f"  - {key:12s}: {value}")

    print("computing fractal.")
    heatmap = compute_image(operator=Core(),
                            limits={"x": (parameters.xmin, parameters.xmax),
                                    "y": (parameters.ymin, parameters.ymax)},
                            parameter=complex(parameters.parameter),
                            resolution={"x": parameters.xres, "y": parameters.yres},
                            max_iterations=100,
                            boundary=parameters.boundary)

    print("drawing image.")
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.imshow(
        heatmap,
        vmin=0.,
        vmax=1.0,
        cmap='gray',
        interpolation=None,
        extent=(parameters.xmin, parameters.xmax, parameters.ymin, parameters.ymax)
    )
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()
