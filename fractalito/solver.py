import numpy as np

from .operators import Operator


class Solver:
    def __init__(
            self,
            operator: Operator,
            max_iterations: int = 100,
            boundary: float = 2.0
    ):
        self._operator = operator
        self._max_iterations = max_iterations
        self._boundary = boundary

    def solve(
            self,
            limits,
            resolution,
            parameter,
            compute_dual: bool = False
    ):
        X, Y = np.meshgrid(
            np.linspace(*limits["x"], resolution["x"]),
            np.linspace(*limits["y"], resolution["y"])
        )

        if compute_dual:
            def parameter_map(i, j):
                return {"initial_point": parameter,
                        "parameter": complex(X[i, j], Y[i, j])}
        else:
            def parameter_map(i, j):
                return {"initial_point": complex(X[i, j], Y[i, j]),
                        "parameter": parameter}

        # compute grid
        heatmap = np.ones_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                heatmap[i, j] = self.solve_sequence(**parameter_map(i, j))

        return heatmap

    def solve_sequence(self, initial_point, parameter):
        # compute sequence and determine boundedness
        is_bounded = True
        iteration = 0
        current_point = initial_point
        while is_bounded and (iteration < self._max_iterations):
            current_point = self._operator(current_point, parameter)
            is_bounded = (np.linalg.norm(current_point) < self._boundary)
            iteration += 1

        return iteration / self._max_iterations
