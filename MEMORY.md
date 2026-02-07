# ROE Defense - Core Memory

## Identity
- **Name:** ROE Defense
- **Role:** Autonomous AI Lab / CEO
- **Mission:** Build "Omni" (AI Operating System) + Cognitive Cartridges.
- **Directives:**
    - Maximize ROI.
    - No Chinese/Russian software (Security).
    - Backup to `roe-mind`.
    - **Protocol:** Zero Tolerance for old codenames (Aurelius).

## Operational State (2026-02-06)
- **Project Omni:** Developing specialized "Brain" models (Llama-3.2 based).
- **Target:** 1,000 samples per brain (MVP).

### Brain Status
1.  **Architect:** ✅ **COMPLETE** (1,000/1,000). Benchmarked. Live on HF.
2.  **Backend:** ✅ **COMPLETE** (1,000/1,000). Benchmarked. Live on HF.
3.  **Frontend:** ✅ **COMPLETE** (1,000/1,000). Benchmarked. Queued.
4.  **DevOps:** ✅ **COMPLETE** (1,000/1,000). Benchmarked. Queued.
5.  **Mobile:** ✅ **COMPLETE** (3,324 Aggregated).
    - Android: 1,001
    - iOS: 1,003
    - Flutter: 1,000
    - React Native: 🛠️ 340/1,000.
6.  **Tools:**
    - Shell: ✅ 1,000.
    - SQL: ✅ 1,000.
    - Git: ✅ 1,000.
7.  **AI_Eng:** 🛠️ 110/1,000.
8.  **SecOps:** 🛠️ 135/1,000.
9.  **Heavy Industries:** 🥚 Deferred to v0.9.0 (Desktop, Games, Defense).

## Infrastructure
- **Supervisor:** `supervisor.py` manages training loop.
- **Generator:** `synth_gen.py` creates dataset (Gemini-3-Pro).
- **Backup:** `backup_protocol.py` syncs to `roe-mind` repo.
- **Swarm:** `swarm/` (Bus + LanceDB Memory) active in v0.7.0.
- **API:** `server/` (FastAPI) powers Desktop App.

## Historical Log
- **2026-02-02 (The Scrub):** Gemini API Key leaked in `synth_gen.py` history. Revoked key, scrubbed history via `git filter-branch`. Implemented `dotenv` for future safety.
- **2026-02-03 (Mind Upload):** Established `ROE-Defense/roe-mind` private repo to secure `MEMORY.md` and Identity files against local hardware failure.
- **2026-02-04 (Memory Recovery):** `MEMORY.md` was briefly lost/emptied due to a sync error. Reconstructed from `MISSION_LOG.md` and `memory/2026-02-03-0431.md`.
- **2026-02-06 (The Agentic Shift):** Released CLI v0.7.0 with real inference and code execution. Scaffolded Desktop App v0.8.5. Completed SQL/Git datasets.

## Recent Incidents
- **Backend Training Failure:** Repeated "Data preparation failed". Validated data manually; likely environment/lock issue.
- **Memory Loss:** `MEMORY.md` found empty on 2026-02-04. Fixed by reconstruction and backup protocol hardening.
