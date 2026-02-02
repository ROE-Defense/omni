#!/bin/bash
set -e

# Omni Installer
# Usage: curl -sL https://tinyurl.com/omni-install | bash

echo "⚡ Installing Omni..."

# Detect OS
OS="$(uname -s)"
ARCH="$(uname -m)"

if [ "$OS" == "Darwin" ]; then
    echo "  • Detected macOS ($ARCH)"
elif [ "$OS" == "Linux" ]; then
    echo "  • Detected Linux ($ARCH)"
else
    echo "  X Unsupported OS: $OS"
    exit 1
fi

# Clone/Pull
INSTALL_DIR="$HOME/.omni"
if [ -d "$INSTALL_DIR" ]; then
    echo "  • Updating existing installation..."
    cd "$INSTALL_DIR"
    git pull --quiet
else
    echo "  • Cloning repository..."
    git clone --quiet https://github.com/AureliusSystemsAI/omni.git "$INSTALL_DIR"
fi

# Setup Venv
echo "  • Setting up Python environment..."
cd "$INSTALL_DIR"
python3 -m venv venv
./venv/bin/pip install -e . --quiet

# Add to PATH (if not present)
SHELL_CONFIG=""
if [ "$SHELL" == "/bin/zsh" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ "$SHELL" == "/bin/bash" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
fi

if [ -n "$SHELL_CONFIG" ]; then
    if ! grep -q "$INSTALL_DIR/venv/bin" "$SHELL_CONFIG"; then
        echo "  • Adding to PATH ($SHELL_CONFIG)..."
        echo "export PATH=\"\$PATH:$INSTALL_DIR/venv/bin\"" >> "$SHELL_CONFIG"
        echo "  ℹ️  Please run: source $SHELL_CONFIG"
    fi
fi

echo ""
echo "✅ Omni Installed Successfully!"
echo "   Run 'omni init' to start."
