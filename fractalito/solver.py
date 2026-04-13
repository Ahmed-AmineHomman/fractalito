import numpy as np
import time

from .operators import Operator, SymmetryType


class Solver:
    """Solver class for computing fractal heatmaps.
    
    The Solver uses an Operator to iteratively compute fractal patterns.
    It supports symmetry-based optimizations to reduce computation time
    when the operator exhibits symmetry properties.
    
    Attributes:
        _operator: The operator defining the fractal iteration function.
        _max_iterations: Maximum number of iterations before considering a point bounded.
        _boundary: The escape radius - points beyond this are considered unbounded.
        _use_symmetry: Whether to enable symmetry-based optimizations.
    """
    def __init__(
            self,
            operator: Operator,
            max_iterations: int = 100,
            boundary: float = 2.0,
            use_symmetry: bool = True
    ):
        """Initialize the solver with an operator and parameters.
        
        Args:
            operator: The operator defining the fractal iteration.
            max_iterations: Maximum iterations per point (default: 100).
            boundary: Escape radius threshold (default: 2.0).
            use_symmetry: Enable symmetry optimizations if operator supports them (default: True).
        """
        self._operator = operator
        self._max_iterations = max_iterations
        self._boundary = boundary
        self._use_symmetry = use_symmetry
        
        # Detect available symmetries for optimization
        self._symmetry_z = operator.symmetry_z if use_symmetry else SymmetryType.NONE
        self._symmetry_c = operator.symmetry_c if use_symmetry else SymmetryType.NONE

    def solve(
            self,
            limits,
            resolution,
            parameter,
            compute_dual: bool = False
    ):
        """Compute the fractal heatmap over a grid.
        
        This method computes the fractal pattern by iterating the operator
        over a grid of complex points. If the operator has symmetry properties
        and symmetry optimization is enabled, only a portion of the grid is
        computed directly, with the rest filled using symmetry transformations.
        
        Args:
            limits: Dictionary with "x" and "y" keys, each containing a tuple
                    of (min, max) values for the complex plane bounds.
            resolution: Dictionary with "x" and "y" keys specifying the number
                       of points in each dimension.
            parameter: The fixed parameter value (c for Mandelbrot-like, or 
                      initial_point for Julia-like sets).
            compute_dual: If True, swap the roles of parameter and initial_point,
                         computing the parameter space instead of the dynamical space.
        
        Returns:
            A 2D numpy array containing normalized iteration counts (0-1 range).
        """
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

        # Initialize heatmap
        heatmap = np.ones_like(X)
        
        # Check if we can use symmetry optimization
        can_use_symmetry = self._can_use_symmetry(limits, compute_dual)
        
        if can_use_symmetry:
            heatmap = self._solve_with_symmetry(X, Y, parameter_map, compute_dual)
        else:
            # Standard computation without symmetry optimization
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    heatmap[i, j] = self.solve_sequence(**parameter_map(i, j))

        return heatmap
    
    def _can_use_symmetry(self, limits, compute_dual: bool) -> bool:
        """Check if symmetry optimization can be applied.
        
        Symmetry optimization requires:
        1. Symmetry is enabled and the operator has a symmetry property
        2. The grid is symmetric around the axis of symmetry
        
        Args:
            limits: The grid limits dictionary.
            compute_dual: Whether computing in dual mode.
            
        Returns:
            True if symmetry optimization can be used, False otherwise.
        """
        if not self._use_symmetry:
            return False
            
        # Check for conjugate symmetry (reflection across real axis)
        # This requires y-limits to be symmetric around 0
        if self._symmetry_z == SymmetryType.Z_CONJUGATE or self._symmetry_c == SymmetryType.C_CONJUGATE:
            y_limits = limits["y"]
            if abs(y_limits[0] + y_limits[1]) < 1e-10:  # y_min ≈ -y_max
                return True
        
        # Check for even/odd symmetry in z (reflection across origin)
        if self._symmetry_z in [SymmetryType.Z_EVEN, SymmetryType.Z_ODD]:
            x_limits = limits["x"]
            y_limits = limits["y"]
            if abs(x_limits[0] + x_limits[1]) < 1e-10 and abs(y_limits[0] + y_limits[1]) < 1e-10:
                return True
                
        return False
    
    def _solve_with_symmetry(self, X, Y, parameter_map, compute_dual: bool):
        """Solve using symmetry optimization.
        
        This method computes only half (or quarter) of the grid and uses
        symmetry properties to fill in the rest, reducing computation time.
        
        Args:
            X: Meshgrid X coordinates.
            Y: Meshgrid Y coordinates.
            parameter_map: Function mapping grid indices to operator parameters.
            compute_dual: Whether computing in dual mode.
            
        Returns:
            The completed heatmap array.
        """
        heatmap = np.ones_like(X)
        nx, ny = X.shape[0], X.shape[1]
        
        # For conjugate symmetry (reflection across real axis), 
        # compute upper half (y >= 0) and mirror to lower half
        # The Mandelbrot set is symmetric about the real axis: M(x,y) = M(x,-y)
        # In meshgrid with symmetric limits, row i has Y[i,:] and row (nx-1-i) has -Y[i,:]
        if self._symmetry_z == SymmetryType.Z_CONJUGATE or self._symmetry_c == SymmetryType.C_CONJUGATE:
            # Compute upper half where Y >= 0 (rows nx//2 and above)
            for i in range(nx // 2, nx):
                for j in range(ny):
                    heatmap[i, j] = self.solve_sequence(**parameter_map(i, j))
            
            # Mirror from upper half to lower half using index symmetry
            # Row i maps to row (nx-1-i) since Y[nx-1-i, :] = -Y[i, :]
            for i in range(nx // 2):
                mirrored_i = nx - 1 - i
                for j in range(ny):
                    heatmap[i, j] = heatmap[mirrored_i, j]
                    
        # For even symmetry in z, compute one quadrant and mirror
        elif self._symmetry_z == SymmetryType.Z_EVEN:
            mid_x = nx // 2
            mid_y = ny // 2
            
            # Compute first quadrant (x >= 0, y >= 0)
            for i in range(mid_x + (nx % 2)):
                for j in range(mid_y + (ny % 2)):
                    heatmap[i, j] = self.solve_sequence(**parameter_map(i, j))
            
            # Mirror across y-axis (left-right symmetry)
            for i in range(mid_x + (nx % 2)):
                for j in range(ny // 2):
                    mirrored_j = ny - 1 - j
                    heatmap[i, mirrored_j] = heatmap[i, j]
            
            # Mirror across x-axis (top-bottom symmetry)
            for i in range(nx // 2):
                mirrored_i = nx - 1 - i
                for j in range(ny):
                    heatmap[mirrored_i, j] = heatmap[i, j]
        
        return heatmap

    def solve_sequence(self, initial_point, parameter):
        """Compute the iteration sequence for a single point.
        
        Iterates the operator starting from initial_point with the given
        parameter until either:
        - The point escapes beyond the boundary
        - Maximum iterations is reached
        
        Args:
            initial_point: Starting point in the complex plane.
            parameter: The parameter value for the operator.
            
        Returns:
            Normalized iteration count (iteration / max_iterations),
            where 1.0 means the point remained bounded for all iterations.
        """
        # compute sequence and determine boundedness
        is_bounded = True
        iteration = 0
        current_point = initial_point
        while is_bounded and (iteration < self._max_iterations):
            current_point = self._operator(current_point, parameter)
            is_bounded = (np.linalg.norm(current_point) < self._boundary)
            iteration += 1

        return iteration / self._max_iterations
