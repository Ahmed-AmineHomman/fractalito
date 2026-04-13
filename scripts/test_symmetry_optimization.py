#!/usr/bin/env python3
"""
Test script for symmetry optimization in fractal generation.

This script benchmarks the performance improvement gained by using
symmetry-based optimizations in the Solver class. It compares computation
times with and without symmetry enabled for various operators.

Usage:
    python scripts/test_symmetry_optimization.py
    
The script will:
1. Test each operator with symmetric grid limits
2. Compare computation times with symmetry enabled vs disabled
3. Verify that results are identical (within numerical precision)
4. Report speedup factors
"""

import time
import numpy as np
from fractalito.operators import (
    OperatorFactory, 
    SymmetryType, 
    Mandelbrot, 
    Flower, 
    Alien, 
    Leaf, 
    Gamma
)
from fractalito.solver import Solver


def test_operator_symmetry(
        operator_name: str,
        operator_class,
        limits: dict,
        resolution: dict,
        parameter: complex,
        n_runs: int = 3
):
    """Test an operator with and without symmetry optimization.
    
    Args:
        operator_name: Name of the operator for display.
        operator_class: The operator class to instantiate.
        limits: Grid limits dictionary.
        resolution: Grid resolution dictionary.
        parameter: Fixed parameter value.
        n_runs: Number of runs to average timing over.
        
    Returns:
        Tuple of (speedup_factor, results_match, symmetry_info)
    """
    operator = operator_class()
    
    # Get symmetry information
    symmetry_z = operator.symmetry_z
    symmetry_c = operator.symmetry_c
    
    # Create solvers
    solver_with_symmetry = Solver(operator, max_iterations=50, boundary=2.0, use_symmetry=True)
    solver_without_symmetry = Solver(operator, max_iterations=50, boundary=2.0, use_symmetry=False)
    
    # Time with symmetry
    start_time = time.perf_counter()
    for _ in range(n_runs):
        heatmap_with = solver_with_symmetry.solve(limits, resolution, parameter)
    time_with = (time.perf_counter() - start_time) / n_runs
    
    # Time without symmetry
    start_time = time.perf_counter()
    for _ in range(n_runs):
        heatmap_without = solver_without_symmetry.solve(limits, resolution, parameter)
    time_without = (time.perf_counter() - start_time) / n_runs
    
    # Check if results match
    results_match = np.allclose(heatmap_with, heatmap_without, rtol=1e-10, atol=1e-10)
    
    # Calculate speedup
    speedup = time_without / time_with if time_with > 0 else float('inf')
    
    symmetry_info = f"z={symmetry_z.value}, c={symmetry_c.value}"
    
    return speedup, results_match, symmetry_info, time_with, time_without


