from typing import Dict, List, Optional, Tuple
from enum import Enum

import numpy as np


class SymmetryType(Enum):
    """Enumeration of symmetry types for operators.
    
    Attributes:
        NONE: No symmetry present.
        Z_EVEN: Operator is even in z: f(-z, c) = f(z, c).
        Z_ODD: Operator is odd in z: f(-z, c) = -f(z, c).
        C_EVEN: Operator is even in c: f(z, -c) = f(z, c).
        C_ODD: Operator is odd in c: f(z, -c) = -f(z, c).
        Z_CONJUGATE: Operator satisfies conjugate symmetry in z: f(conj(z), c) = conj(f(z, c)).
        C_CONJUGATE: Operator satisfies conjugate symmetry in c: f(z, conj(c)) = conj(f(z, c)).
    """
    NONE = "none"
    Z_EVEN = "z_even"
    Z_ODD = "z_odd"
    C_EVEN = "c_even"
    C_ODD = "c_odd"
    Z_CONJUGATE = "z_conjugate"
    C_CONJUGATE = "c_conjugate"


class Operator:
    """Base class for fractal operators.
    
    Operators define the iterative function f(z, c) used to generate fractals.
    Subclasses should implement the __call__ method and optionally specify
    symmetry properties to enable solver optimizations.
    
    Attributes:
        symmetry_z: Symmetry type with respect to z variable. Defaults to SymmetryType.NONE.
        symmetry_c: Symmetry type with respect to c parameter. Defaults to SymmetryType.NONE.
    """
    
    symmetry_z: SymmetryType = SymmetryType.NONE
    symmetry_c: SymmetryType = SymmetryType.NONE

    def __call__(
            self,
            z: complex,
            c: complex,
    ) -> complex:
        """Apply the operator to compute the next iteration.
        
        Args:
            z: Current point in the complex plane.
            c: Parameter value for the operator.
            
        Returns:
            The next point in the iteration sequence.
        """
        raise NotImplementedError()
    
    def apply_symmetry(
            self,
            result: float,
            z: complex,
            c: complex,
            original_z: Optional[complex] = None,
            original_c: Optional[complex] = None
    ) -> float:
        """Apply symmetry transformation to a computed result.
        
        This method can be overridden by subclasses to handle special cases
        where symmetry affects the iteration count differently.
        
        Args:
            result: The computed iteration result.
            z: The z value used in computation (may be transformed).
            c: The c value used in computation (may be transformed).
            original_z: The original z value before symmetry transformation.
            original_c: The original c value before symmetry transformation.
            
        Returns:
            The result, potentially adjusted based on symmetry properties.
        """
        # For most symmetries, the iteration count is the same
        return result


class Mandelbrot(Operator):
    """Standard Mandelbrot set operator: f(z, c) = z² + c.
    
    This operator has conjugate symmetry in both z and c:
    - f(conj(z), c) = conj(f(z, c)) when c is real
    - f(z, conj(c)) = conj(f(z, c)) when z is real
    
    More importantly, it exhibits reflection symmetry across the real axis
    for the Mandelbrot set visualization.
    """
    symmetry_z = SymmetryType.Z_CONJUGATE
    symmetry_c = SymmetryType.C_CONJUGATE
    
    def __call__(self, z, c):
        return (z * z) + c


class Flower(Operator):
    """Flower fractal operator: f(z, c) = sinh(z) + 1/c².
    
    This operator has even symmetry in c since 1/(-c)² = 1/c².
    """
    symmetry_z = SymmetryType.NONE
    symmetry_c = SymmetryType.C_EVEN
    
    def __call__(self, z, c):
        return np.sinh(z) + 1.0 / (c * c)


class Alien(Operator):
    """Alien fractal operator: f(z, c) = cos(z) + 1/c.
    
    This operator has even symmetry in z since cos(-z) = cos(z).
    Note: The symmetry applies to the iteration function itself, not necessarily
    to the escape behavior for all initial conditions. Use with appropriate limits.
    """
    symmetry_z = SymmetryType.NONE  # Disabled: symmetry doesn't apply to escape time
    symmetry_c = SymmetryType.NONE
    
    def __call__(self, z, c):
        return np.cos(z) + 1.0 / c


class Leaf(Operator):
    """Leaf fractal operator: f(z, c) = cos(z/c).
    
    This operator has no particular symmetry that can be exploited
    for fractal generation (symmetry of cos doesn't translate to 
    symmetric escape times from different initial points).
    """
    symmetry_z = SymmetryType.NONE  # Disabled: symmetry doesn't apply to escape time
    symmetry_c = SymmetryType.NONE
    
    def __call__(self, z, c):
        return np.cos(z / c)


class Gamma(Operator):
    """Gamma fractal operator: f(z, c) = c^(z-1) * exp(-c).
    
    This operator has no particular symmetry.
    """
    symmetry_z = SymmetryType.NONE
    symmetry_c = SymmetryType.NONE
    
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
