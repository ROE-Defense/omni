# Omni Benchmark Report - v0.7.0 (Swarm Alpha)
**Date:** 2026-02-08
**Tester:** ROE Defense (AI)
**Focus:** Desktop App Experience (UI Logic).

## Incident Report
User stated: "I never want the code in the chat window, only the right sidebar. Remember that."
This reverses my previous fix (which made code visible in chat). The original logic was correct per user preference, but the **sidebar was not populating**, leading to the "empty green square" experience.

## Root Cause (Sidebar Failure)
The sidebar *only* populates when `artifacts.length > 0`.
Artifacts are populated via the WebSocket message `{type: 'artifacts', data: [...]}`.
This message is sent by the backend (`server/app.py`) *after* processing the full response.
If the model output format does not perfectly match the executor's regex (e.g., missing `# filename:` comments), `omni.executor.process` returns no artifacts, and thus the sidebar remains empty.

**The catch:** The Desktop App hides the code block in the chat (`div class="hidden"`) *assuming* it will appear in the sidebar. If extraction fails, the user sees nothing.

## Fix Strategy
1.  **Revert Chat Visibility:** Hide code blocks in chat again (per user request).
2.  **Fix Sidebar Populating:** Ensure the sidebar shows *something* even if formal artifact extraction fails, OR ensure extraction is robust.
3.  **Intermediate State:** The `streamingCode` state in `App.jsx` handles the "Incoming Transmission" view in the sidebar while generating. This works!
4.  **Final State:** Once done, `streamingCode` is cleared. If `artifacts` is empty, the sidebar goes blank.

**Solution:**
We need to capture the *raw code blocks* during streaming and keep them in the sidebar even if the backend validator doesn't "bless" them as official artifacts. Or, strictly enforce the backend to return "Unknown Artifact" if it finds code without a filename.

**Immediate Action:**
I will revert the chat visibility change (hide code again). I will verify `omni.py` and `server/core.py` are forcing filenames so `artifacts` always populate.
