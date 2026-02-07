#!/usr/bin/env python3
import os
import sys
import time
import glob
import subprocess
import re
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm

# Omni - The Secure Interface
# Usage: omni run

console = Console()

# Configuration
BASE_MODEL_REPO = "mlx-community/Llama-3.2-3B-Instruct"
LOCAL_MODEL_DIR = os.path.expanduser("~/.omni/models/base-3b")

class OmniAgent:
    def __init__(self):
        self.active_brain = "None"
        self.status = "Idle"
        self.model = None
        self.tokenizer = None
        self.context_files = self.scan_context()
        # Personas are capabilities, not physical downloads (unless finetuned)
        self.personas = [
            "architect", "backend", "frontend", "devops",
            "ios", "android", "flutter", "react-native",
            "unity", "unreal", "shell", "sql", "git"
        ]

    def scan_context(self):
        files = [f for f in os.listdir(".") if os.path.isfile(f) and not f.startswith(".")]
        return len(files)

    def get_installed_brains(self):
        """Return list of physically present models."""
        installed = []
        if os.path.exists(LOCAL_MODEL_DIR):
            installed.append("Base Model (Llama-3.2-3B)")
        
        if os.path.exists("models"):
            for p in glob.glob("models/*-fused"):
                installed.append(os.path.basename(p).replace("-fused", ""))
        return installed

    def splash(self):
        console.clear()
        console.print(Panel.fit(
            "[bold white]OMNI v0.7.0 (Intelligent)[/bold white]\n[dim]The Secure AI Stack[/dim]",
            border_style="green",
            padding=(1, 4)
        ))
        console.print("")

    def dashboard(self):
        table = Table(show_header=True, header_style="bold magenta", expand=True, border_style="dim")
        table.add_column("Active Brain", style="cyan")
        table.add_column("Status", style="green")
        
        brain_label = f"@roe/{self.active_brain}" if self.active_brain != "None" else "Omni (General)"
        table.add_row(brain_label, self.status)
        console.print(table)

    def ensure_model(self):
        if os.path.exists(LOCAL_MODEL_DIR):
            return True
            
        console.print(f"[yellow]⚠️  I need to download my neural weights (3GB) to function.[/yellow]")
        if Confirm.ask(f"Download [bold white]Llama-3.2-3B[/bold white] from Hugging Face?"):
            try:
                from huggingface_hub import snapshot_download
                with console.status("[bold cyan]Downloading...[/bold cyan]"):
                    snapshot_download(repo_id=BASE_MODEL_REPO, local_dir=LOCAL_MODEL_DIR, local_dir_use_symlinks=False)
                console.print("[green]✅ Download Complete.[/green]")
                return True
            except ImportError:
                console.print("[red]❌ Error: huggingface_hub missing. Run install.sh.[/red]")
            except Exception as e:
                console.print(f"[red]❌ Download Failed: {e}[/red]")
        return False

    def load_model_if_needed(self):
        if self.model: return True
        if not self.ensure_model(): return False
        
        with console.status(f"[bold cyan]Loading Neural Network...[/bold cyan]", spinner="arc"):
            try:
                from mlx_lm import load
                self.model, self.tokenizer = load(LOCAL_MODEL_DIR)
                self.status = "Ready"
                return True
            except Exception as e:
                console.print(f"[red]❌ Load Failed: {e}[/red]")
                return False

    def extract_and_run(self, text):
        matches = re.findall(r'```(\w+)\n(.*?)```', text, re.DOTALL)
        if not matches: return

        lang, code = matches[-1]
        ext = "txt"
        if lang in ["python", "py"]: ext = "py"
        elif lang in ["html", "js", "javascript"]: ext = "html"
        elif lang in ["sh", "bash"]: ext = "sh"
        
        filename = f"omni_output.{ext}"
        console.print(f"\n[bold yellow]⚡ Detected {lang} code block.[/bold yellow]")
        
        if Confirm.ask(f"Save and run as [bold white]{filename}[/bold white]?"):
            with open(filename, "w") as f: f.write(code)
            console.print(f"[green]✓ Saved to {filename}[/green]")
            try:
                if ext == "py":
                    res = subprocess.run([sys.executable, filename], capture_output=True, text=True)
                    print(res.stdout)
                    if res.returncode != 0:
                        console.print(f"[red]Error:[/red]\n{res.stderr}")
                        if "ModuleNotFoundError" in res.stderr:
                            mod = res.stderr.split("'")[1]
                            if Confirm.ask(f"[yellow]Install missing '{mod}'?[/yellow]"):
                                subprocess.run([sys.executable, "-m", "pip", "install", mod])
                                subprocess.run([sys.executable, filename])
                elif ext == "html":
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.run([opener, filename])
                elif ext == "sh":
                    subprocess.run(["bash", filename])
            except Exception as e:
                console.print(f"[red]❌ Execution Failed: {e}[/red]")

    def generate(self, user_prompt):
        if not self.load_model_if_needed(): return

        # Intelligent System Prompt
        installed = self.get_installed_brains()
        
        base_prompt = f"""You are Omni, a Secure AI Stack running locally.
Your goal is to help the user build software.
You have access to the following Physical Brains: {', '.join(installed)}.
You can act as the following Personas: {', '.join(self.personas)}.

Current Context:
- User is in a directory with {self.context_files} files.
- You can write code. If you write code, the user can run it immediately.
- If the user asks about system status or brains, answer truthfully based on the 'Physical Brains' list above.
- Do not simulate. Do not hallucinate capabilities you don't have.
- If asked to build something, choose the best persona and WRITE THE CODE.
"""
        
        # Persona Injection
        if self.active_brain != "None":
            base_prompt += f"\nCURRENT PERSONA: You are acting as @roe/{self.active_brain}."

        full_prompt = f"<|start_header_id|>system<|end_header_id|>\n\n{base_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        console.print(f"\n[bold green]Omni:[/bold green]", end=" ")
        
        from mlx_lm import generate
        with console.status("[dim]Processing...[/dim]", spinner="dots"):
            response = generate(self.model, self.tokenizer, prompt=full_prompt, max_tokens=1024, verbose=False)
        
        console.print(Markdown(response))
        self.extract_and_run(response)
        console.print("")

    def chat_loop(self):
        self.splash()
        console.print("[dim]System Ready. I am listening.[/dim]")

        while True:
            user_input = Prompt.ask("\n[bold white]omni[/bold white] [dim]>[/dim]")
            if not user_input: continue
            if user_input.lower() in ["exit", "quit"]: break
            
            # Simple keyword shortcut for menu
            if user_input.lower() == "menu":
                console.print(f"[cyan]Personas:[/cyan] {', '.join(self.personas)}")
                continue

            # Auto-Persona Switcher (Simple Heuristic to help the LLM)
            # We allow the LLM to handle most things, but setting active_brain helps context.
            if "flutter" in user_input.lower(): self.active_brain = "flutter"
            elif "react" in user_input.lower() or "web" in user_input.lower(): self.active_brain = "frontend"
            elif "python" in user_input.lower() or "backend" in user_input.lower(): self.active_brain = "backend"
            elif "game" in user_input.lower(): self.active_brain = "frontend" # Default simple game
            
            self.generate(user_input)

    def run_cli(self):
        self.chat_loop()

def main():
    agent = OmniAgent()
    agent.run_cli()

if __name__ == "__main__":
    main()
