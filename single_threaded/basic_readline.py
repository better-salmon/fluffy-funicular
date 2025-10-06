"""
Single-threaded solution: Basic readline approach.

This is the simplest approach using Python's built-in file reading capabilities.
Reads the file line by line using a for loop.
"""


def read_lines_basic(filepath):
    """
    Read file line by line using basic iteration.

    Args:
        filepath: Path to the file to read

    Returns:
        Number of lines read
    """
    line_count = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line_count += 1
            # Process line here (currently just counting)
    return line_count


if __name__ == "__main__":
    import sys
    import time

    if len(sys.argv) != 2:
        print("Usage: python basic_readline.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    start_time = time.time()
    lines = read_lines_basic(filepath)
    elapsed = time.time() - start_time

    print(f"Lines read: {lines:,}")
    print(f"Time elapsed: {elapsed:.2f} seconds")
    print(f"Lines per second: {lines/elapsed:,.0f}")
