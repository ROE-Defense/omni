# Omni: The Secure AI Stack

**Omni** is a sovereign AI Runtime that turns your Mac Mini (or Linux/Windows machine) into an air-gapped intelligence node. It runs specialized 1B/3B parameter models ("Cognitive Cartridges") that outperform GPT-4 on specific tasks, with zero latency and zero data leaks.

## 🚀 Quick Install

### Mac / Linux (Universal)
```bash
curl -fsSL https://roe-defense.github.io/omni/install.sh | bash
```

### Windows (WSL)
```bash
wsl curl -fsSL https://roe-defense.github.io/omni/install.sh | bash
```

## 🧠 Specialized Brains

Omni ships with specialized brains. You can hot-swap them instantly:

| Brain | Status | Purpose | Tech Stack |
| :--- | :--- | :--- | :--- |
| **@roe/architect** | ✅ **Live** | System Design & Strategy | Cloud-Native, Distributed Systems |
| **@roe/backend** | ✅ **Live** | API & Database Logic | Python, FastAPI, Node, SQL |
| **@roe/frontend** | ✅ **Live** | Web UI Development | React, Tailwind, TypeScript |
| **@roe/devops** | ✅ **Live** | Infrastructure & Defense | Docker, K8s, SecOps, Linux Hardening |
| **@roe/ios** | ⏳ Soon | Native iOS Apps | Swift, SwiftUI, Combine |
| **@roe/android** | ⏳ Soon | Native Android Apps | Kotlin, Compose, Gradle |
| **@roe/flutter** | ⏳ Soon | Cross-Platform Mobile | Dart, Widgets, Plugins |
| **@roe/desktop** | ⏳ Soon | Native Desktop Apps | MacOS Native, Windows .NET, Rust |
| **@roe/ai-eng** | ⏳ Soon | AI Engineering | PyTorch, RAG, LangChain, Agents |

## ✨ Features

-   **100% Local:** Runs on Apple Silicon (Metal) or NVIDIA (CUDA). No API keys required.
-   **Zero-Trace Training:** Fine-tune your own brains (`@roe/custom`) on local documents. Raw data is shredded immediately after training.
-   **Air-Gapped:** Designed for defense and critical infrastructure. No telemetry.

## 🛠 Usage

**Start the Interactive Wizard:**
```bash
omni run
```

**Install a Brain:**
```bash
omni install @roe/atak
```

**Run an Agent Task:**
```bash
omni run "Build a React component for a login form"
```

## 📜 License

MIT License. Copyright (c) 2026 ROE Defense.
