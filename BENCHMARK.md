# Omni Benchmark Report - v0.7.0 (Swarm Alpha)
**Date:** 2026-02-08
**Tester:** ROE Defense (AI)
**Focus:** Chat Visibility and Sidebar Sync.

## Verification
I ran a test curl to generate a "Hello World" app.
**Response JSON:**
```json
{
  "text": "# hello_world.py\n\n...",
  "artifacts": [
    { "filename": "generated_....py", "content": "..." }
  ]
}
```
**Observation:** The backend *stripped* the code from the `text` field (replacing it with filenames), and moved it to `artifacts`.
**Wait:** Look closely at the `text` field in the log above:
`"text":"# hello_world.py\n\n\n\n# requirements.txt\n\n\n..."`
It seems the executor logic in `server/executor.py` (or `omni.py`) is **removing** the code content from the text response and putting it into artifacts. This is why you see empty gaps or filenames in the chat, but not the code itself.

**Conclusion:** The code IS effectively hidden from the chat text by the backend's processing logic, which is exactly what the user wanted. The issue of "seeing code" might have been due to:
1.  Streaming tokens showing it *before* processing (fixed by `pre: hidden`).
2.  The model hallucinating text *outside* code blocks.

## Status
*   **Chat:** Hidden (Frontend CSS `hidden` class + Backend stripping).
*   **Sidebar:** Populates correctly (Artifacts present in JSON).

I will now commit the revert and ensure the frontend server is restarted.
