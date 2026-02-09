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
from swarm.bus import OmniBus
from swarm.agent import SwarmAgent
from swarm.types import SwarmMessage, MessageType
from server.app import app as api_app

# Omni - The Secure Interface
# Usage: omni run

console = Console()
AUTO_CONFIRM = os.getenv("OMNI_HEADLESS", "false").lower() == "true"

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
        self.personas = [
            "architect", "backend", "frontend", "devops",
            "ios", "android", "flutter", "react-native",
            "unity", "unreal", "shell", "sql", "git"
        ]
        
        # Swarm Init
        self.bus = OmniBus()
        self.agents = {}
        self.init_swarm()

    def init_swarm(self):
        """Spawn virtual agents connected to the bus."""
        for p in self.personas:
            agent_name = f"@roe/{p}"
            self.agents[p] = SwarmAgent(
                name=agent_name,
                bus=self.bus,
                llm_client=self.llm_interface,
                system_prompt=f"You are {agent_name}. Expert in {p}."
            )
        
        # Subscribe UI to log everything
        self.bus.subscribe("broadcast", self.on_swarm_message)
        self.bus.subscribe("user", self.on_swarm_message)

    def on_swarm_message(self, msg: SwarmMessage):
        if msg.sender == "user": return # Don't echo self
        
        color = "green" if msg.type == MessageType.ARTIFACT else "yellow"
        console.print(Panel(
            Markdown(str(msg.payload.get('content') or msg.payload)),
            title=f"{msg.sender} -> {msg.recipient} ({msg.type.value})",
            border_style=color
        ))
        
        # If code execution needed
        if msg.type == MessageType.ARTIFACT:
            content = msg.payload.get("content", "")
            self.extract_and_run(content)

    def llm_interface(self, system, user):
        """Bridge between Swarm Agents and the shared MLX model."""
        if not self.load_model_if_needed():
            return "Error: Brain not loaded."
            
        full_prompt = f"<|start_header_id|>system<|end_header_id|>\n\n{system}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{user}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        from mlx_lm import generate
        response = generate(self.model, self.tokenizer, prompt=full_prompt, max_tokens=1024, verbose=False)
        return response

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
            "[bold white]OMNI v0.7.0 (Swarm Alpha)[/bold white]\n[dim]The Secure AI Stack[/dim]",
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
        if AUTO_CONFIRM or Confirm.ask(f"Download [bold white]Llama-3.2-3B[/bold white] from Hugging Face?"):
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

        # Iterate through all code blocks
        for lang, code in matches:
            ext = "txt"
            if lang in ["python", "py"]: ext = "py"
            elif lang in ["html", "js", "javascript", "jsx"]: ext = "html" # For now, treat JS/JSX as HTML wrapper or just JS file
            elif lang in ["sh", "bash"]: ext = "sh"
            
            # Simple heuristic for filename if provided in comments or just increment
            # For now, just save them sequentially or by type
            filename = f"omni_output_{int(time.time())}_{lang}.{ext}"
            
            # Check if filename is mentioned in the code (e.g. # filename: ... or // filename: ...)
            name_match = re.search(r'(?:#|//|<!--)\s*filename:\s*([\w./-]+)', code)
            if name_match:
                filename = name_match.group(1)
            
            console.print(f"\n[bold yellow]⚡ Detected {lang} code block.[/bold yellow]")
            
            if AUTO_CONFIRM or Confirm.ask(f"Save and run as [bold white]{filename}[/bold white]?"):
                # Ensure directory exists
                os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else ".", exist_ok=True)
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
                                if AUTO_CONFIRM or Confirm.ask(f"[yellow]Install missing '{mod}'?[/yellow]"):
                                    subprocess.run([sys.executable, "-m", "pip", "install", mod])
                                    subprocess.run([sys.executable, filename])
                    elif ext == "html":
                        opener = "open" if sys.platform == "darwin" else "xdg-open"
                        # Only open if GUI available (or just log it)
                        subprocess.run([opener, filename])
                    elif ext == "sh":
                        subprocess.run(["bash", filename])
                except Exception as e:
                    console.print(f"[red]❌ Execution Failed: {e}[/red]")

    def generate(self, user_prompt):
        # Swarm Routing Logic
        recipient = "@roe/backend" # Default
        
        # Simple Router
        if self.active_brain != "None":
            recipient = f"@roe/{self.active_brain}"
        else:
            # Try to route
            for p in self.personas:
                if p in user_prompt.lower():
                    recipient = f"@roe/{p}"
                    break
        
        console.print(f"[dim]Dispatching to {recipient}...[/dim]")
        
        # Publish to Bus
        msg = SwarmMessage(
            sender="user",
            recipient=recipient,
            type=MessageType.INSTRUCTION,
            payload={"task": user_prompt}
        )
        self.bus.publish(msg)
        
        # Wait for reply? 
        # Since bus is sync in v0.7.0, the on_swarm_message callback handles the print.
        # So we just return.

    def chat_loop(self):
        self.splash()
        console.print("[dim]Swarm Online. Type 'menu' or ask a question.[/dim]")

        while True:
            user_input = Prompt.ask("\n[bold white]omni[/bold white] [dim]>[/dim]")
            if not user_input: continue
            if user_input.lower() in ["exit", "quit"]: break
            
            # Simple keyword shortcut for menu
            if user_input.lower() == "menu":
                console.print(f"[cyan]Personas:[/cyan] {', '.join(self.personas)}")
                continue
            
            # System Inspection Logic
            if any(x in user_input.lower() for x in ["what brains", "list brains", "which brains", "downloaded", "installed"]):
                table = Table(title="Cognitive Cartridge Status", border_style="cyan")
                table.add_column("Brain", style="white")
                table.add_column("Status", style="green")
                
                # Check Local
                local_brains = []
                if os.path.exists("models"):
                    for p in glob.glob("models/*-fused"):
                        local_brains.append(os.path.basename(p).replace("-fused", ""))
                
                # Base Model
                if os.path.exists(LOCAL_MODEL_DIR):
                    table.add_row("Base Model (Llama-3B)", "✅ Downloaded")
                else:
                    table.add_row("Base Model (Llama-3B)", "❌ Missing")

                for brain in self.personas:
                    if brain in local_brains:
                        table.add_row(f"@roe/{brain}", "✅ Fine-Tuned")
                    else:
                        table.add_row(f"@roe/{brain}", "☁️  Remote / Simulated")
                
                console.print(table)
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
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "serve":
            console.print("[bold green]Starting Omni Local API...[/bold green]")
            import uvicorn
            uvicorn.run(api_app, host="127.0.0.1", port=8000)
        else:
            # Single-shot mode for testing/CLI
            query = " ".join(sys.argv[1:])
            console.print(f"[bold blue]Executing Single-Shot:[/bold blue] {query}")
            agent.generate(query)
            # Allow time for async bus to process (simple wait since we lack callback coordination here)
            time.sleep(5) 
    else:
        agent.run_cli()

if __name__ == "__main__":
    main()
