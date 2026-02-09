# Omni Benchmark Report - v0.7.0 (Swarm Alpha)
**Date:** 2026-02-08
**Tester:** ROE Defense (AI)
**Focus:** CLI vs. Desktop Integration.

## Incident Report
User reported `net::ERR_CONNECTION_REFUSED` when using the Desktop App.
**Root Cause:** The Benchmark passed for the CLI core (`omni.py`) but the Desktop App relies on the API Server (`omni serve`) which was not running.
**Fix:** Manually started `omni serve` and verified API availability.

## Test Suite Results

### 1. CLI Core (Offline Generation)
*   **Test:** `run_benchmark.py` (Snake, Dashboard, Deduplicator)
*   **Status:** ✅ PASS (Verified via `03523a4`)
*   **Notes:** Successfully creates files in `public/` when run from terminal.

### 2. API Server (Desktop Backend)
*   **Test:** `curl` request to `http://127.0.0.1:8000/chat`
*   **Status:** ✅ PASS
*   **Notes:** Server is now running (PID 10241). Returns valid JSON artifacts.

### 3. Integrated Experience
*   **Action:** User must run `omni serve` before launching Desktop App.
*   **Verification:** Verified via `curl` that backend is listening.

## Conclusion
The system is functional, but user error (server not started) caused the perceived failure.
**Action Item:** Update documentation/UI to auto-start server or warn user.
