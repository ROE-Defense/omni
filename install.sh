#!/bin/bash
set -e

# Omni Installer v1.1
# "It just works."

echo "⚡ Installing Omni..."

INSTALL_DIR="$HOME/.omni"

# 1. Clone/Update
if [ -d "$INSTALL_DIR" ]; then
    echo "  • Updating..."
    cd "$INSTALL_DIR"
    git pull --quiet
else
    echo "  • Downloading..."
    git clone --quiet https://github.com/AureliusSystemsAI/omni.git "$INSTALL_DIR"
fi

# 2. Setup Venv
echo "  • configuring brain..."
cd "$INSTALL_DIR"
python3 -m venv venv
./venv/bin/pip install -e . --quiet

# 3. The "Just Works" Fix (Symlink)
# Try to write to /usr/local/bin (Standard PATH)
BIN_PATH="/usr/local/bin/omni"

echo "  • Linking binary..."
BIN_PATH="/usr/local/bin/omni"
BIN_DIR="/usr/local/bin"

if [ ! -d "$BIN_DIR" ]; then
    echo "    (Creating $BIN_DIR)"
    if [ -w "/usr/local" ]; then
        mkdir -p "$BIN_DIR"
    else
        sudo mkdir -p "$BIN_DIR"
    fi
fi

if [ -w "$BIN_DIR" ]; then
    # We have write access, just link it
    ln -sf "$INSTALL_DIR/venv/bin/omni" "$BIN_PATH"
else
    # We need sudo
    echo "    (Password required to create 'omni' command)"
    sudo ln -sf "$INSTALL_DIR/venv/bin/omni" "$BIN_PATH"
fi

echo ""
echo "✅ Omni Installed!"
echo "👉 Try it now: omni init"
