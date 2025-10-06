"""
Single-threaded solution: Using readlines with chunking.

Reads file in chunks using readlines with a size hint.
"""


def read_lines_chunked(filepath, chunk_size=1024 * 1024 * 10):
    """
    Read file in chunks using readlines.

    Args:
        filepath: Path to the file to read
        chunk_size: Size hint for readlines in bytes (default 10MB)

    Returns:
        Number of lines read
    """
    line_count = 0
    with open(filepath, "r", encoding="utf-8") as f:
        while True:
            lines = f.readlines(chunk_size)
            if not lines:
                break
            line_count += len(lines)
            # Process lines here (currently just counting)
    return line_count


if __name__ == "__main__":
    import sys
    import time

    if len(sys.argv) != 2:
        print("Usage: python chunked_readlines.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    start_time = time.time()
    lines = read_lines_chunked(filepath)
    elapsed = time.time() - start_time

    print(f"Lines read: {lines:,}")
    print(f"Time elapsed: {elapsed:.2f} seconds")
    print(f"Lines per second: {lines/elapsed:,.0f}")
