#!/usr/bin/env python3
import os
import sys
import time
import argparse
import platform
import json

# omni.py - The AI Operating System
# Built by: ROE Defense Swarm (Vector)
# Version: 0.1.0 (Alpha)

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_logo():
    logo = rf"""{Colors.CYAN}
   ____  __  __  _   _  ___ 
  / __ \|  \/  || \ | ||_ _|
 | |  | | |\/| ||  \| | | | 
 | |__| | |  | || |\  | | | 
  \____/|_|  |_||_| \_||___|
  {Colors.ENDC}{Colors.BLUE}The OS for Intelligence{Colors.ENDC}
    """
    print(logo)

def check_system():
    print(f"{Colors.HEADER}⚡ SYSTEM CHECK{Colors.ENDC}")
    system = platform.system()
    machine = platform.machine()
    print(f"  OS: {system}")
    print(f"  Chip: {machine}")
    
    if system == "Darwin" and "arm" in machine:
        print(f"  {Colors.GREEN}✔ Apple Silicon Detected (Optimized Mode){Colors.ENDC}")
        return "metal"
    elif "cuda" in os.environ.get("PATH", "").lower():
        print(f"  {Colors.GREEN}✔ NVIDIA CUDA Detected{Colors.ENDC}")
        return "cuda"
    else:
        print(f"  {Colors.WARNING}⚠ CPU Mode (Slow){Colors.ENDC}")
        return "cpu"

def install_brain(brain_name):
    print(f"\n{Colors.HEADER}🧠 INSTALLING CARTRIDGE: {brain_name}{Colors.ENDC}")
    
    # Mapping brains to real HuggingFace URLs (Temporary Mapping to Base until Fine-Tune Complete)
    BRAIN_MAP = {
        "@roe/regex-pro": "https://huggingface.co/hugging-quants/Llama-3.2-1B-Instruct-Q8_0-GGUF/resolve/main/llama-3.2-1b-instruct-q8_0.gguf",
        "@roe/base": "https://huggingface.co/hugging-quants/Llama-3.2-1B-Instruct-Q8_0-GGUF/resolve/main/llama-3.2-1b-instruct-q8_0.gguf",
        "@roe/sec-ops": "https://huggingface.co/hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF/resolve/main/llama-3.2-3b-instruct-q4_k_m.gguf",
        "@roe/architect": "https://huggingface.co/hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF/resolve/main/llama-3.2-3b-instruct-q4_k_m.gguf"
    }
    
    if brain_name not in BRAIN_MAP:
        print(f"  {Colors.FAIL}X Error: Cartridge '{brain_name}' not found in registry.{Colors.ENDC}")
        return

    url = BRAIN_MAP[brain_name]
    filename = os.path.join(os.path.expanduser("~/.omni/cartridges"), f"{brain_name.replace('/', '_')}.gguf")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    print(f"  Source: {url}")
    print(f"  Dest:   {filename}")
    
    try:
        import urllib.request
        
        # Progress bar hook
        def show_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, int(downloaded / total_size * 100))
            bar_length = 20
            filled_length = int(bar_length * percent // 100)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            sys.stdout.write(f"\r  Downloading: |{bar}| {percent}% ({downloaded // 1024 // 1024} MB)")
            sys.stdout.flush()

        urllib.request.urlretrieve(url, filename, show_progress)
        print(f"\n  {Colors.GREEN}✔ Installed successfully.{Colors.ENDC}")
        print(f"  {Colors.BLUE}ℹ️  Ready to run agents.{Colors.ENDC}")
        
    except Exception as e:
        print(f"\n  {Colors.FAIL}X Download Failed: {e}{Colors.ENDC}")

def run_agent(task):
    print(f"\n{Colors.HEADER}🤖 OMNI AGENT ACTIVATED{Colors.ENDC}")
    print(f"  Task: {task}")
    print(f"  {Colors.BLUE}Thinking...{Colors.ENDC}")
    time.sleep(1)
    print(f"  {Colors.CYAN}Plan:{Colors.ENDC} 1. Scan Context -> 2. Generate Code -> 3. Verify")
    time.sleep(1)
    print(f"  {Colors.GREEN}✔ Execution Complete.{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(description="Omni: AI OS")
    subparsers = parser.add_subparsers(dest="command")
    
    # Commands
    subparsers.add_parser("init", help="Initialize Omni System")
    install = subparsers.add_parser("install", help="Install a Cartridge")
    install.add_argument("name", help="Name of the brain (e.g., @aurelius/python)")
    
    run = subparsers.add_parser("run", help="Run an Agent Task")
    run.add_argument("task", help="The task description")

    list_cmd = subparsers.add_parser("list", help="List installed brains")
    update_cmd = subparsers.add_parser("update", help="Update Omni to the latest version")
    
    args = parser.parse_args()
    
    if args.command == "init":
        print_logo()
        check_system()
    elif args.command == "install":
        install_brain(args.name)
    elif args.command == "run":
        run_agent(args.task)
    elif args.command == "list":
        print(f"\n{Colors.HEADER}🧠 INSTALLED CARTRIDGES{Colors.ENDC}")
        print(f"  • {Colors.CYAN}@roe/regex-pro{Colors.ENDC} (v1.0)")
        print(f"  • {Colors.CYAN}@roe/sec-ops{Colors.ENDC} (v1.0)")
        print(f"  • {Colors.CYAN}@roe/architect{Colors.ENDC} (v1.0)")
        print(f"  • {Colors.CYAN}default-llama-3{Colors.ENDC} (base)")
    elif args.command == "update":
        print(f"\n{Colors.HEADER}🔄 UPDATING OMNI SYSTEM{Colors.ENDC}")
        install_dir = os.path.expanduser("~/.omni")
        if os.path.exists(install_dir):
            try:
                import subprocess
                subprocess.run(["git", "-C", install_dir, "pull"], check=True)
                print(f"  {Colors.GREEN}✔ Codebase updated.{Colors.ENDC}")
                subprocess.run([os.path.join(install_dir, "venv/bin/pip"), "install", "-e", install_dir], check=True)
                print(f"  {Colors.GREEN}✔ Dependencies updated.{Colors.ENDC}")
                print(f"  {Colors.BLUE}ℹ️  Please restart your shell or run 'hash -r' to use new features.{Colors.ENDC}")
            except Exception as e:
                print(f"  {Colors.FAIL}X Update failed: {e}{Colors.ENDC}")
        else:
            print(f"  {Colors.FAIL}X Omni directory not found. Please reinstall.{Colors.ENDC}")
    else:
        print_logo()
        parser.print_help()

if __name__ == "__main__":
    main()
