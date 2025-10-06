"""
Single-threaded solution: Buffered reading with larger buffer.

Uses a larger buffer size to potentially improve I/O performance.
"""


def read_lines_buffered(filepath, buffer_size=1024 * 1024):
    """
    Read file with custom buffer size.

    Args:
        filepath: Path to the file to read
        buffer_size: Buffer size in bytes (default 1MB)

    Returns:
        Number of lines read
    """
    line_count = 0
    with open(filepath, "r", encoding="utf-8", buffering=buffer_size) as f:
        for line in f:
            line_count += 1
            # Process line here (currently just counting)
    return line_count


if __name__ == "__main__":
    import sys
    import time

    if len(sys.argv) != 2:
        print("Usage: python buffered_read.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    start_time = time.time()
    lines = read_lines_buffered(filepath)
    elapsed = time.time() - start_time

    print(f"Lines read: {lines:,}")
    print(f"Time elapsed: {elapsed:.2f} seconds")
    print(f"Lines per second: {lines/elapsed:,.0f}")
