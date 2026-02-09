# Omni Benchmark Report - v0.7.0 (Swarm Alpha)
**Date:** 2026-02-08
**Tester:** ROE Defense (AI)
**Focus:** Desktop App Experience.

## Incident Report
User reported two issues:
1.  **"Green empty square" response:** The Desktop App uses a markdown renderer that hides code blocks (`pre: () => <div className="hidden" />`) to move them to the sidebar. However, if the sidebar logic fails or the user doesn't see it, they just see an empty square (the hidden div style/placeholder).
2.  **Missing Sidebar Features:** The sidebar shows "Generated Artifacts" only when `artifacts.length > 0`. If generation fails or returns no files, the sidebar is empty.

## Root Cause
*   **UI Design:** The `App.jsx` actively hides code blocks in the main chat window (`pre: () => <div className="hidden" />`).
*   **Artifacts:** The artifacts array only populates *after* the `processed` event from the backend. If the backend crashed or returned early (before `done`), the artifacts array remains empty, leaving the user with hidden code in chat and an empty sidebar.

## Action Plan
1.  **Fix UI:** Stop hiding code blocks in the chat. They should be visible *and* in the sidebar (or at least visible until processed).
2.  **Verify Backend:** Ensure the backend (`omni serve`) is actually returning artifacts properly via the WebSocket.

## Test
I will modify `desktop/src/App.jsx` to show code blocks again, so the user can at least see the raw code even if the sidebar extraction fails.
