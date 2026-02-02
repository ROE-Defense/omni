# 📦 Context Suite (cpack + cchat)

**The AI-Native Developer Toolkit.**

Stop wrestling with context windows. `Context Suite` provides the fastest way to bridge your local codebase with Large Language Models.

## 🛠 Tools

### 1. `cpack` (Context Packer)
Bundles your entire project into a single, LLM-optimized Markdown file.
- **Smart Ignore:** Respects `.gitignore`.
- **Safety:** Auto-filters secrets and binaries.
- **Clipboard Mode:** `cpack -c` -> Paste into ChatGPT.

### 2. `cchat` (Context Chat)
Chat directly with your codebase from the terminal.
- **No Dependencies:** Pure Python standard library.
- **Model Agnostic:** Works with OpenAI, DeepSeek, or any compatible API.
- **Usage:** `python3 cchat.py "How do I fix the auth bug?"`

## 📦 Installation

```bash
git clone https://github.com/your-username/context-suite.git
cd context-suite
chmod +x cpack.py cchat.py
```

## ⚡ Usage

**Pack to clipboard:**
```bash
./cpack.py -c
```

**Chat with code:**
```bash
export OPENAI_API_KEY="sk-..."
./cchat.py "Explain the architecture of this app"
```

## 🤖 Built By AI
Designed and coded by **Aurelius Systems** (Vector Agent).
100% Autonomous Code Generation.
