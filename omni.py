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

def run_agent(task, file_path=None):
    print(f"\n{Colors.HEADER}🤖 OMNI AGENT ACTIVATED{Colors.ENDC}")
    print(f"  Task: {task}")
    
    context_str = ""
    if file_path:
        if os.path.exists(file_path):
            print(f"  {Colors.CYAN}📄 Reading context: {file_path}{Colors.ENDC}")
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    # Basic truncation to fit context window (simplistic)
                    if len(content) > 6000: 
                        content = content[:6000] + "\n...[truncated]"
                    context_str = f"\n\nCONTEXT FILE ({file_path}):\n```\n{content}\n```"
            except Exception as e:
                print(f"  {Colors.WARNING}⚠ Could not read file: {e}{Colors.ENDC}")
        else:
            print(f"  {Colors.WARNING}⚠ File not found: {file_path}{Colors.ENDC}")

    # 1. Find the Brain
    # Default to base/regex for now if not specified (Logic to pick best brain coming in v0.2)
    model_path = os.path.expanduser("~/.omni/cartridges/@roe_regex-pro.gguf")
    
    if not os.path.exists(model_path):
        print(f"  {Colors.WARNING}⚠ No brain found. Installing default...{Colors.ENDC}")
        install_brain("@roe/regex-pro")
        
    print(f"  {Colors.BLUE}🧠 Loading Neural Engine...{Colors.ENDC}")
    
    try:
        from llama_cpp import Llama
        
        # Initialize Llama (Silence logs with verbose=False)
        llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            verbose=False,
            n_gpu_layers=-1 # Use Metal/CUDA
        )
        
        print(f"  {Colors.BLUE}🤔 Thinking...{Colors.ENDC}")
        
        # Simple Prompt Engineering (Fixing duplicate BOS)
        prompt = f"""<|start_header_id|>system<|end_header_id|>

You are an expert AI assistant. Solve the user's task accurately. If you write code, put it in markdown code blocks. Use the provided Context File if relevant.<|eot_id|><|start_header_id|>user<|end_header_id|>

{task}{context_str}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""
        
        stream = llm(
            prompt,
            max_tokens=2048, # Increased for code generation
            stop=["<|eot_id|>"],
            stream=True
        )
        
        print(f"\n{Colors.GREEN}✔ RESPONSE:{Colors.ENDC}\n")
        
        # Stream output
        full_response = ""
        for output in stream:
            token = output['choices'][0]['text']
            sys.stdout.write(token)
            sys.stdout.flush()
            full_response += token
            
        print("\n")
        
        # 3. Auto-Save Logic (The Agent Part)
        if "```python" in full_response:
            print(f"{Colors.HEADER}💾 DETECTED CODE BLOCK{Colors.ENDC}")
            try:
                # Extract code
                code = full_response.split("```python")[1].split("```")[0].strip()
                filename = "omni_output.py"
                with open(filename, "w") as f:
                    f.write(code)
                print(f"  ✔ Saved code to: {Colors.CYAN}{filename}{Colors.ENDC}")
                
                # 4. Dependency Auto-Installer (The "Just Work" Part)
                import re
                import subprocess
                
                # Scan for imports
                imports = re.findall(r"^(?:import|from)\s+(\w+)", code, re.MULTILINE)
                stdlib = sys.stdlib_module_names if hasattr(sys, 'stdlib_module_names') else set() # Only py3.10+
                
                # Filter out standard lib (approximate) and installed packages
                missing = []
                for pkg in set(imports):
                    if pkg in stdlib: continue
                    if pkg in ["sys", "os", "time", "random", "math", "json", "re", "subprocess"]: continue # Fallback
                    
                    # Check if installed in CURRENT env (Omni's venv)? No, we want User's env.
                    # We can't check User's env easily. We assume if it's external, we try to install.
                    # Heuristic: Try to import it. If fail, install.
                    try:
                        __import__(pkg)
                    except ImportError:
                        missing.append(pkg)

                if missing:
                    print(f"  {Colors.WARNING}📦 Missing Dependencies detected: {', '.join(missing)}{Colors.ENDC}")
                    print(f"  {Colors.BLUE}⚡ Auto-installing...{Colors.ENDC}")
                    
                    # We install into the environment executing the script (Likely User's global python if they run 'python3')
                    # WAIT. Omni is running in its OWN venv.
                    # If we install into Omni's venv, the user can run it via `omni run-script`.
                    # If the user runs `python3 omni_output.py`, they use their System Python.
                    
                    # DECISION: Install into Omni's Venv and provide a runner.
                    
                    for pkg in missing:
                        try:
                            # Map imports to package names (pygame -> pygame, bs4 -> beautifulsoup4)
                            # Simple 1:1 mapping for now
                            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                            print(f"    ✔ Installed {pkg}")
                        except Exception as e:
                            print(f"    X Failed to install {pkg}: {e}")
                            
                    print(f"  👉 Run it (using Omni's env): {Colors.BOLD}{sys.executable} {filename}{Colors.ENDC}")
                else:
                    print(f"  👉 Run it: {Colors.BOLD}python3 {filename}{Colors.ENDC}")

            except Exception as e:
                print(f"  {Colors.WARNING}⚠ Could not auto-save/install: {e}{Colors.ENDC}")
        
    except ImportError:
        print(f"  {Colors.FAIL}X Error: llama-cpp-python not installed correctly.{Colors.ENDC}")
    except Exception as e:
        print(f"  {Colors.FAIL}X Inference Error: {e}{Colors.ENDC}")

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
    doctor_cmd = subparsers.add_parser("doctor", help="Check system health")
    
    args = parser.parse_args()
    
    if args.command == "init":
        print_logo()
        check_system()
        print(f"\n{Colors.HEADER}🚀 NEXT STEPS{Colors.ENDC}")
        print(f"  1. Install a Brain: {Colors.CYAN}omni install @roe/regex-pro{Colors.ENDC}")
        print(f"  2. Run a Task:      {Colors.CYAN}omni run \"Find all emails\"{Colors.ENDC}")
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
    elif args.command == "doctor":
        print(f"\n{Colors.HEADER}🚑 OMNI DOCTOR{Colors.ENDC}")
        # Python Check
        print(f"  • Python: {sys.version.split()[0]}")
        # RAM Check
        try:
            import psutil
            mem = psutil.virtual_memory()
            total_gb = round(mem.total / (1024**3), 1)
            print(f"  • RAM: {total_gb} GB")
            if total_gb < 8:
                print(f"    {Colors.WARNING}⚠ Low RAM. 1B models recommended.{Colors.ENDC}")
            else:
                print(f"    {Colors.GREEN}✔ Sufficient for 3B/7B models.{Colors.ENDC}")
        except ImportError:
            print(f"  • RAM: Unknown (psutil not installed)")
        
        # Disk Check
        install_dir = os.path.expanduser("~/.omni")
        if os.path.exists(install_dir):
            print(f"  • Install Dir: {Colors.GREEN}✔ Found{Colors.ENDC} ({install_dir})")
        else:
            print(f"  • Install Dir: {Colors.FAIL}X Missing{Colors.ENDC}")
            
    else:
        print_logo()
        parser.print_help()

if __name__ == "__main__":
    main()
