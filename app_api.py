from fractalito.operators import OperatorFactory
from fractalito.solver import Solver


def compute_image(
        operator: str,
        xmin: float,
        xmax: float,
        ymin: float,
        ymax: float,
        xres: int,
        yres: int,
        boundary: float,
        dual: bool
):
    return (
        Solver(
            operator=OperatorFactory.create(operator=operator),
            boundary=boundary
        )
        .solve(
            limits={"x": (xmin, xmax), "y": (ymin, ymax)},
            parameter=1j,
            resolution={"x": xres, "y": yres},
            compute_dual=dual,
        )
    )