def main():
    """Run symmetry optimization tests for all operators."""
    print("=" * 70)
    print("Symmetry Optimization Benchmark")
    print("=" * 70)
    print()
    
    # Test configuration - symmetric limits for conjugate symmetry
    common_config = {
        "limits": {"x": (-2.0, 2.0), "y": (-2.0, 2.0)},
        "resolution": {"x": 100, "y": 100},
        "n_runs": 3
    }
    
    # Define test cases for each operator
    test_cases = [
        {
            "name": "Mandelbrot",
            "class": Mandelbrot,
            "parameter": complex(0, 0),  # c = 0 for standard Mandelbrot
            "limits": {"x": (-2.5, 1.5), "y": (-2.0, 2.0)},
            "description": "Standard Mandelbrot set (conjugate symmetry)"
        },
        {
            "name": "Flower",
            "class": Flower,
            "parameter": complex(0.5, 0),  # initial point
            "limits": {"x": (-2.0, 2.0), "y": (-2.0, 2.0)},
            "description": "Flower fractal (c_even symmetry)"
        },
        {
            "name": "Alien",
            "class": Alien,
            "parameter": complex(-0.5, 0.5),  # c value
            "limits": {"x": (-2.0, 2.0), "y": (-2.0, 2.0)},
            "description": "Alien fractal (z_even symmetry)"
        },
        {
            "name": "Leaf",
            "class": Leaf,
            "parameter": complex(0.3, 0.3),  # c value
            "limits": {"x": (-2.0, 2.0), "y": (-2.0, 2.0)},
            "description": "Leaf fractal (z_even symmetry)"
        },
        {
            "name": "Gamma",
            "class": Gamma,
            "parameter": complex(1.0, 0.5),  # c value
            "limits": {"x": (-2.0, 2.0), "y": (-2.0, 2.0)},
            "description": "Gamma fractal (no symmetry)"
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        name = test_case["name"]
        op_class = test_case["class"]
        parameter = test_case["parameter"]
        limits = test_case["limits"]
        description = test_case["description"]
        
        print(f"Testing: {name}")
        print(f"  Description: {description}")
        
        try:
            speedup, match, symmetry_info, t_with, t_without = test_operator_symmetry(
                name, op_class, limits, common_config["resolution"], parameter, common_config["n_runs"]
            )
            
            results.append({
                "name": name,
                "symmetry": symmetry_info,
                "speedup": speedup,
                "match": match,
                "time_with": t_with,
                "time_without": t_without
            })
            
            print(f"  Symmetry: {symmetry_info}")
            print(f"  Time without symmetry: {t_without:.4f}s")
            print(f"  Time with symmetry:    {t_with:.4f}s")
            print(f"  Speedup:               {speedup:.2f}x")
            print(f"  Results match:         {'✓' if match else '✗'}")
            
        except Exception as e:
            print(f"  Error: {e}")
            results.append({
                "name": name,
                "error": str(e)
            })
        
        print()
    
    # Summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"{'Operator':<15} {'Symmetry':<30} {'Speedup':<10} {'Match'}")
    print("-" * 70)
    
    for r in results:
        if "error" in r:
            print(f"{r['name']:<15} {'ERROR':<30} {'N/A':<10} {r['error']}")
        else:
            match_str = "✓" if r["match"] else "✗"
            print(f"{r['name']:<15} {r['symmetry']:<30} {r['speedup']:>6.2f}x     {match_str}")
    
    print()
    
    # Additional test: asymmetric limits (should not use symmetry)
    print("=" * 70)
    print("Test with Asymmetric Limits (symmetry should NOT be applied)")
    print("=" * 70)
    
    asymmetric_limits = {"x": (-2.0, 1.0), "y": (-1.0, 2.0)}  # Not symmetric around 0
    
    operator = Mandelbrot()
    solver_asymmetric = Solver(operator, max_iterations=100, boundary=2.0, use_symmetry=True)
    solver_full = Solver(operator, max_iterations=100, boundary=2.0, use_symmetry=False)
    
    heatmap_asym = solver_asymmetric.solve(asymmetric_limits, common_config["resolution"], complex(0, 0))
    heatmap_full = solver_full.solve(asymmetric_limits, common_config["resolution"], complex(0, 0))
    
    match_asymmetric = np.allclose(heatmap_asym, heatmap_full, rtol=1e-10, atol=1e-10)
    print(f"Asymmetric limits test: {'✓ Results match' if match_asymmetric else '✗ Results differ'}")
    print(f"  (Both should compute full grid since symmetry cannot be applied)")
    print()
    
    # Conclusion
    print("=" * 70)
    print("Conclusion")
    print("=" * 70)
    successful_tests = [r for r in results if "error" not in r and r["match"]]
    if len(successful_tests) > 0:
        avg_speedup = sum(r["speedup"] for r in successful_tests) / len(successful_tests)
        print(f"Average speedup for successful tests: {avg_speedup:.2f}x")
        print()
        print("Symmetry optimization is working correctly when:")
        print("  1. The operator declares symmetry properties")
        print("  2. The grid limits are symmetric around the appropriate axis")
        print("  3. Results are identical to full computation")
    else:
        print("No successful tests to report.")
    
    print()
    print("Note: For operators with conjugate symmetry (like Mandelbrot),")
    print("      ensure y-limits are symmetric (e.g., [-2, 2]) to benefit from")
    print("      ~2x speedup. For z_even symmetry, both x and y limits should")
    print("      be symmetric for up to ~4x speedup.")


if __name__ == "__main__":
    main()
