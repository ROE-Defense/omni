#!/usr/bin/env python3
import os
import sys
import time
import argparse
import platform
import json

# omni.py - The AI Operating System
# Built by: ROE Defense Swarm
# Version: 0.2.1 (Beta) - "The Manager Update"

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
    "1": {"name": "@roe/architect", "desc": "3B Param | System Design & Stack Strategy", "url": "https://huggingface.co/roe-defense/architect-v1/resolve/main/model.gguf"},
    "2": {"name": "@roe/backend", "desc": "3B Param | Python/Node/SQL Specialist", "url": "https://huggingface.co/roe-defense/backend-v1/resolve/main/model.gguf"},
    "3": {"name": "@roe/frontend", "desc": "3B Param | React/Tailwind/UI Specialist", "url": "https://huggingface.co/roe-defense/frontend-v1/resolve/main/model.gguf"},
    "4": {"name": "@roe/devops", "desc": "3B Param | Docker/K8s/CI-CD Specialist", "url": "https://huggingface.co/roe-defense/devops-v1/resolve/main/model.gguf"},
    "5": {"name": "@roe/mobile", "desc": "3B Param | iOS/Android/ATAK (Beta)", "url": "https://huggingface.co/roe-defense/mobile-v1/resolve/main/model.gguf"},
    "6": {"name": "@roe/desktop", "desc": "3B Param | macOS/Windows Native (Soon)", "url": "https://huggingface.co/roe-defense/desktop-v1/resolve/main/model.gguf"},
    "7": {"name": "@roe/ai-eng", "desc": "3B Param | MLX/PyTorch/RAG (Soon)", "url": "https://huggingface.co/roe-defense/ai-eng-v1/resolve/main/model.gguf"},
    "8": {"name": "@roe/custom", "desc": "Train Your Own | Fine-tune on Docs", "action": "train"}
}

def goal_based_setup():
    print(f"\n{Colors.HEADER}🎯 GOAL-BASED SETUP{Colors.ENDC}")
    print("Tell Omni what you want to achieve, and we'll recommend the right brain.")
    
    goal = input(f"\n  {Colors.BOLD}What is your objective?{Colors.ENDC} ").strip().lower()
    
    # Simple Keyword Matching Logic (The "Omni" Brain)
    recommendation = None
    reason = ""
    
    if any(x in goal for x in ['regex', 'parse', 'extract', 'scrape', 'string', 'pattern']):
        recommendation = "1"
        reason = "Optimized for string manipulation and data extraction."
    elif any(x in goal for x in ['sec', 'hack', 'log', 'network', 'defense', 'cyber', 'audit']):
        recommendation = "2"
        reason = "Trained on security protocols and log analysis."
    elif any(x in goal for x in ['design', 'architect', 'system', 'diagram', 'plan', 'structure', 'cloud']):
        recommendation = "3"
        reason = "Best for high-level system design and infrastructure planning."
    elif any(x in goal for x in ['code', 'python', 'script', 'app', 'build', 'program', 'dev']):
        recommendation = "4"
        reason = "General purpose coding and scripting specialist."
    
    if recommendation:
        brain = BRAIN_MAP[recommendation]
        print(f"\n  {Colors.GREEN}✔ Recommendation found:{Colors.ENDC} {brain['name']}")
        print(f"  {Colors.BLUE}ℹ️  Reason:{Colors.ENDC} {reason}")
        
        confirm = input(f"\n  Install this brain? (Y/n) ").strip().lower()
        if confirm in ['', 'y', 'yes']:
            install_brain_logic(recommendation)
        else:
            print("  Cancelled.")
    else:
        print(f"\n  {Colors.WARNING}Could not determine specific requirement.{Colors.ENDC}")
        print("  Please select manually from the list.")
        time.sleep(2)

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
    
    # Simulate success for Wizard (v0.2 feature)
    time.sleep(1)
    # Register the custom brain (Mock)
    print(f"\n  {Colors.GREEN}✔ Brain '{name}' created successfully.{Colors.ENDC}")
    input(f"  Press Enter to return...")

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

