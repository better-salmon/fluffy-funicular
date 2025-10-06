"""
Generate test data for benchmarking.

Creates a text file with the specified number of lines.
Each line contains a simple pattern to ensure realistic file size.
"""

import sys


def generate_test_file(filepath, num_lines, line_template=None):
    """
    Generate a test file with specified number of lines.

    Args:
        filepath: Path where the file should be created
        num_lines: Number of lines to generate
        line_template: Template for each line (default uses a pattern)
    """
    if line_template is None:
        line_template = "This is line number {}: Sample data for 1BRC challenge\n"

    print(f"Generating {num_lines:,} lines...")
    with open(filepath, "w", encoding="utf-8") as f:
        for i in range(num_lines):
            f.write(line_template.format(i))
            if (i + 1) % 1000000 == 0:
                print(f"  Written {i+1:,} lines...")

    print(f"File created: {filepath}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_data.py <filepath> <num_lines>")
        print("Example: python generate_data.py data.txt 1000000")
        sys.exit(1)

    filepath = sys.argv[1]
    num_lines = int(sys.argv[2])

    generate_test_file(filepath, num_lines)
