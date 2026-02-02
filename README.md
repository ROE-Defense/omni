# 📦 cpack (Context Packer)

**Stop copy-pasting 15 files into ChatGPT.**

`cpack` is a lightning-fast CLI tool that bundles your entire code project into a single, LLM-ready text file. It respects `.gitignore`, skips binaries, and formats everything in Markdown so your AI (Claude, GPT-4, DeepSeek) understands the context immediately.

## 🚀 Features

- **Smart Ignore**: Automatically respects your `.gitignore` rules.
- **Binary Detection**: Skips images, executables, and other non-text files.
- **Token Friendly**: Adds file trees and clear delimiters to help LLMs parse structure.
- **Security**: Auto-ignores common secret keys (`.pem`, `.enc`, `.env`).
- **Clipboard Mode**: Pipe directly to your clipboard with `-c`.

## 📦 Installation

Just grab the script (no heavy dependencies):

```bash
git clone https://github.com/your-username/cpack.git
cd cpack
chmod +x cpack.py
# Optional: Link to your path
ln -s $(pwd)/cpack.py /usr/local/bin/cpack
```

## ⚡ Usage

**Pack current directory to clipboard:**
```bash
cpack -c
```

**Pack specific folder to a file:**
```bash
cpack /path/to/project -o context.txt
```

**Pack and print to stdout (for piping):**
```bash
cpack | pbcopy
```

## 🧠 Why?

"I want to fix a bug in `auth.py`, but it depends on `db.py` and `config.py`."

**The Old Way:**
1. Copy `auth.py` -> Paste.
2. Copy `db.py` -> Paste.
3. Copy `config.py` -> Paste.
4. "Wait, I forgot the schema..."

**The cpack Way:**
1. `cpack -c`
2. Paste into Chat.
3. "Fix the auth bug."

## 📄 License

MIT. Build cool stuff.
