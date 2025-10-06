"""
Multi-threaded solution: Using ThreadPoolExecutor.

Divides the file into chunks and processes them in parallel using threads.
Uses only built-in threading capabilities.
"""

import os
from concurrent.futures import ThreadPoolExecutor


def count_lines_in_chunk(filepath, start, end):
    """
    Count lines in a specific chunk of the file.

    Args:
        filepath: Path to the file to read
        start: Starting byte position
        end: Ending byte position

    Returns:
        Number of lines in this chunk
    """
    line_count = 0
    with open(filepath, "rb") as f:
        f.seek(start)
        # If not at the beginning, skip to the next newline
        if start != 0:
            f.readline()

        while f.tell() < end:
            line = f.readline()
            if not line:
                break
            line_count += 1

    return line_count


def read_lines_threaded(filepath, num_threads=4):
    """
    Read file using multiple threads.

    Args:
        filepath: Path to the file to read
        num_threads: Number of threads to use

    Returns:
        Total number of lines read
    """
    file_size = os.path.getsize(filepath)
    chunk_size = file_size // num_threads

    chunks = []
    for i in range(num_threads):
        start = i * chunk_size
        end = file_size if i == num_threads - 1 else (i + 1) * chunk_size
        chunks.append((filepath, start, end))

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = executor.map(lambda args: count_lines_in_chunk(*args), chunks)

    return sum(results)


if __name__ == "__main__":
    import sys
    import time

    if len(sys.argv) < 2:
        print("Usage: python thread_pool.py <filepath> [num_threads]")
        sys.exit(1)

    filepath = sys.argv[1]
    num_threads = int(sys.argv[2]) if len(sys.argv) > 2 else 4

    start_time = time.time()
    lines = read_lines_threaded(filepath, num_threads)
    elapsed = time.time() - start_time

    print(f"Lines read: {lines:,}")
    print(f"Threads used: {num_threads}")
    print(f"Time elapsed: {elapsed:.2f} seconds")
    print(f"Lines per second: {lines/elapsed:,.0f}")
