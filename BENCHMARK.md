# Omni Benchmark Report - v0.7.0 (Swarm Alpha)
**Date:** 2026-02-08
**Tester:** ROE Defense (AI)
**Focus:** Orchestration, File Generation, Execution, Brain Selection.

## Test Suite Execution
Started automated benchmark suite `run_benchmark.py`.

### Test 1: Snake Game (Matrix Theme)
**Prompt:** "Make a single-file HTML snake game that looks like a Matrix simulation. Include '<!-- filename: public/matrix_snake.html -->' at the top."
**Status:** IN PROGRESS (Inference Running)
**Notes:** 
- Updated `omni.py` to support headless CLI arguments and `AUTO_CONFIRM`.
- Updated regex to capture filenames from comments (`#`, `//`, `<!--`).
- Expected Output: `public/matrix_snake.html`.

### Test 2: Stock Dashboard (React + Python)
**Prompt:** "Create a React component 'StockDash.jsx'... Include '# filename: public/StockDash.jsx'. Also create a python script 'stock_api.py'... Include '# filename: public/stock_api.py'."
**Status:** PENDING
**Notes:** 
- Will verify multi-block code extraction.
- Will verify `jsx` and `py` extensions.

### Test 3: File Deduplicator (System Util)
**Prompt:** "Write a python script to find duplicate files... Include '# filename: public/dedup.py'."
**Status:** PENDING
**Notes:** 
- Will verify `os` and `hashlib` imports.
- Will verify safe execution (dry run first).

## System Updates
- `omni.py`: Added headless support, regex filename parsing, multi-block extraction.
- `requirements.txt`: Added `rich`, `typer`, `inquirer`, `requests`.
- `run_benchmark.py`: Created automated test runner.
