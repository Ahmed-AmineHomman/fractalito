import matplotlib.pyplot as plt

from fractalito import compute_image
from fractalito.operators import Mandelbrot as Core


if __name__ == "__main__":
    ensemble = 'mandelbrot'
    limits = {"x": (-2.5, 2.5), "y": (-2.0, 2.0)}
    resolution = {"x": 100, "y": 100}
    parameter = 1j
    boundary = 2
    operator = Core()

    print("computing fractal.")
    heatmap = compute_image(operator=operator,
                            limits=limits,
                            parameter=parameter,
                            resolution=resolution,
                            max_iterations=100,
                            boundary=boundary)

    print("drawing image.")
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.imshow(heatmap, vmin=0., vmax=1.0, cmap='gray', interpolation=None, extent=(*limits["x"], *limits["y"]))
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()
