# fluffy-funicular

A benchmarking repository for the 1 Billion Row Challenge (1BRC) - finding the fastest way to read 1 billion lines from a text file using Python's built-in features.

## Overview

This repository contains various implementations for reading large text files, separated into:
- **Single-threaded solutions**: Sequential processing approaches
- **Multi-threaded solutions**: Parallel processing using threads and multiprocessing

All solutions use only Python's built-in features (no external dependencies for the actual processing).

## Project Structure

```
fluffy-funicular/
├── single_threaded/          # Single-threaded implementations
│   ├── basic_readline.py     # Basic line-by-line reading
│   ├── buffered_read.py      # Custom buffer size approach
│   └── chunked_readlines.py  # Chunked reading with readlines
├── multi_threaded/           # Multi-threaded implementations
│   ├── thread_pool.py        # ThreadPoolExecutor approach
│   └── multiprocess_pool.py  # Multiprocessing Pool approach
├── generate_data.py          # Test data generator
├── benchmark.py              # Benchmark runner
├── .flake8                   # Flake8 configuration
├── pyproject.toml           # Project configuration and dependencies
└── uv.lock                  # Locked dependencies
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/better-salmon/fluffy-funicular.git
   cd fluffy-funicular
   ```

2. **Install dependencies (optional, for linting/formatting):**
   ```bash
   uv sync --all-extras
   ```
   
   This will create a virtual environment and install development tools (Black, Flake8, isort).

## Usage

### Generate Test Data

Create a test file with a specified number of lines:

```bash
# Using Python directly
python generate_data.py <output_file> <num_lines>

# Using uv
uv run generate_data.py <output_file> <num_lines>
```

Example:
```bash
# Using Python directly
python generate_data.py test_data.txt 1000000

# Using uv
uv run generate_data.py test_data.txt 1000000
```

### Run Individual Solutions

**Single-threaded:**
```bash
# Using Python directly
python single_threaded/basic_readline.py <file_path>
python single_threaded/buffered_read.py <file_path>
python single_threaded/chunked_readlines.py <file_path>

# Using uv
uv run single_threaded/basic_readline.py <file_path>
uv run single_threaded/buffered_read.py <file_path>
uv run single_threaded/chunked_readlines.py <file_path>
```

**Multi-threaded:**
```bash
# Using Python directly
python multi_threaded/thread_pool.py <file_path> [num_threads]
python multi_threaded/multiprocess_pool.py <file_path> [num_processes]

# Using uv
uv run multi_threaded/thread_pool.py <file_path> [num_threads]
uv run multi_threaded/multiprocess_pool.py <file_path> [num_processes]
```

### Run Benchmarks

Compare all solutions on the same file:

```bash
# Using Python directly
python benchmark.py <file_path>

# Using uv
uv run benchmark.py <file_path>
```

Example workflow:
```bash
# Using Python directly
# Generate 10 million line test file
python generate_data.py test.txt 10000000

# Run benchmarks
python benchmark.py test.txt

# Using uv
# Generate 10 million line test file
uv run generate_data.py test.txt 10000000

# Run benchmarks
uv run benchmark.py test.txt
```

## Linting and Formatting

This project uses industry-standard tools for code quality:

- **Black**: Code formatter
- **Flake8**: Style guide enforcement
- **isort**: Import sorting

### Format code:
```bash
uv run black .
uv run isort .
```

### Lint code:
```bash
uv run flake8 .
```

## Solutions Explained

### Single-threaded Solutions

1. **basic_readline.py**: Simple iteration over file lines. Most straightforward approach.

2. **buffered_read.py**: Uses a custom buffer size (1MB) to potentially improve I/O performance.

3. **chunked_readlines.py**: Reads file in chunks using `readlines()` with a size hint (10MB).

### Multi-threaded Solutions

1. **thread_pool.py**: Divides file into chunks and processes them in parallel using `ThreadPoolExecutor`. Good for I/O-bound operations.

2. **multiprocess_pool.py**: Uses `multiprocessing.Pool` to process chunks in separate processes. Better for CPU-bound operations and bypasses Python's GIL.

## Performance Considerations

- **Single-threaded** solutions are simpler and have less overhead, suitable for smaller files or when CPU cores are limited.
- **Multi-threaded** solutions can provide significant speedup for large files on multi-core systems.
- **Threading** is generally better for I/O-bound operations (like reading files).
- **Multiprocessing** provides true parallelism but has higher overhead due to process creation.

## Contributing

Feel free to add new solutions or optimizations! Please ensure:
- Solutions use only built-in Python features
- Code is formatted with Black and passes Flake8 checks
- Solutions are placed in the appropriate directory (single_threaded or multi_threaded)

## License

MIT