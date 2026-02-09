# Omni Benchmark Report - v0.7.0 (Swarm Alpha)
**Date:** 2026-02-08
**Tester:** ROE Defense (AI)
**Focus:** Production Stability.

## Incident Report
User encountered `ModuleNotFoundError: No module named 'dash'` during launch of the generated "Stock Dashboard" app.
**Root Cause:** The model generated `app.py` using `dash`, but the `requirements.txt` only contained `flask`. Additionally, `package.json` contained invalid dependencies (`flask` via npm).

## Fix Execution
1.  **Workspace Repair:**
    *   Updated `~/.omni/workspace/requirements.txt` to include `dash`, `pandas`, `yfinance`.
    *   Fixed `~/.omni/workspace/package.json` to remove invalid npm packages.
    *   Created `launch_fix.sh` for the user to manually recover if needed.
2.  **System Prevention:**
    *   Updated `server/core.py` prompt to explicitly forbid putting python packages in `package.json` and enforce complete `requirements.txt`.

## Status
*   **User App:** Repaired locally. The next launch should work.
*   **System Core:** Hardened against mixed-dependency hallucinations.

## Next Steps
User should click "LAUNCH APP" again or run the fix script.
