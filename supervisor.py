#!/usr/bin/env python3
import time
import os
import subprocess
import datetime
import sys

# supervisor.py - The Autonomous Commander
# Objective: Monitor Data Gen -> Trigger Training per Brain

LOG_FILE = "MISSION_LOG.md"
TARGET_SAMPLES = 1000
TRAIN_ENV_PYTHON = "train_env/bin/python3"
MLX_LORA = "train_env/bin/mlx_lm.lora"
MLX_FUSE = "train_env/bin/mlx_lm.fuse"

# Configuration
# Base models: 1B for Regex, 3B for others
BRAINS = [
    {"name": "architect", "file": "datasets/architect_training.jsonl", "base": "mlx-community/Llama-3.2-3B-Instruct-4bit", "status": "pending", "merge": ["datasets/python_training.jsonl"]},
    {"name": "backend",   "file": "datasets/backend_training.jsonl",   "base": "mlx-community/Llama-3.2-3B-Instruct-4bit", "status": "pending"},
    {"name": "frontend",  "file": "datasets/frontend_training.jsonl",  "base": "mlx-community/Llama-3.2-3B-Instruct-4bit", "status": "pending"},
    {"name": "devops",    "file": "datasets/devops_training.jsonl",    "base": "mlx-community/Llama-3.2-3B-Instruct-4bit", "status": "pending"},
    {"name": "mobile",    "file": "datasets/mobile_training.jsonl",    "base": "mlx-community/Llama-3.2-3B-Instruct-4bit", "status": "pending"},
    {"name": "desktop",   "file": "datasets/desktop_training.jsonl",   "base": "mlx-community/Llama-3.2-3B-Instruct-4bit", "status": "pending"},
    {"name": "ai_eng",    "file": "datasets/ai_eng_training.jsonl",    "base": "mlx-community/Llama-3.2-3B-Instruct-4bit", "status": "pending"},
    {"name": "regex-pro", "file": "datasets/regex_training.jsonl",    "base": "mlx-community/Llama-3.2-1B-Instruct-4bit", "status": "pending"},
    {"name": "sec-ops",   "file": "datasets/secops_training.jsonl",    "base": "mlx-community/Llama-3.2-3B-Instruct-4bit", "status": "pending"},
]

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"**[{timestamp}]** {message}\n"
    print(entry.strip())
    with open(LOG_FILE, "a") as f:
        f.write(entry)

def ensure_env():
    if not os.path.exists("train_env"):
        log("⚙️  Setting up Training Environment...")
        subprocess.run([sys.executable, "-m", "venv", "train_env"], check=True)
        subprocess.run(["train_env/bin/pip", "install", "-U", "pip", "mlx", "mlx-lm"], check=True)

def count_lines(filepath):
    if not os.path.exists(filepath): return 0
    try:
        with open(filepath, "r") as f:
            return sum(1 for _ in f)
    except:
        return 0

def prepare_data(brain):
    name = brain["name"]
    main_file = brain["file"]
    
    data_dir = f"data/{name}"
    os.makedirs(data_dir, exist_ok=True)
    
    # Merge if needed
    full_dataset = f"{data_dir}/full.jsonl"
    if os.path.exists(main_file):
        os.system(f"cat {main_file} > {full_dataset}")
    
    if "merge" in brain:
        for extra in brain["merge"]:
            if os.path.exists(extra):
                log(f"• Merging {extra} into {name}...")
                os.system(f"cat {extra} >> {full_dataset}")
    
    # CONVERT FORMAT (Instruction/Output -> Chat/Messages)
    # MLX expects {"messages": [{"role": "user", "content": "X"}, {"role": "assistant", "content": "Y"}]}
    converted_dataset = f"{data_dir}/converted.jsonl"
    
    import json
    try:
        with open(full_dataset, 'r') as infile, open(converted_dataset, 'w') as outfile:
            for line in infile:
                try:
                    obj = json.loads(line)
                    # Support legacy format
                    if "instruction" in obj and "output" in obj:
                        new_obj = {
                            "messages": [
                                {"role": "user", "content": obj["instruction"]},
                                {"role": "assistant", "content": obj["output"]}
                            ]
                        }
                        outfile.write(json.dumps(new_obj) + "\n")
                    elif "messages" in obj:
                        outfile.write(line)
                except:
                    continue
    except Exception as e:
        log(f"❌ Conversion failed: {e}")
        return False

    # Split 90/10
    total = count_lines(converted_dataset)
    if total == 0: return False
    
    split = int(total * 0.9)
    os.system(f"head -n {split} {converted_dataset} > {data_dir}/train.jsonl")
    os.system(f"tail -n +{split+1} {converted_dataset} > {data_dir}/valid.jsonl")
    return True

def train_brain(brain):
    name = brain["name"]
    base = brain["base"]
    data_path = f"data/{name}"
    adapter_path = f"adapters/{name}"
    
    log(f"🧠 STARTING TRAINING: {name.upper()}")
    log(f"• Base: {base}")
    
    try:
        # 1. Train
        cmd = [
            MLX_LORA,
            "--model", base,
            "--train",
            "--data", data_path,
            "--iters", "600",
            "--batch-size", "4",
            "--adapter-path", adapter_path
        ]
        
        with open(f"{name}_train.log", "w") as logfile:
            subprocess.run(cmd, stdout=logfile, stderr=logfile, check=True)
            
        # 2. Fuse
        log(f"• Fusing {name}...")
        subprocess.run([
            MLX_FUSE,
            "--model", base,
            "--adapter-path", adapter_path,
            "--save-path", f"models/{name}-fused"
        ], check=True)
        
        log(f"✅ {name.upper()} TRAINING COMPLETE.")
        return True
        
    except Exception as e:
        log(f"❌ TRAINING FAILED for {name}: {e}")
        return False

def main():
    log("🤖 SUPERVISOR ACTIVE. Mode: Concurrent Training.")
    ensure_env()
    
    while True:
        active_training = False
        
        for brain in BRAINS:
            if brain["status"] == "done":
                continue
                
            count = count_lines(brain["file"])
            # Check merge files too for total count
            if "merge" in brain:
                for m in brain["merge"]:
                    count += count_lines(m)
            
            if count >= TARGET_SAMPLES:
                if brain["status"] == "pending":
                    log(f"🎯 Target Reached for {brain['name']} ({count}). Preparing...")
                    if prepare_data(brain):
                        brain["status"] = "training"
                        if train_brain(brain):
                            brain["status"] = "done"
                        else:
                            brain["status"] = "failed"
                    else:
                        log(f"⚠️  Data preparation failed for {brain['name']}")
                elif brain["status"] == "training":
                    # Should be blocking in this loop, but just in case
                    pass
            else:
                # Still generating
                pass
        
        # Pace the checks
        time.sleep(30)

if __name__ == "__main__":
    main()
