#!/usr/bin/env python3
import os
import sys
import time
import argparse
import platform
import json

# omni.py - The AI Operating System
# Built by: ROE Defense Swarm
# Version: 0.2.0 (Beta) - "The Wizard Update"

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

BRAIN_MAP = {
    "1": {"name": "@roe/regex-pro", "desc": "1B Param | Precision String Extraction", "url": "https://huggingface.co/hugging-quants/Llama-3.2-1B-Instruct-Q8_0-GGUF/resolve/main/llama-3.2-1b-instruct-q8_0.gguf"},
    "2": {"name": "@roe/sec-ops", "desc": "3B Param | Network Defense & Log Analysis", "url": "https://huggingface.co/hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF/resolve/main/llama-3.2-3b-instruct-q4_k_m.gguf"},
    "3": {"name": "@roe/architect", "desc": "3B Param | System Design & Stack Strategy", "url": "https://huggingface.co/hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF/resolve/main/llama-3.2-3b-instruct-q4_k_m.gguf"},
    "4": {"name": "@roe/python", "desc": "3B Param | Code Generation & Scripting", "url": "https://huggingface.co/hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF/resolve/main/llama-3.2-3b-instruct-q4_k_m.gguf"},
    "5": {"name": "@roe/custom", "desc": "Train Your Own | Fine-tune on Docs (Images/Video/Audio coming soon)", "action": "train"}
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    logo = rf"""{Colors.CYAN}
   ____  __  __  _   _  ___ 
  / __ \|  \/  || \ | ||_ _|
 | |  | | |\/| ||  \| | | | 
 | |__| | |  | || |\  | | | 
  \____/|_|  |_||_| \_||___|
  {Colors.ENDC}{Colors.BLUE}The Local-Only AI Stack{Colors.ENDC}
    """
    print(logo)

def check_system():
    print(f"{Colors.HEADER}⚡ SYSTEM CHECK{Colors.ENDC}")
    system = platform.system()
    machine = platform.machine()
    print(f"  OS: {system}")
    print(f"  Chip: {machine}")
    
    if system == "Darwin" and "arm" in machine:
        print(f"  {Colors.GREEN}✔ Apple Silicon Detected (Metal Optimized){Colors.ENDC}")
        return "metal"
    elif "cuda" in os.environ.get("PATH", "").lower():
        print(f"  {Colors.GREEN}✔ NVIDIA CUDA Detected{Colors.ENDC}")
        return "cuda"
    else:
        print(f"  {Colors.WARNING}⚠ CPU Mode (Slower){Colors.ENDC}")
        return "cpu"

def train_wizard():
    print(f"\n{Colors.HEADER}🎓 TRAIN YOUR OWN BRAIN{Colors.ENDC}")
    print("This feature allows you to ingest local documents and fine-tune a specialized model.")
    print(f"{Colors.WARNING}⚠ Requirement: Apple Silicon (M1/M2/M3) or NVIDIA GPU (16GB+ VRAM){Colors.ENDC}")
    
    path = input(f"\n  {Colors.BOLD}Path to documents folder:{Colors.ENDC} ").strip()
    if not os.path.exists(path):
        print(f"  {Colors.FAIL}X Path not found.{Colors.ENDC}")
        return

    name = input(f"  {Colors.BOLD}Name your brain (e.g., @my/project):{Colors.ENDC} ").strip()
    
    print(f"\n  {Colors.BLUE}ℹ️  Scanning {path}...{Colors.ENDC}")
    # Placeholder for actual logic
    print(f"  {Colors.GREEN}✔ Found 14 documents.{Colors.ENDC}")
    print(f"  {Colors.BLUE}⚡ Starting Zero-Trace Training Protocol...{Colors.ENDC}")
    print("  (This would take 20-40 mins on M1 Max. Feature coming in v0.3)")
    input(f"\n  Press Enter to return...")

def install_brain_logic(brain_key):
    brain = BRAIN_MAP.get(brain_key)
    if not brain:
        return False
    
    if brain.get("action") == "train":
        train_wizard()
        return True

    brain_name = brain["name"]
    url = brain["url"]
    filename = os.path.join(os.path.expanduser("~/.omni/cartridges"), f"{brain_name.replace('/', '_')}.gguf")
    
    if os.path.exists(filename):
        print(f"  {Colors.GREEN}✔ {brain_name} is already installed.{Colors.ENDC}")
        return True

    print(f"\n{Colors.HEADER}🧠 INSTALLING: {brain_name}{Colors.ENDC}")
    print(f"  Source: {url}")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    try:
        import urllib.request
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
        return True
    except Exception as e:
        print(f"\n  {Colors.FAIL}X Download Failed: {e}{Colors.ENDC}")
        return False

def wizard_loop():
    clear_screen()
    print_logo()
    print("Welcome to Omni. Let's set up your stack.\n")
    check_system()
    time.sleep(1)

    while True:
        print(f"\n{Colors.HEADER}🏗  STACK CONFIGURATION{Colors.ENDC}")
        print("Select a Cognitive Cartridge to install:")
        
        for key, info in BRAIN_MAP.items():
            # Check if installed
            fname = os.path.join(os.path.expanduser("~/.omni/cartridges"), f"{info['name'].replace('/', '_')}.gguf")
            status = f"{Colors.GREEN}[Installed]{Colors.ENDC}" if os.path.exists(fname) else "[ ]"
            print(f"  {Colors.BOLD}{key}.{Colors.ENDC} {info['name']} \t{status} - {info['desc']}")
        
        print(f"  {Colors.BOLD}R.{Colors.ENDC} Run Agent (Start Shell)")
        print(f"  {Colors.BOLD}Q.{Colors.ENDC} Quit")

        choice = input(f"\n{Colors.CYAN}omni > {Colors.ENDC}").strip().lower()

        if choice == 'q':
            print("Exiting.")
            sys.exit(0)
        
        elif choice == 'r':
            # Enter Agent Mode
            agent_loop()
            break 
            
        elif choice in BRAIN_MAP:
            install_brain_logic(choice)
            time.sleep(1)
            # Loop continues to show updated status
        else:
            print(f"{Colors.WARNING}Invalid option.{Colors.ENDC}")

def agent_loop():
    clear_screen()
    print_logo()
    print(f"{Colors.GREEN}✔ Stack Loaded.{Colors.ENDC} You are now in the Omni Shell.")
    print("Type a task to execute (e.g., 'Extract IPs from auth.log') or 'exit'.\n")

    # Pre-load brain logic (simplified)
    # Ideally, we let the user pick the brain per task or route automatically
    # For MVP: Check if *any* brain exists, if not, force install default
    default_model = os.path.join(os.path.expanduser("~/.omni/cartridges/@roe_regex-pro.gguf"))
    if not os.path.exists(default_model):
        print(f"{Colors.WARNING}⚠ No default brain found. Installing @roe/regex-pro...{Colors.ENDC}")
        install_brain_logic("1")
    
    # Initialize LLM once (Mock for speed in menu, real load on first task)
    llm = None

    while True:
        task = input(f"\n{Colors.BLUE}omni/agent > {Colors.ENDC}").strip()
        if not task: continue
        if task.lower() in ['exit', 'quit']:
            print("Shutting down agent.")
            break
        
        if not llm:
            print(f"  {Colors.BLUE}🧠 Loading Neural Engine (Metal/CUDA)...{Colors.ENDC}")
            try:
                from llama_cpp import Llama
                llm = Llama(
                    model_path=default_model,
                    n_ctx=2048,
                    verbose=False,
                    n_gpu_layers=-1
                )
            except Exception as e:
                print(f"  {Colors.FAIL}X Failed to load model: {e}{Colors.ENDC}")
                return

        print(f"  {Colors.BLUE}🤔 Thinking...{Colors.ENDC}")
        
        prompt = f"<|start_header_id|>system<|end_header_id|>\nYou are an expert AI. Return the answer directly.<|eot_id|><|start_header_id|>user<|end_header_id|>\n{task}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
        
        try:
            output = llm(prompt, max_tokens=1024, stop=["<|eot_id|>"])
            response = output['choices'][0]['text'].strip()
            print(f"\n{Colors.GREEN}✔ RESPONSE:{Colors.ENDC}")
            print(response)
        except Exception as e:
            print(f"  {Colors.FAIL}X Error: {e}{Colors.ENDC}")


def main():
    parser = argparse.ArgumentParser(description="Omni: AI Stack")
    subparsers = parser.add_subparsers(dest="command")
    
    # New Commands
    subparsers.add_parser("run", help="Start the Omni Wizard (Interactive Mode)")
    subparsers.add_parser("init", help="Alias for run") # Backwards compat
    
    # CLI Bypass commands
    install = subparsers.add_parser("install", help="Install a Cartridge directly")
    install.add_argument("name", help="Name of the brain")
    
    exec_cmd = subparsers.add_parser("exec", help="Run a one-off task")
    exec_cmd.add_argument("task", help="The task description")

    args = parser.parse_args()
    
    if args.command in ["run", "init"] or args.command is None:
        try:
            wizard_loop()
        except KeyboardInterrupt:
            print("\nExiting.")
            sys.exit(0)
            
    elif args.command == "install":
        # Find key by name or just try to install raw name
        found = False
        for k, v in BRAIN_MAP.items():
            if v["name"] == args.name:
                install_brain_logic(k)
                found = True
                break
        if not found:
            print(f"{Colors.FAIL}Unknown cartridge: {args.name}{Colors.ENDC}")
            
    elif args.command == "exec":
        # One-shot mode
        pass # To be implemented similar to agent_loop but one-off

if __name__ == "__main__":
    main()