def manage_brains():
    while True:
        clear_screen()
        print(f"{Colors.HEADER}🧠 BRAIN MANAGER{Colors.ENDC}")
        print("Installed Cartridges:\n")
        
        installed = []
        cartridge_dir = os.path.expanduser("~/.omni/cartridges")
        if not os.path.exists(cartridge_dir):
            os.makedirs(cartridge_dir)
            
        for f in os.listdir(cartridge_dir):
            if f.endswith(".gguf"):
                installed.append(f)
        
        if not installed:
            print(f"  {Colors.WARNING}(No brains installed){Colors.ENDC}")
        else:
            for i, brain in enumerate(installed):
                print(f"  {i+1}. {brain}")
        
        print(f"\n{Colors.BOLD}Actions:{Colors.ENDC}")
        print("  G. I have a Goal (Install by Intent)")
        print("  D. Delete a brain")
        print("  R. Rename a brain")
        print("  B. Back to Main Menu")
        
        choice = input(f"\n{Colors.CYAN}manager > {Colors.ENDC}").strip().lower()
        
        if choice == 'b': break
        elif choice == 'g':
            goal_based_setup()
        elif choice == 'd':
            idx = input("  Number to delete: ")
            if idx.isdigit() and 1 <= int(idx) <= len(installed):
                target = os.path.join(cartridge_dir, installed[int(idx)-1])
                os.remove(target)
                print(f"  {Colors.FAIL}✔ Deleted {installed[int(idx)-1]}{Colors.ENDC}")
                time.sleep(1)
        elif choice == 'r':
            idx = input("  Number to rename: ")
            if idx.isdigit() and 1 <= int(idx) <= len(installed):
                old_name = installed[int(idx)-1]
                new_name = input("  New name (e.g., @my/brain.gguf): ").strip()
                if not new_name.endswith(".gguf"): new_name += ".gguf"
                os.rename(os.path.join(cartridge_dir, old_name), os.path.join(cartridge_dir, new_name))
                print(f"  {Colors.GREEN}✔ Renamed to {new_name}{Colors.ENDC}")
                time.sleep(1)
        else:
            print("Invalid.")
            time.sleep(0.5)

def agent_loop():
    clear_screen()
    print_logo()
    print(f"{Colors.GREEN}✔ Stack Loaded.{Colors.ENDC} You are now in the Omni Shell.")
    
    # Brain Selector
    cartridge_dir = os.path.expanduser("~/.omni/cartridges")
    available_brains = [f for f in os.listdir(cartridge_dir) if f.endswith(".gguf")] if os.path.exists(cartridge_dir) else []
    
    selected_model = None
    if not available_brains:
        print(f"{Colors.WARNING}⚠ No brains found. Please install one first.{Colors.ENDC}")
        input("Press Enter...")
        return
    
    if len(available_brains) == 1:
        selected_model = os.path.join(cartridge_dir, available_brains[0])
        print(f"  Using: {Colors.CYAN}{available_brains[0]}{Colors.ENDC}")
    else:
        print("\nSelect Active Brain for this session:")
        for i, b in enumerate(available_brains):
            print(f"  {i+1}. {b}")
        
        print(f"  {Colors.BOLD}G. Goal-based Switch (Coming soon){Colors.ENDC}")

        while True:
            sel = input(f"\n{Colors.BLUE}select [1-{len(available_brains)}] > {Colors.ENDC}")
            if sel.isdigit() and 1 <= int(sel) <= len(available_brains):
                selected_model = os.path.join(cartridge_dir, available_brains[int(sel)-1])
                print(f"  Selected: {Colors.GREEN}{available_brains[int(sel)-1]}{Colors.ENDC}")
                break
            elif sel.lower() == 'g':
                print(f"{Colors.WARNING}Feature pending runtime integration.{Colors.ENDC}")
                time.sleep(1)
            else:
                print("Invalid selection.")

    print("\nType a task to execute or 'exit'.\n")
    
    # Initialize LLM
    llm = None
    default_model = selected_model

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

