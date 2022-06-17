from .solvers import BasicSolver


def compute_image(operator, limits, parameter, resolution, **kwargs):
    return BasicSolver(operator, **kwargs).solve(limits=limits, parameter=parameter, resolution=resolution)
