# Omni: The Sovereign Roadmap (Detailed Master Plan)

**Mission:** Create the world's first "Sovereign AI Operating System" — a local-only, air-gapped, multi-agent development environment that outperforms cloud models through specialization.

**Current Version:** v0.2.2 (Beta)
**Target v1.0 Release:** Q4 2026

---

## ✅ v0.1.0 - v0.2.x: The Core Runtime (Completed/Active)
*Status: Live / Maintenance*

### **1. The Omni Runtime Shell**
-   **Interactive Wizard (`omni run`):** A TUI (Text User Interface) for managing the system.
-   **Hardware Abstraction Layer:** Auto-detects Apple Silicon (Metal/MPS) vs NVIDIA (CUDA) vs CPU.
-   **Dependency Sandbox:** Automatically creates and manages a dedicated Python venv (`~/.omni/venv`) to avoid system conflicts.
-   **Model Manager:** Downloads, verifies hashes, and organizes `.gguf` models in `~/.omni/cartridges`.

### **2. The First "Cognitive Cartridges" (3B Parameters)**
-   **`@roe/architect`:** Fine-tuned on 1,000 system design scenarios. Can output MermaidJS diagrams, folder structures, and tech stack recommendations.
-   **`@roe/backend`:** Fine-tuned on 1,000 Python/FastAPI/SQL patterns. specialized in async DB calls and Pydantic models.
-   **`@roe/frontend`:** Fine-tuned on 1,000 React/Tailwind/TypeScript examples.

### **3. The "Immortal" Infrastructure**
-   **Supervisor Loop:** A background daemon that watches dataset files and auto-triggers LoRA training when thresholds (1k) are met.
-   **Mind Upload:** `backup_protocol.py` that syncs identity/memory to a private, encrypted git repo.
-   **Secure Synth Generator:** A data pipeline that rotates API keys to generate synthetic training data from Gemini-3-Pro without leaking secrets.

---

## 🔮 v0.3.0: The "Creator" Update (Next Up)
*Focus: Customization & Accessibility.*

### **1. "Train Your Own" (Local LoRA)**
-   **Feature:** `omni train --name @my/brain --path ./documents`
-   **Technical Detail:**
    -   Recursively ingests PDF, MD, TXT, and Code files from the target path.
    -   Uses a local 1B model (or Gemini API if allowed) to generate Q&A pairs from documents.
    -   Runs an MLX (Apple) or Unsloth (CUDA) LoRA fine-tuning job.
    -   Outputs a fused `.gguf` model ready to use.

### **2. The Web Interface (GUI)**
-   **Feature:** `omni web` launches a local server at `localhost:8080`.
-   **Technical Detail:**
    -   React-based "ChatGPT-like" interface.
    -   **Model Switcher:** Dropdown to hot-swap brains instantly.
    -   **System Stats:** Real-time VRAM/RAM usage visualization.
    -   **Dark/Hacker Mode:** CSS themes matching the CLI aesthetic.

### **3. Goal-Based Orchestration**
-   **Feature:** "I want to build a CRM." -> Omni installs Backend + Frontend + SQL brains.
-   **Technical Detail:** Simple keyword matching logic expanded into a decision tree classifier.

---

## 🔮 v0.4.0: The "Swarm" Update
*Focus: Multi-Agent Interoperability.*

### **1. The "Omni Bus" Protocol**
-   **Feature:** Standardized JSON schema for agents to exchange artifacts.
-   **Technical Detail:**
    -   `{ "sender": "architect", "recipient": "backend", "type": "spec", "payload": { ... } }`
    -   Allows one brain to "call" another brain without human copy-pasting.

### **2. The "Router" Model (1B)**
-   **Feature:** A tiny, always-on model that classifies user prompts.
-   **Technical Detail:**
    -   User: "Fix the CSS bug." -> Router: Activates `@roe/frontend`.
    -   User: "Optimize the SQL query." -> Router: Activates `@roe/backend`.
    -   Reduces latency by not loading the wrong 3B model.

### **3. Shared Project Memory (Vector Store)**
-   **Feature:** Agents remember the project context across sessions.
-   **Technical Detail:**
    -   Integration of **LanceDB** (embedded vector DB).
    -   Automatically chunks and embeds project files (`README.md`, code) into a persistent index.
    -   RAG (Retrieval Augmented Generation) enabled for all brains by default.

---

## 🔮 v0.5.0: The "Dev Ecosystem" Update
*Focus: Integration with external tools.*

### **1. Omni API Server**
-   **Feature:** Drop-in replacement for OpenAI API.
-   **Technical Detail:**
    -   Exposes `http://localhost:11434/v1/chat/completions`.
    -   Allows Omni to be used as the backend for VS Code extensions (Cursor, Copilot), Obsidian plugins, or custom scripts.

### **2. The Brain SDK (Python)**
-   **Feature:** Define complex agent behaviors in code.
-   **Technical Detail:**
    -   `class MyAgent(OmniAgent):` with hooks for `on_message`, `on_tool_call`.
    -   Allows developers to script specific workflows (e.g., "Run unit tests, then ask `@roe/backend` to fix errors").

