# Omni Benchmark Report - v0.7.0 (Swarm Alpha)
**Date:** 2026-02-08
**Tester:** ROE Defense (AI)
**Focus:** Orchestration, File Generation, Execution, Brain Selection.

## Test Suite Execution
Started automated benchmark suite `run_benchmark.py`.

### Test 1: Snake Game (Matrix Theme)
**Prompt:** "Make a single-file HTML snake game that looks like a Matrix simulation. Include '<!-- filename: public/matrix_snake.html -->' at the top."
**Status:** ❌ FAIL
**Notes:** 
- Omni executed but timed out or crashed without producing the file.
- `public/matrix_snake.html` not found.
- Investigation: Model might be hanging on generation or `omni.py` extraction logic is failing silently.

### Test 2: Stock Dashboard (React + Python)
**Prompt:** "Create a React component 'StockDash.jsx'... Include '# filename: public/StockDash.jsx'. Also create a python script 'stock_api.py'... Include '# filename: public/stock_api.py'."
**Status:** ❌ FAIL
**Notes:** 
- `public/StockDash.jsx` not found.

### Test 3: File Deduplicator (System Util)
**Prompt:** "Write a python script to find duplicate files... Include '# filename: public/dedup.py'."
**Status:** ❌ FAIL (Manual Kill)
**Notes:** 
- Process ran for >5 minutes without output.
- Manually killed to prevent resource hog.
- `public/dedup.py` was not created.

## Diagnosis
The `omni.py` core seems to be loading the model correctly (memory usage ~18GB, consistent with 3B model + overhead), but it fails to complete generation or save the file. This suggests:
1.  **Inference Hang:** The model generation is stuck in an infinite loop or waiting for a stop token it never generates.
2.  **Output Parsing:** The regex might not be matching the output format, or the output is not being flushed.
3.  **Headless Mode:** The `AUTO_CONFIRM` might not be triggering correctly in the `extract_and_run` loop.

## Next Steps
1.  Debug `omni.py` generation loop.
2.  Add explicit logging to `extract_and_run`.
3.  Force a shorter max_tokens limit for testing.
