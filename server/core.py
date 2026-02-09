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
from .pilot import Pilot
from .executor import AutoExecutor

# Models
MODEL_LITE = "mlx-community/Llama-3.2-3B-Instruct"
MODEL_PRO = "mlx-community/Meta-Llama-3.1-8B-Instruct-4bit"
LOCAL_MODEL_DIR = os.path.expanduser("~/.omni/models/base")

class OmniCore:
    def __init__(self):
        print("DEBUG: OMNI CORE INIT - EXECUTOR LOADING...")
        self.active_brain = "None"
        self.status = "Idle"
        self.model = None
        self.tokenizer = None
        self.base_model_repo = self.detect_hardware()
        self.pilot = Pilot(self)
        self.executor = AutoExecutor()
        
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
        total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
        print(f"[Core] System RAM: {total_ram_gb:.1f} GB")
        if total_ram_gb >= 14: return MODEL_PRO
        else: return MODEL_LITE

    def init_swarm(self):
        for p in self.personas:
            agent_name = f"@roe/{p}"
            self.agents[p] = SwarmAgent(
                name=agent_name,
                bus=self.bus,
                llm_client=self.llm_interface,
                system_prompt=f"You are {agent_name}. Expert in {p}."
            )
        self.bus.subscribe("broadcast", self.on_swarm_message)
        self.bus.subscribe("user", self.on_swarm_message)

    def on_swarm_message(self, msg: SwarmMessage): pass

    def get_installed_brains(self) -> List[str]:
        installed = []
        if os.path.exists(LOCAL_MODEL_DIR):
            installed.append("Base Brain")
        if os.path.exists("models"):
            for p in glob.glob("models/*-fused"):
                installed.append(os.path.basename(p).replace("-fused", ""))
        return installed

    def load_model_if_needed(self):
        if self.model: return True
        if not os.path.exists(LOCAL_MODEL_DIR): return False 
        try:
            from mlx_lm import load
            self.model, self.tokenizer = load(LOCAL_MODEL_DIR)
            self.status = "Ready"
            return True
        except Exception as e:
            print(f"Load Error: {e}")
            return False

    def llm_interface(self, system, user):
        if not self.load_model_if_needed(): return "Error: Brain not loaded."
        full_prompt = f"<|start_header_id|>system<|end_header_id|>\n\n{system}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{user}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        from mlx_lm import generate
        response = generate(self.model, self.tokenizer, prompt=full_prompt, max_tokens=1024, verbose=False)
        return response

    def route_intent(self, prompt: str) -> str:
        prompt = prompt.lower()
        if ("backend" in prompt and "frontend" in prompt) or "dashboard" in prompt or "full stack" in prompt:
            return "architect"
        if any(x in prompt for x in ["react native", "mobile app", "ios", "android"]):
            return "react-native" 
        if any(x in prompt for x in ["react", "frontend", "css", "html", "tailwind", "ui", "component"]):
            return "frontend"
        if any(x in prompt for x in ["python", "backend", "api", "flask", "django", "fastapi", "sql", "database"]):
            return "backend"
        if any(x in prompt for x in ["docker", "kubernetes", "aws", "deploy", "ci/cd"]):
            return "devops"
        if any(x in prompt for x in ["game", "pygame", "unity"]):
            return "backend" 
        return "None"

    def run_inference(self, user_prompt: str, active_brain: str = "None"):
        # Sticky Routing: If the user didn't specify a brain, use the currently loaded one
        # unless a strong signal detects a different intent.
        
        detected_brain = self.route_intent(user_prompt)
        
        if active_brain in ["None", "Base Brain"]:
            if detected_brain != "None":
                active_brain = detected_brain
            elif self.active_brain not in ["None", "Base Brain"] and self.active_brain is not None:
                # Keep current brain if no new intent detected (prevent fallback to Base causing reload)
                active_brain = self.active_brain

        self.prepare_model(active_brain)
        self.active_brain = active_brain
        
        # ... rest of function
        base_prompt = f"""You are Omni, a Secure AI Stack.
Current Persona: @roe/{active_brain if active_brain != "None" else "omni"}

CRITICAL RULES:
1. Provide the FULL SOURCE CODE for ALL files.
2. START every code block with a comment: `# filename: <name>` (or `// filename: <name>`).
3. YOU MUST GENERATE `requirements.txt` (for Python) containing ALL used libraries (e.g., flask, pandas, dash).
4. DO NOT put python packages in `package.json`. `package.json` is ONLY for Node.js/React.
5. For Multi-File Apps, generate a `start.sh` script that runs everything locally.
   - Example: `python3 app.py`
   - DO NOT USE DOCKER unless explicitly asked. Run processes directly.
6. PREFERENCE: Use `flask`/`fastapi` for Python, `react` for Frontend.
"""
        response = self.llm_interface(base_prompt, user_prompt)
        return self.executor.process(response)

    def prepare_model(self, active_brain):
        potential_path = os.path.join("models", f"{active_brain}-fused")
        target_path = LOCAL_MODEL_DIR
        if os.path.exists(potential_path): target_path = potential_path
        
        # Concurrency safety: if we are already loading or running, we might need to be careful.
        # But this method is called within inference flow.
        
        if not hasattr(self, 'current_model_path') or self.current_model_path != target_path:
             print(f"[Core] Loading Weights: {target_path}...")
             try:
                 # Clear previous model to free memory/buffers if possible
                 if self.model:
                     del self.model
                     del self.tokenizer
                     import gc
                     gc.collect() # Force cleanup to release Metal buffers
                     
                 from mlx_lm import load
                 self.model, self.tokenizer = load(target_path)
                 self.current_model_path = target_path
                 self.status = f"Active: {active_brain}"
             except Exception as e:
                 print(f"[Core] Load Failed: {e}")
                 # Fallback
                 self.current_model_path = LOCAL_MODEL_DIR
                 self.model, self.tokenizer = load(LOCAL_MODEL_DIR)

    def stream_generate(self, user_prompt, active_brain="None"):
        # Sticky Routing Logic (Mirrored from run_inference)
        detected_brain = self.route_intent(user_prompt)
        
        if active_brain in ["None", "Base Brain"]:
            if detected_brain != "None":
                active_brain = detected_brain
            elif self.active_brain not in ["None", "Base Brain"] and self.active_brain is not None:
                # Keep current brain if no new intent detected
                active_brain = self.active_brain

        yield f"__BRAIN__:{active_brain}"

        if not self.load_model_if_needed(): yield "Error: Model missing."
        
        # Ensure model is ready
        self.prepare_model(active_brain)
        
        installed_brains_list = "\n".join([f"- @roe/{b}" if b != "Base Brain" else "- Base Brain" for b in self.get_installed_brains()])
        
        base_prompt = f"""You are Omni, a Secure AI Stack created by ROE Defense.
Current Persona: @roe/{active_brain if active_brain != "None" else "omni"}

REALITY CONFIGURATION (You ONLY have these modules):
{installed_brains_list}

RULES:
1. IDENTITY: You are Omni. You were created by ROE Defense. You are NOT created by Meta, OpenAI, or Google.
2. CAPABILITIES: You ONLY have the brains listed above. If asked for 'Medical' or 'Math' brains, say you don't have them.
3. CONVERSATION: Answer questions naturally. Do NOT write code unless the user explicitly asks you to "write", "create", "generate", or "build" something.
4. CODING STANDARDS (Only apply if coding):
   - Provide FULL SOURCE CODE.
   - Start blocks with `# filename: <name>`.
   - Generate `requirements.txt` / `package.json`.
   - Generate `start.sh` (except for static sites).
   - Python packages go in requirements.txt, NOT package.json.
"""
        # Improved Prompt Structure: System -> User -> Assistant
        full_prompt = f"<|start_header_id|>system<|end_header_id|>\n\n{base_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        from mlx_lm import stream_generate
        
        # Adding a small delay or try/except block around generation to handle Metal flakiness
        try:
            for response in stream_generate(self.model, self.tokenizer, full_prompt, max_tokens=2048):
                yield response.text
        except Exception as e:
            print(f"[Core] Generation Error: {e}")
            yield f"\n[Error: {str(e)}]"

    def download_model(self):
        try:
            from huggingface_hub import snapshot_download
            snapshot_download(repo_id=self.base_model_repo, local_dir=LOCAL_MODEL_DIR, local_dir_use_symlinks=False)
            return True
        except Exception as e:
            raise e

    def run_vision(self, image_path: str, prompt: str = "Describe this image."):
        try:
            from mlx_vlm import load, generate
            from mlx_vlm.utils import load_image
            vision_model_path = "mlx-community/moondream2-4bit" 
            model, processor = load(vision_model_path)
            image = load_image(image_path)
            return generate(model, processor, image, prompt, verbose=False)
        except Exception as e:
            return f"Vision Error: {str(e)}"

    def run_transcription(self, audio_path: str):
        try:
            import mlx_whisper
            return mlx_whisper.transcribe(audio_path, path_or_hf_repo="mlx-community/whisper-base-mlx")["text"]
        except Exception as e:
            return f"Voice Error: {str(e)}"

    def run_tts(self, text: str, output_path: str):
        try:
            from kokoro_onnx import Kokoro
            import soundfile as sf
            model_dir = os.path.expanduser("~/.omni/models/kokoro")
            model_path = os.path.join(model_dir, "kokoro-v0_19.onnx")
            voices_path = os.path.join(model_dir, "voices.json")
            if not os.path.exists(model_path): return
            
            kokoro = Kokoro(model_path, voices_path)
            samples, sample_rate = kokoro.create(text, voice="af_sarah", speed=1.0, lang="en-us")
            sf.write(output_path, samples, sample_rate)
            return output_path
        except Exception as e:
            raise e

    def run_pilot_action(self, instruction: str):
        return self.pilot.execute(instruction)
