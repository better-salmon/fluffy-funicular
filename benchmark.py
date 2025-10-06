"""
Benchmark all solutions and compare performance.

Runs all single-threaded and multi-threaded solutions on the same file
and reports performance metrics.
"""

import importlib.util
import os
import sys
import time
from pathlib import Path


def load_module_from_file(filepath):
    """Dynamically load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location("module", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def benchmark_solution(solution_path, data_file, solution_type="single"):
    """
    Benchmark a single solution.

    Args:
        solution_path: Path to the solution file
        data_file: Path to the data file to process
        solution_type: 'single' or 'multi'

    Returns:
        Dictionary with benchmark results
    """
    # For multiprocessing solutions, run as subprocess to avoid pickling issues
    if "multiprocess" in solution_path.name:
        import subprocess

        start_time = time.time()
        try:
            result = subprocess.run(
                [sys.executable, str(solution_path), data_file, "4"],
                capture_output=True,
                text=True,
                timeout=300,
            )
            elapsed = time.time() - start_time

            if result.returncode == 0:
                # Parse output to get line count
                for line in result.stdout.split("\n"):
                    if "Lines read:" in line:
                        line_count = int(line.split(":")[1].strip().replace(",", ""))
                        return {
                            "success": True,
                            "lines": line_count,
                            "time": elapsed,
                            "lines_per_sec": line_count / elapsed if elapsed > 0 else 0,
                        }
                return {"success": False, "error": "Could not parse output"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # For other solutions, use direct module loading
    module = load_module_from_file(solution_path)

    # Find the main function (varies by solution)
    if hasattr(module, "read_lines_basic"):
        func = module.read_lines_basic
        args = (data_file,)
    elif hasattr(module, "read_lines_buffered"):
        func = module.read_lines_buffered
        args = (data_file,)
    elif hasattr(module, "read_lines_chunked"):
        func = module.read_lines_chunked
        args = (data_file,)
    elif hasattr(module, "read_lines_threaded"):
        func = module.read_lines_threaded
        args = (data_file, 4)  # Default to 4 threads
    else:
        return {"error": "No suitable function found"}

    start_time = time.time()
    try:
        line_count = func(*args)
        elapsed = time.time() - start_time
        return {
            "success": True,
            "lines": line_count,
            "time": elapsed,
            "lines_per_sec": line_count / elapsed if elapsed > 0 else 0,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_benchmarks(data_file):
    """
    Run all benchmarks and display results.

    Args:
        data_file: Path to the data file to process
    """
    base_path = Path(__file__).parent

    results = {"single_threaded": [], "multi_threaded": []}

    # Single-threaded solutions
    single_dir = base_path / "single_threaded"
    if single_dir.exists():
        print("\n=== Single-Threaded Solutions ===\n")
        for solution_file in sorted(single_dir.glob("*.py")):
            print(f"Running {solution_file.name}...")
            result = benchmark_solution(solution_file, data_file, "single")
            if result.get("success"):
                results["single_threaded"].append(
                    {"name": solution_file.name, **result}
                )
                print(
                    f"  Lines: {result['lines']:,}, "
                    f"Time: {result['time']:.2f}s, "
                    f"Speed: {result['lines_per_sec']:,.0f} lines/sec"
                )
            else:
                print(f"  Error: {result.get('error', 'Unknown error')}")
            print()

    # Multi-threaded solutions
    multi_dir = base_path / "multi_threaded"
    if multi_dir.exists():
        print("\n=== Multi-Threaded Solutions ===\n")
        for solution_file in sorted(multi_dir.glob("*.py")):
            print(f"Running {solution_file.name}...")
            result = benchmark_solution(solution_file, data_file, "multi")
            if result.get("success"):
                results["multi_threaded"].append({"name": solution_file.name, **result})
                print(
                    f"  Lines: {result['lines']:,}, "
                    f"Time: {result['time']:.2f}s, "
                    f"Speed: {result['lines_per_sec']:,.0f} lines/sec"
                )
            else:
                print(f"  Error: {result.get('error', 'Unknown error')}")
            print()

    # Summary
    print("\n=== Summary ===\n")
    all_results = results["single_threaded"] + results["multi_threaded"]
    if all_results:
        sorted_results = sorted(
            all_results, key=lambda x: x["lines_per_sec"], reverse=True
        )
        print("Ranking by speed:")
        for i, result in enumerate(sorted_results, 1):
            print(
                f"{i}. {result['name']}: {result['lines_per_sec']:,.0f} lines/sec "
                f"({result['time']:.2f}s)"
            )
    else:
        print("No successful benchmark results.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python benchmark.py <data_file>")
        print("Example: python benchmark.py data.txt")
        sys.exit(1)

    data_file = sys.argv[1]
    if not os.path.exists(data_file):
        print(f"Error: File '{data_file}' not found.")
        sys.exit(1)

    run_benchmarks(data_file)
