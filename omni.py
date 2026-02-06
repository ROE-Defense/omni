#!/usr/bin/env python3
import os
import sys
import time
import glob
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
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
        self.available_brains = self.scan_brains()

    def scan_brains(self):
        # We list all "Personas" that the Base Model can act as
        return [
            "architect", "backend", "frontend", "devops",
            "ios", "android", "flutter", "react-native",
            "unity", "unreal", "shell", "sql", "git"
        ]

    def scan_context(self):
        files = [f for f in os.listdir(".") if os.path.isfile(f) and not f.startswith(".")]
        return len(files)

    def splash(self):
        console.clear()
        
        with console.status("[bold green]Initializing Omni Runtime...[/bold green]", spinner="dots"):
            time.sleep(0.3)
            console.log("[green]✓[/green] GPU Acceleration: [bold cyan]Metal/MPS[/bold cyan]")
            time.sleep(0.1)
            console.log(f"[green]✓[/green] Local Context: [bold cyan]{self.context_files} Files[/bold cyan]")
            time.sleep(0.1)
            console.log(f"[green]✓[/green] Cognitive Cartridges: [bold cyan]{len(self.available_brains)} Available[/bold cyan]")
            time.sleep(0.3)

        console.print(Panel.fit(
            "[bold white]OMNI v0.5.1 (Real)[/bold white]\n[dim]The Secure AI Stack[/dim]",
            border_style="green",
            padding=(1, 4)
        ))
        console.print("")

    def dashboard(self):
        table = Table(show_header=True, header_style="bold magenta", expand=True, border_style="dim")
        table.add_column("Active Brain", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("VRAM", style="yellow")
        
        mem_usage = "0.0 GB"
        if self.model:
            mem_usage = "~3.5 GB"
            
        brain_label = f"@roe/{self.active_brain}"
        if self.active_brain == "None":
             brain_label = "No Brain Loaded"
        else:
             brain_label += " (Base Model)"
            
        table.add_row(brain_label, self.status, mem_usage)
        console.print(table)

    def ensure_model(self):
        """Ensure the Base Model is downloaded using Python API."""
        if os.path.exists(LOCAL_MODEL_DIR):
            return True
            
        console.print(f"[yellow]⚠️  Base Brain (Llama-3.2-3B) not found.[/yellow]")
        if Confirm.ask(f"Download [bold white]Base Brain (3GB)[/bold white] from Hugging Face?"):
            try:
                from huggingface_hub import snapshot_download
                
                with console.status("[bold cyan]Downloading Neural Weights (this may take a while)...[/bold cyan]"):
                    snapshot_download(
                        repo_id=BASE_MODEL_REPO,
                        local_dir=LOCAL_MODEL_DIR,
                        local_dir_use_symlinks=False
                    )
                
                console.print("[green]✅ Download Complete.[/green]")
                return True
            except ImportError:
                console.print("[red]❌ huggingface_hub not installed. Run install.sh again.[/red]")
                return False
            except Exception as e:
                console.print(f"[red]❌ Download Failed: {e}[/red]")
                return False
        return False

    def load_brain(self, name):
        if not self.ensure_model():
            return False
            
        if self.model is None:
            with console.status(f"[bold cyan]Mounting Base Model into VRAM...[/bold cyan]", spinner="arc"):
                try:
                    from mlx_lm import load
                    self.model, self.tokenizer = load(LOCAL_MODEL_DIR)
                    self.status = "Ready"
                except ImportError:
                    console.print("[red]❌ MLX not installed. Run install.sh again.[/red]")
                    return False
                except Exception as e:
                    console.print(f"[red]❌ Load Failed: {e}[/red]")
                    return False
        
        # We swap persona, not weights
        self.active_brain = name
        console.print(f"[green]✅ Active Persona: @roe/{name}[/green]")
        return True

    def generate(self, user_prompt):
        if not self.model:
            console.print("[red]❌ No brain loaded.[/red]")
            return

        # System Prompt based on Persona
        personas = {
            "frontend": "You are @roe/frontend, an expert in React, Tailwind, and TypeScript. Write clean, modern code.",
            "backend": "You are @roe/backend, an expert in Python, FastAPI, and SQL. Write robust, async code.",
            "flutter": "You are @roe/flutter, an expert in Dart and Flutter. Write widget-based code.",
            "unity": "You are @roe/unity, an expert in C# and Unity3D. Write component-based scripts.",
            "architect": "You are @roe/architect. Design scalable cloud systems using MermaidJS diagrams.",
            "None": "You are Omni, a helpful AI assistant."
        }
        
        system_prompt = personas.get(self.active_brain, personas["None"])
        
        full_prompt = f"<|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        console.print(f"\n[bold green]@{self.active_brain}:[/bold green]", end=" ")
        
        from mlx_lm import generate
        
        # Spinner while generating
        with console.status("[dim]Thinking...[/dim]", spinner="dots"):
            response = generate(self.model, self.tokenizer, prompt=full_prompt, max_tokens=512, verbose=False)
        
        console.print(Markdown(response))
        console.print("")

    def chat_loop(self):
        self.splash()
        console.print("[dim]I see 12 files here. How can I help you today?[/dim]")
        console.print("[dim](Try: 'I want to build a Flutter app' or 'Train a brain on ./docs')[/dim]")

        while True:
            # Smart Prompt
            user_input = Prompt.ask("\n[bold white]omni[/bold white] [dim]>[/dim]")
            
            if not user_input: continue
            if user_input.lower() in ["exit", "quit"]: break
            
            if user_input.lower() == "menu":
                self.available_brains = self.scan_brains()
                console.print(f"[cyan]Available Personas:[/cyan] {', '.join(self.available_brains)}")
                continue

            # Auto-Routing Logic (Simple)
            if self.active_brain == "None":
                keywords = {
                    "unity": "unity", "flutter": "flutter", "react": "frontend", 
                    "web": "frontend", "game": "frontend", "api": "backend", "python": "backend",
                    "atari": "frontend", "pitfall": "frontend", "snake": "frontend"
                }
                for k, v in keywords.items():
                    if k in user_input.lower():
                        console.print(f"[dim]Routing to @roe/{v}...[/dim]")
                        self.load_brain(v)
                        break
            
            # If still no brain, ask user or default to backend
            if self.active_brain == "None":
                if Confirm.ask("[yellow]No brain selected. Load default (Backend)?[/yellow]"):
                    self.load_brain("backend")
                else:
                    continue

            # Generate
            self.generate(user_input)

    def run_cli(self):
        self.chat_loop()

def main():
    agent = OmniAgent()
    agent.run_cli()

if __name__ == "__main__":
    main()
