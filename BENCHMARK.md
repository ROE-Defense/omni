# Omni Benchmark Report - v0.7.0 (Swarm Alpha)
**Date:** 2026-02-08
**Tester:** ROE Defense (AI)
**Focus:** Error Analysis (22:24 MST).

## Incident Report
**User Issue:** "Another fail, review the run"
**Run Time:** ~22:23 MST (Timestamp 1770614615)
**Intent:** "Make a snake game" (implied by file content).

### Artifact Analysis
*   `generated_1770614615.html`: Valid HTML5 Canvas setup.
*   `generated_1770614615.js`: Valid JS logic for Snake.
*   `generated_1770614615.css`: (Likely valid CSS).
*   `launch_1770614615.sh`: **CRITICAL FAILURE.**
    *   Content: `python3 app.py`.
    *   Issue 1: There is no `app.py` in this generation! The user asked for a snake game, the model generated static HTML/JS, but the launch script tried to run a nonexistent Python backend.
    *   Issue 2: The static files (`index.html` etc.) were named `generated_....html` by the executor because the model didn't provide `# filename: index.html` comments inside the blocks (or the regex missed them).

### Root Cause
1.  **Hallucinated Launcher:** The model is obsessed with the `python3 app.py` example in the system prompt, even when generating a static site.
2.  **Naming Failure:** The executor assigned random timestamps (`generated_...`) instead of `index.html`, making the files disconnected. `launch.sh` (if it worked) wouldn't know where to look.

### Fix Strategy
1.  **Smart Executor:** If `app.py` is missing but `index.html` (or `.html` file) exists, the launch script should just `open index.html`.
2.  **Prompt Refinement:** Tell the model: "For static sites (HTML/JS), do NOT generate a start.sh script. Just provide the files." OR "If static, start.sh should just be `open index.html`".

## Action Plan
1.  Update `server/core.py` prompt to handle Static Sites explicitly.
2.  Update `server/executor.py` to auto-detect "Entry Point" if the model's `launch.sh` is broken.
