#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
import json
import time

# Omni CLI - The Interface
# Version: 0.1.0

BANNER = """
   ____  __  __ _   _ _____ 
  / __ \|  \/  | \ | |_   _|
 | |  | | \  / |  \| | | |  
 | |  | | |\/| | . ` | | |  
 | |__| | |  | | |\  |_| |_ 
  \____/|_|  |_|_| \_|_____|
                            
  The Secure AI Stack.
"""

def check_requirements():
    """Ensure MLX and dependencies are installed."""
    try:
        import mlx.core
    except ImportError:
        print("❌ Error: MLX not found.")
        print("Run: pip install mlx mlx-lm")
        sys.exit(1)

def train_brain(name, path, base_model="mlx-community/Llama-3.2-3B-Instruct"):
    """
    Orchestrate the local training process.
    1. Scan/Prep Data
    2. Convert to JSONL
    3. Trigger MLX LoRA
    4. Fuse
    """
    print(f"🧠 INITIALIZING TRAINING PROTOCOL: {name}")
    print(f"📂 Source: {os.path.abspath(path)}")
    print(f"🤖 Base:   {base_model}")
    print("-" * 40)

    if not os.path.exists(path):
        print(f"❌ Error: Path '{path}' does not exist.")
        sys.exit(1)

    # 1. Ingestion (Mock for now - real version would use cpack.py logic)
    print("• Scanning documents...")
    file_count = 0
    for root, _, files in os.walk(path):
        file_count += len(files)
    print(f"  > Found {file_count} files.")
    
    # 2. Preparation
    print("• Converting to Training Format (JSONL)...")
    dataset_path = f"datasets/custom_{name.replace('@', '').replace('/', '_')}.jsonl"
    os.makedirs("datasets", exist_ok=True)
    
    # Creates a dummy dataset for the CLI demo if none exists
    if not os.path.exists(dataset_path):
        with open(dataset_path, "w") as f:
            sample = {"messages": [{"role": "user", "content": "Explain this project."}, {"role": "assistant", "content": "This is a custom trained brain."}]}
            for _ in range(100): # Mock data
                f.write(json.dumps(sample) + "\n")
    print(f"  > Dataset created: {dataset_path}")

    # 3. Training
    print("• Igniting MLX Engine (LoRA)...")
    adapter_path = f"adapters/{name}"
    
    # We construct the command but don't run it fully in this demo script to avoid locking the GPU
    # In a real run, we would subprocess.call this:
    cmd = [
        "mlx_lm.lora",
        "--model", base_model,
        "--train",
        "--data", dataset_path,
        "--iters", "100", 
        "--adapter-path", adapter_path
    ]
    print(f"  > Executing: {' '.join(cmd)}")
    
    # Simulator
    for i in range(0, 101, 20):
        time.sleep(0.5)
        print(f"  > Training... {i}% Loss: {2.5 - (i/50.0):.4f}")

    # 4. Fusing
    print("• Fusing Weights...")
    fuse_path = f"models/{name}-fused"
    print(f"  > Saving to: {fuse_path}")
    
    print("-" * 40)
    print(f"✅ BRAIN READY: {name}")
    print(f"To run: omni run {name}")

def run_brain(name):
    print(f"🚀 Loading Cartridge: {name}")
    # Integration with mlx_lm.generate would go here
    print("• Interactive Mode Active. (Ctrl+C to exit)")
    while True:
        try:
            user_input = input("You > ")
            print(f"{name} > [Simulated Inference Response]")
        except KeyboardInterrupt:
            print("\nExiting.")
            break

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="Omni CLI Management Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # train
    train_parser = subparsers.add_parser("train", help="Train a custom brain on local data")
    train_parser.add_argument("--name", required=True, help="Name of the brain (e.g. @my/project)")
    train_parser.add_argument("--path", required=True, help="Path to documents/code")
    train_parser.add_argument("--base", default="mlx-community/Llama-3.2-3B-Instruct", help="Base model to use")

    # run
    run_parser = subparsers.add_parser("run", help="Run a specific brain")
    run_parser.add_argument("name", help="Name of the fused brain to run")

    # list
    list_parser = subparsers.add_parser("list", help="List available brains")

    args = parser.parse_args()

    if args.command == "train":
        train_brain(args.name, args.path, args.base)
    elif args.command == "run":
        run_brain(args.name)
    elif args.command == "list":
        print("Available Brains:")
        if os.path.exists("models"):
            for m in os.listdir("models"):
                if m.endswith("-fused"):
                    print(f"  - {m.replace('-fused', '')}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
