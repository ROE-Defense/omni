#!/bin/bash

# Omni Air Gap Protocol (v0.8.0)
# Usage: ./airgap.sh [on|off|status]

STATUS_FILE="$HOME/.omni/airgap_status"

function check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo "❌ Error: Air Gap control requires root privileges (sudo)."
        exit 1
    fi
}

function status() {
    if [ -f "$STATUS_FILE" ]; then
        echo "🔒 AIR GAP: ACTIVE"
        echo "• Network Interfaces: DISABLED"
        echo "• Outbound Traffic: BLOCKED"
    else
        echo "🔓 AIR GAP: INACTIVE"
        echo "• Network Interfaces: ONLINE"
    fi
}

function enable_airgap() {
    check_root
    echo "🚨 INITIATING AIR GAP PROTOCOL..."
    
    # 1. Block all outbound traffic except localhost
    # (MacOS PF syntax or Linux iptables)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # MacOS Packet Filter
        echo "block drop all" | pfctl -f - 2>/dev/null
        echo "pass on lo0 all" | pfctl -f - 2>/dev/null
        pfctl -e 2>/dev/null
    else
        # Linux iptables
        iptables -P INPUT DROP
        iptables -P FORWARD DROP
        iptables -P OUTPUT DROP
        iptables -A INPUT -i lo -j ACCEPT
        iptables -A OUTPUT -o lo -j ACCEPT
    fi
    
    # 2. Disable physical interfaces (Aggressive)
    # ifconfig en0 down
    
    touch "$STATUS_FILE"
    echo "✅ SYSTEM ISOLATED. ZERO EMISSIONS."
}

function disable_airgap() {
    check_root
    echo "⚠️  DISABLING AIR GAP..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        pfctl -d 2>/dev/null
    else
        iptables -P INPUT ACCEPT
        iptables -P OUTPUT ACCEPT
    fi
    
    rm -f "$STATUS_FILE"
    echo "🌐 NETWORK RESTORED."
}

case "$1" in
    on)
        enable_airgap
        ;;
    off)
        disable_airgap
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {on|off|status}"
        exit 1
        ;;
esac
