class Operator:
    def __init__(self):
        pass

    def __call__(self, z, c):
        if not isinstance(z, complex):
            raise TypeError(f"operator argument {z} must be of type {complex}")
        if not isinstance(c, complex):
            raise TypeError(f"operator argument {c} must be of type {complex}")
