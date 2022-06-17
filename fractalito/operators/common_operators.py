import numpy as np

from .operator import Operator


class Mandelbrot(Operator):
    def __call__(self, z, c):
        super().__call__(z, c)
        return (z * z) + c


class GenericMandelbrot(Operator):
    def __init__(self, power=2):
        super().__init__()
        if not isinstance(power, (float, int)):
            raise TypeError(f"operator argument {power} must be of type {(int, float)}")
        self.power = power

    def __call__(self, z, c):
        super().__call__(z, c)
        return z ** self.power + c


class Flower(Operator):
    def __call__(self, z, c):
        super().__call__(z, c)
        return np.sinh(z) + 1.0 / (c * c)


class GenericFlower(Operator):
    def __init__(self, power=2):
        super().__init__()
        if not isinstance(power, (float, int)):
            raise TypeError(f"operator argument {power} must be of type {(int, float)}")
        if (power < 0.1) or (power > 10.0):
            raise ValueError(f"argument 'power' must be between 0.1 and 10 (received {power})")
        self.power = power

    def __call__(self, z, c):
        super().__call__(z, c)
        return np.sinh(z) + 1.0 / c ** self.power


class Alien(Operator):
    def __call__(self, z, c):
        super().__call__(z, c)
        return np.cos(z) + 1.0 / c


class GenericAlien(Operator):
    def __init__(self, power=1):
        super().__init__()
        if not isinstance(power, (float, int)):
            raise TypeError(f"operator argument {power} must be of type {(int, float)}")
        if (power < 0.1) or (power > 10.0):
            raise ValueError(f"argument 'power' must be between 0.1 and 10 (received {power})")
        self.power = power

    def __call__(self, z, c):
        super().__call__(z, c)
        return np.cos(z) + 1.0 / c ** self.power


class Leaf(Operator):
    def __call__(self, z, c):
        super().__call__(z, c)
        return np.cos(z / c)


class Gamma(Operator):
    def __call__(self, z, c):
        super().__call__(z, c)
        return c ** (z - 1) * np.exp(-c)
