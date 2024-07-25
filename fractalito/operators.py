from typing import Dict, List

import numpy as np


class Operator:

    def __call__(
            self,
            z: complex,
            c: complex,
    ) -> complex:
        raise NotImplementedError()


class Mandelbrot(Operator):
    def __call__(self, z, c):
        return (z * z) + c


class Flower(Operator):
    def __call__(self, z, c):
        return np.sinh(z) + 1.0 / (c * c)


class Alien(Operator):
    def __call__(self, z, c):
        return np.cos(z) + 1.0 / c


class Leaf(Operator):
    def __call__(self, z, c):
        return np.cos(z / c)


class Gamma(Operator):
    def __call__(self, z, c):
        return c ** (z - 1) * np.exp(-c)


class OperatorFactory:
    _operators: Dict[str, Operator] = {
        "mandelbrot": Mandelbrot,
        "flower": Flower,
        "alien": Alien,
        "leaf": Leaf,
        "gamma": Gamma
    }

    @staticmethod
    def create(operator: str) -> Operator:
        if operator not in OperatorFactory._operators:
            raise ValueError(f"Invalid operator: {operator}")
        return OperatorFactory._operators[operator]()

    @staticmethod
    def get_operators() -> List[str]:
        return list(OperatorFactory._operators.keys())