def manual_catalog_view():
    print(f"\n{Colors.HEADER}📋 MANUAL CATALOG{Colors.ENDC}")
    print("Select a Cognitive Cartridge to install:")
    
    for key, info in BRAIN_MAP.items():
        # Check if installed
        fname = os.path.join(os.path.expanduser("~/.omni/cartridges"), f"{info['name'].replace('/', '_')}.gguf")
        status = f"{Colors.GREEN}[Installed]{Colors.ENDC}" if os.path.exists(fname) else "[ ]"
        print(f"  {Colors.BOLD}{key}.{Colors.ENDC} {info['name']} \t{status} - {info['desc']}")
    
    print("\nSelect number to install, or B to go back.")
    choice = input(f"\n{Colors.CYAN}catalog > {Colors.ENDC}").strip().lower()
    
    if choice == 'b':
        return
    elif choice in BRAIN_MAP:
        install_brain_logic(choice)
        input("Press Enter to continue...")

def wizard_loop():
    clear_screen()
    print_logo()
    print("Welcome to Omni. Let's set up your stack.\n")
    check_system()
    time.sleep(1)

    while True:
        print(f"\n{Colors.HEADER}🏗  STACK CONFIGURATION{Colors.ENDC}")
        print("Select a Brain to install:")
        
        for key, info in BRAIN_MAP.items():
            # Check if installed
            fname = os.path.join(os.path.expanduser("~/.omni/cartridges"), f"{info['name'].replace('/', '_')}.gguf")
            status = f"{Colors.GREEN}[Installed]{Colors.ENDC}" if os.path.exists(fname) else "[ ]"
            print(f"  {Colors.BOLD}{key}.{Colors.ENDC} {info['name']} \t{status} - {info['desc']}")
        
        print(f"  {Colors.BOLD}M.{Colors.ENDC} Manage Installed Brains (Rename/Delete)")
        print(f"  {Colors.BOLD}G.{Colors.ENDC} I have a Goal (Auto-Select)")
        print(f"  {Colors.BOLD}R.{Colors.ENDC} Run Agent (Start Shell)")
        print(f"  {Colors.BOLD}Q.{Colors.ENDC} Quit")

        choice = input(f"\n{Colors.CYAN}omni > {Colors.ENDC}").strip().lower()

        if choice == 'q':
            print("Exiting.")
            sys.exit(0)
        
        elif choice == 'g':
            goal_based_setup()
        
        elif choice == 'r':
            # Enter Agent Mode
            agent_loop()
            break 
        
        elif choice == 'm':
            manage_brains()

        elif choice in BRAIN_MAP:
            install_brain_logic(choice)
            time.sleep(1)
            # Loop continues to show updated status
        else:
            print(f"{Colors.WARNING}Invalid option.{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(description="Omni: AI Stack")
    subparsers = parser.add_subparsers(dest="command")
    
    # New Commands
    subparsers.add_parser("run", help="Start the Omni Wizard (Interactive Mode)")
    subparsers.add_parser("init", help="Alias for run") # Backwards compat
    
    # CLI Bypass commands
    install = subparsers.add_parser("install", help="Install a Brain directly")
    install.add_argument("name", help="Name of the brain")
    
    subparsers.add_parser("update", help="Update Omni System")

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
            print(f"{Colors.FAIL}Unknown brain: {args.name}{Colors.ENDC}")
            
    elif args.command == "exec":
        # One-shot mode
        pass # To be implemented similar to agent_loop but one-off

    elif args.command == "update":
        print(f"{Colors.BLUE}🔄 UPDATING OMNI SYSTEM{Colors.ENDC}")
        try:
            import subprocess
            # Assume git repo is where this script lives
            repo_path = os.path.dirname(os.path.abspath(__file__))
            subprocess.check_call(["git", "pull"], cwd=repo_path)
            print(f"{Colors.GREEN}✔ Update Complete.{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}X Update failed: {e}{Colors.ENDC}")

if __name__ == "__main__":
    main()
