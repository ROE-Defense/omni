# Omni: The Sovereign Roadmap (2.0)

This roadmap transforms Omni from a "Local LLM Wrapper" into a true **AI Operating System**.

## Phase 1: The Foundation (v0.2.x - v0.3.x)
*Focus: Stability, Core Brains, and User Experience.*

### 🧠 Model Evolution (The Brains)
-   **Expansion to 2,000 Samples:**
    -   **Current:** 1k samples = "Competent Junior."
    -   **Upgrade:** Retrain all brains at 2k samples (Synth + Human Verified).
    -   **Goal:** "Mid-Level Senior" capability. Reduced hallucinations in niche syntax (e.g., ATAK XML, K8s manifests).
-   **New Brains:**
    -   **`@roe/analyst`:** Specialized in CSV/Excel data analysis, Python Pandas, and generating charts (matplotlib).
    -   **`@roe/writer`:** Specialized in creative writing, technical documentation, and blog posts (steerable tone).
    -   **`@roe/vision`:** (Multimodal) Integration of LlaVA or similar for image analysis ("What's in this screenshot?").

### 🛠 Technical Core
-   **Universal Installer v2:** One-line install for Windows (PowerShell native, no WSL required), Linux, and Mac.
-   **Auto-Updater:** `omni update` acts like `apt-get upgrade` for your AI brains. Checks hashes, pulls deltas.
-   **Context Window Expansion:** Bump default context from 2k to **8k or 16k** (using RoPE scaling) to handle larger codebases.

### 👤 User Experience
-   **Web UI (Localhost):** A beautiful, dark-mode web interface (`localhost:8080`) for users who prefer GUIs over CLI. Chat style (like ChatGPT) but 100% local.
-   **"Goal Mode" (Wizard):** As planned, the intent-based selector.

---

## Phase 2: The Swarm & Integration (v0.4.x - v0.5.x)
*Focus: Interoperability and Workflow Automation.*

### 🐝 The Swarm Runtime (Multi-Agent)
-   **The "Bus" Protocol:** A JSON-based standard for brains to pass data.
    -   *Example:* Architect passes `{ "files": ["app.py", "db.py"] }` -> Backend fills content -> Reviewer audits it.
-   **Shared Working Memory:** A persistent vector store (ChromaDB or FAISS local) that all agents can read/write to. "Remember the API key I gave the backend agent? Frontend agent needs it too."

### 🔌 Developer Ecosystem
-   **Omni API Server:** Expose an OpenAI-compatible API endpoint (`http://localhost:11434/v1/chat/completions`).
    -   *Benefit:* Use Omni brains inside VS Code (Cursor/Copilot), Obsidian, or any 3rd party tool.
-   **Brain SDK:** A simple Python framework for users to define their own brains (`class MyBrain(OmniBrain): ...`).

### 📱 "Everywhere" Access
-   **Mobile Companion:** A minimal iOS/Android app that connects to your home Omni node via secure P2P (Tailscale/Wireguard integrated). Chat with your sovereign AI while away from home.

---

## Phase 3: The "Sovereign OS" (v0.6.x - v0.9.x)
*Focus: Multimodal, Autonomous Action, and Hardware.*

### 👁️ Multimodal Native
-   **"Screen Aware":** Omni can see your screen (snapshot every 5s). "How do I fix this error?" (Omni sees the error dialog).
-   **"Voice Mode":** Real-time, low-latency voice conversation (Whisper + Local TTS). Interruptible. "Omni, stop, actually do this..."

### 🦾 Active Agency (Computer Use)
-   **The "Hand":** Give Omni the ability to *control* the mouse/keyboard (sandboxed).
    -   *Task:* "Organize my Downloads folder."
    -   *Action:* Omni visually scans files, creates folders, moves them.
-   **Browser Driver:** Headless browser control. "Go to GitHub, find the latest release of X, and summarize the changelog."

### 🔒 Defense Grade
-   **The "Air Gap" Mode:** A strict hardware switch (software enforced) that disables the network adapter while Omni processes sensitive data.
-   **Encrypted Memory:** All `memory/*.md` files and vector stores are encrypted at rest with a user password.

---

## Phase 4: Release 1.0 (The Singularity)
*Focus: Production Ready, Certified, and polished.*

-   **Certification:** Audited code for no telemetry. "Clean Room" build verification.
-   **Hardware Kits:** Official ROE Defense "Compute Bricks" (Pre-flashed Jetson Orin or Mac Mini clusters) shipped to users. Plug and play sovereignty.
-   **The "Hive":** Optional P2P networking where trusted Omni nodes (e.g., your team's laptops) can share compute or knowledge without a central server.

---

## 🛑 Technical Updates Needed to Achieve This
1.  **Quantization Engine:** Build a pipeline to auto-quantize models to 4-bit/5-bit/6-bit based on user RAM.
2.  **Memory Management:** Dynamic loading/unloading of LoRA adapters to keep RAM usage low (~100MB per agent).
3.  **Vector Database:** Integrate a lightweight, file-based vector DB (like LanceDB) for long-term recall.
4.  **Audio Pipeline:** Integrate `whisper.cpp` (STT) and a high-quality local TTS (Piper or similar) into the binary.

This roadmap moves us from "Cool Tool" to "Essential Infrastructure."
