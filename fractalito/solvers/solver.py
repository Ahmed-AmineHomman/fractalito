class Solver:
    def __init__(self, operator, max_iterations=100, boundary=2.0):
        self._operator = operator
        self._max_iterations = max_iterations
        self._boundary = boundary

    def solve_sequence(self, *args, **kwargs):
        raise NotImplementedError()

    def solve(self, *args, **kwargs):
        raise NotImplementedError()