### **3. Mobile Companion App**
-   **Feature:** Chat with your home Omni node from your phone.
-   **Technical Detail:**
    -   Flutter/React Native app.
    -   Uses **Tailscale** or **Tor Hidden Service** for secure, NAT-punching P2P connection. No central server.

---

## 🔮 v0.6.0: The "Visionary" Update
*Focus: Multimodal capabilities.*

### **1. Screen Awareness ("The Eye")**
-   **Feature:** Omni can "see" your screen.
-   **Technical Detail:**
    -   OCR + Vision Model (LlaVA or BakLLaVA 7B quantized).
    -   "Explain this error message." (Omni takes a screenshot, crops to the active window, analyzes text).

### **2. Voice Interface ("The Mouth")**
-   **Feature:** Full duplex voice conversation.
-   **Technical Detail:**
    -   **STT:** `whisper.cpp` (Tiny/Base English) for <200ms latency.
    -   **TTS:** `Piper` or `StyleTTS2` running locally.
    -   Wake word detection ("Hey Omni").

### **3. Image Generation**
-   **Feature:** Generate assets for frontend projects.
-   **Technical Detail:**
    -   Integration of **Stable Diffusion XL Turbo** (1-step generation).
    -   `@roe/frontend` can request: "Generate a placeholder hero image."

---

## 🔮 v0.7.0: The "Active Agency" Update
*Focus: Omni doing the work, not just chatting.*

### **1. "The Hand" (Input Injection)**
-   **Feature:** Omni can control mouse and keyboard.
-   **Technical Detail:**
    -   Sandboxed implementation using accessibility APIs (macOS) or uinput (Linux).
    -   Strict "Human-in-the-loop" confirmation before execution.

### **2. Headless Browser Driver**
-   **Feature:** Omni can research the web.
-   **Technical Detail:**
    -   Control of a headless Chromium instance (Playwright).
    -   Capabilities: Scrape docs, check GitHub issues, verify deployment URLs.

### **3. The File Surgeon**
-   **Feature:** Precise code editing.
-   **Technical Detail:**
    -   Instead of rewriting full files, Omni uses AST (Abstract Syntax Tree) parsing to inject code into specific functions or classes surgically.

---

## 🔮 v0.8.0: The "Quality Surge" Update
*Focus: Precision, Reliability, and Depth.*

### **1. 2,000 Sample Retraining**
-   **Feature:** All brains upgraded from "Junior" to "Senior".
-   **Technical Detail:**
    -   Expansion of training datasets to 2,000+ high-quality, human-verified samples per niche.
    -   Specific focus on edge cases (e.g., complex regex, legacy code refactoring).

### **2. New Specialist Brains**
-   **`@roe/analyst`:** Pandas/Matplotlib wizard. Auto-generates charts from CSVs.
-   **`@roe/writer`:** Technical documentation and blog post expert.
-   **`@roe/security`:** dedicated Red Teaming / Pen-testing brain.

### **3. Auto-Quantization Pipeline**
-   **Feature:** Omni optimizes itself for your RAM.
-   **Technical Detail:**
    -   Detects available RAM (e.g., 8GB vs 32GB).
    -   Automatically quantizes models to Q4_K_M, Q5_K_M, or Q8_0 to maximize intelligence within hardware limits.

---

## 🔮 v0.9.0: The "Sovereign OS" Update
*Focus: Security, Hardening, and Independence.*

### **1. Air Gap Mode (The Kill Switch)**
-   **Feature:** One-toggle total isolation.
-   **Technical Detail:**
    -   Software-level disable of network interfaces (`ifconfig down`).
    -   Verification that no process is attempting outbound connections.

### **2. Encrypted Vault**
-   **Feature:** Zero-knowledge storage.
-   **Technical Detail:**
    -   All `memory/*.md`, vector stores, and conversation logs are AES-256 encrypted at rest.
    -   Decrypted only in RAM when the user enters a session password.

### **3. The "Hive" (P2P Mesh)**
-   **Feature:** Distributed compute.
-   **Technical Detail:**
    -   Link your laptop + desktop + old server.
    -   Omni distributes the workload: "Laptop runs UI, Desktop runs Backend model, Server runs Vector DB."

---

## 🚀 v1.0.0: The Singularity (Release)
*Focus: Certification, Polish, and Physical Distribution.*

### **1. Zero-Telemetry Certification**
-   **Feature:** Trust but verify.
-   **Technical Detail:**
    -   Third-party audit of the codebase.
    -   Reproducible builds (users can compile binary and get exact hash match).

### **2. Hardware Kits**
-   **Feature:** Official ROE Defense Hardware.
-   **Technical Detail:**
    -   Custom-cased Mac Mini or Jetson Orin Nano.
    -   Pre-loaded with Omni v1.0.
    -   Physical "Privacy Switch" for microphone/camera.

### **3. Long Term Support (LTS)**
-   **Feature:** Stability guarantee.
-   **Technical Detail:**
    -   Commitment to support v1.0 API and model formats for 2 years.
    -   Enterprise support channels.
