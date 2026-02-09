# Omni Benchmark Report - v0.7.0 (Swarm Alpha)
**Date:** 2026-02-08
**Tester:** ROE Defense (AI)
**Focus:** Error Analysis (20:09 MST Run).

## Analysis of Last Run (20:09:52 MST)
**User Inquiry:** "review the last run for issues"
**Log ID:** `sharp-haven` (PID 11157)

### Detected Issues:
1.  **Malformed Requirements:** `generated_1770606592.flask` was created with content `==2.0.2\n`.
    *   **Reason:** The executor (`server/executor.py`) fell back to `generated_{time}.{ext}` logic because the model did not provide a `# filename:` comment inside the block.
    *   **Ext Issue:** The model tagged the code block as ` ```flask `, causing the executor to use `.flask` as the extension.
    *   **Content Issue:** The model output `==2.0.2` instead of `Flask==2.0.2`.
2.  **Phantom React:** `launch_1770606592.sh` contained `npm run dev`, but no React files were generated.
    *   **Reason:** The system prompt in `server/core.py` gave an example: `python3 app.py & npm run dev`. The model blindly copied this example instead of adapting to the *actual* generated code (pure python).

### Fix Strategy
1.  **Executor:** Update `_get_filename` to handle `flask` language tag -> `.txt` or `.py` fallback, and detect `requirements.txt` content more robustly.
2.  **Core Prompt:** Update `server/core.py` to remove the misleading `npm run dev` example and explicitly warn against including it for Python-only apps.

## Action Plan
1.  Patch `server/executor.py` to map `flask` -> `txt` (or better, detect requirements content).
2.  Patch `server/core.py` to fix the `start.sh` example prompt.
