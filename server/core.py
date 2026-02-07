import os
import sys
import glob
import subprocess
import re
import psutil
from typing import List, Optional
from swarm.bus import OmniBus
from swarm.agent import SwarmAgent
from swarm.types import SwarmMessage, MessageType

# Models
MODEL_LITE = "mlx-community/Llama-3.2-3B-Instruct"
MODEL_PRO = "mlx-community/Meta-Llama-3.1-8B-Instruct-4bit"
LOCAL_MODEL_DIR = os.path.expanduser("~/.omni/models/base")

class OmniCore:
    def __init__(self):
        self.active_brain = "None"
        self.status = "Idle"
        self.model = None
        self.tokenizer = None
        self.base_model_repo = self.detect_hardware()
        
        self.personas = [
            "architect", "backend", "frontend", "devops",
            "ios", "android", "flutter", "react-native",
            "unity", "unreal", "shell", "sql", "git"
        ]
        
        # Swarm Init
        self.bus = OmniBus()
        self.agents = {}
        self.init_swarm()

    def detect_hardware(self):
        """Auto-select best Brain based on RAM."""
        total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
        print(f"[Core] System RAM: {total_ram_gb:.1f} GB")
        
        if total_ram_gb >= 14: # Safe buffer for 16GB machines
            print(f"[Core] High-Spec Detected. Selecting PRO Brain (8B).")
            return MODEL_PRO
        else:
            print(f"[Core] Standard-Spec Detected. Selecting LITE Brain (3B).")
            return MODEL_LITE

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
        
        # Subscribe broadcast handler
        self.bus.subscribe("broadcast", self.on_swarm_message)
        self.bus.subscribe("user", self.on_swarm_message)

    def on_swarm_message(self, msg: SwarmMessage):
        pass

    def get_installed_brains(self) -> List[str]:
        installed = []
        if os.path.exists(LOCAL_MODEL_DIR):
            installed.append(f"Base Brain ({self.base_model_repo.split('/')[-1]})")
        
        if os.path.exists("models"):
            for p in glob.glob("models/*-fused"):
                installed.append(os.path.basename(p).replace("-fused", ""))
        return installed

    def load_model_if_needed(self):
        if self.model: return True
        
        if not os.path.exists(LOCAL_MODEL_DIR):
            return False 
        
        try:
            from mlx_lm import load
            self.model, self.tokenizer = load(LOCAL_MODEL_DIR)
            self.status = "Ready"
            return True
        except Exception as e:
            print(f"Load Error: {e}")
            return False

    def llm_interface(self, system, user):
        """Bridge between Swarm Agents and the shared MLX model."""
        if not self.load_model_if_needed():
            return "Error: Brain not loaded."
            
        full_prompt = f"<|start_header_id|>system<|end_header_id|>\n\n{system}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{user}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        from mlx_lm import generate
        response = generate(self.model, self.tokenizer, prompt=full_prompt, max_tokens=1024, verbose=False)
        return response

    def run_inference(self, user_prompt: str, active_brain: str = "None"):
        if not self.load_model_if_needed():
            raise Exception("Model not installed")

        self.active_brain = active_brain
        
        installed = self.get_installed_brains()
        base_prompt = f"""You are Omni, a Secure AI Stack running locally.
Your goal is to help the user build software.
You have access to the following Physical Brains: {', '.join(installed)}.
You can act as the following Personas: {', '.join(self.personas)}.
Current Persona: @roe/{active_brain if active_brain != "None" else "omni"}
"""
        
        response = self.llm_interface(base_prompt, user_prompt)
        return response

    def download_model(self):
        try:
            from huggingface_hub import snapshot_download
            snapshot_download(repo_id=self.base_model_repo, local_dir=LOCAL_MODEL_DIR, local_dir_use_symlinks=False)
            return True
        except Exception as e:
            raise e
