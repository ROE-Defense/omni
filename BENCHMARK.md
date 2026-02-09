# Omni Benchmark Report - v0.7.0 (Swarm Alpha)
**Date:** 2026-02-08
**Tester:** ROE Defense (AI)
**Focus:** Performance Tuning.

## Incident Report
User reported "it took forever thinking this run".
**Data:**
*   `models/architect-fused`: 6.0GB
*   `models/backend-fused`: 6.0GB
*   ... and so on.
**Total Brains Size:** ~44GB.

## Root Cause
The system is using **Full Fused Models** (6GB each) instead of **LoRA Adapters** (which would be ~100MB + 1 Base Model).
Every time the intent router switches personas (e.g., from "Base" to "Architect"), the system has to:
1.  Dump 6GB from RAM.
2.  Load a new 6GB file from disk.
3.  Re-initialize the Metal cache.
On a MacBook, this takes 5-15 seconds of pure I/O and memory bandwidth, appearing as "thinking" time.

## Optimization Plan
1.  **Short Term:** Inform user that switching "Brains" is heavy.
2.  **Code Optimization:** Ensure `route_intent` is not "flapping" (switching back and forth unnecessarily).
3.  **Long Term (v0.8.0):** Switch to LoRA Adapter runtime (load Base Model once, hot-swap 100MB adapters). *Current MLX implementation in `server/core.py` uses `load()` which implies full weights.*

## Immediate Action
I will verify if `server/core.py` can be made "sticky" to avoid switching back to Base Brain for simple queries if a Specialized Brain is already loaded.
