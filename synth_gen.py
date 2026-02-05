#!/usr/bin/env python3
import os
import json
import random
import time
import sys
import requests
from dotenv import load_dotenv

# synth_gen.py - Secure Synthetic Data Generator
# Uses REST API to avoid deprecated library issues.
# Model: gemini-3-pro-preview

# Load Env
load_dotenv(override=True)

# KEY ROTATION
# Load from environment variables (comma separated) or single key
KEYS = [
    os.getenv("GEMINI_API_KEY", "").strip(),
]
# Support multiple keys via env var GEMINI_KEYS if needed
if os.getenv("GEMINI_KEYS"):
    KEYS.extend([k.strip() for k in os.getenv("GEMINI_KEYS").split(",")])

# Filter empties
KEYS = [k for k in KEYS if k]
if not KEYS:
    print("ERROR: No API Keys found in GEMINI_API_KEY or GEMINI_KEYS env vars.")
    sys.exit(1)

current_key_idx = 0

print(f"DEBUG: Loaded {len(KEYS)} API Keys for rotation.")

# Config
MODEL_NAME = "gemini-3-pro-preview"
OUTPUT_DIR = "datasets"

TASKS = {
    "architect": {
        "file": "architect_training.jsonl",
        "prompt": "Generate 10 unique System Architecture tasks. Format: JSON array of objects with keys 'instruction' (the task) and 'output' (the solution). Output ONLY raw JSON."
    },
    "frontend": {
        "file": "frontend_training.jsonl",
        "prompt": "Generate 10 unique Frontend Dev tasks (React/Tailwind/Typescript). Focus on modern UI, state, and responsive. Format: JSON array of objects with keys 'instruction' (the task) and 'output' (the code solution). Output ONLY raw JSON."
    },
    "backend": {
        "file": "backend_training.jsonl",
        "prompt": "Generate 10 unique Backend Dev tasks (Python/FastAPI/Node/SQL). Focus on APIs, DB schemas, and async logic. Format: JSON array of objects with keys 'instruction' (the task) and 'output' (the code solution). Output ONLY raw JSON."
    },
    "ios": {
        "file": "ios_training.jsonl",
        "prompt": "Generate 10 unique iOS Development tasks (Swift/SwiftUI/UIKit/Objective-C). Focus on memory management, Core Data, Combine, and native Apple frameworks. Format: JSON array of objects with keys 'instruction' (the task) and 'output' (the code solution). Output ONLY raw JSON."
    },
    "android": {
        "file": "android_training.jsonl",
        "prompt": "Generate 10 unique Android Development tasks (Kotlin/Java/Jetpack Compose/XML). Focus on Activities, Fragments, Room Database, and Hilt dependency injection. Format: JSON array of objects with keys 'instruction' (the task) and 'output' (the code solution). Output ONLY raw JSON."
    },
    "flutter": {
        "file": "flutter_training.jsonl",
        "prompt": "Generate 10 unique Flutter Development tasks (Dart/Widgets). Focus on state management (Provider/Riverpod), custom painters, and platform channels. Format: JSON array of objects with keys 'instruction' (the task) and 'output' (the code solution). Output ONLY raw JSON."
    },
    "react-native": {
        "file": "react_native_training.jsonl",
        "prompt": "Generate 10 unique React Native tasks (TypeScript/JavaScript). Focus on Native Modules, Expo, Reanimated, and bridge optimization. Format: JSON array of objects with keys 'instruction' (the task) and 'output' (the code solution). Output ONLY raw JSON."
    },
    "desktop": {
        "file": "desktop_training.jsonl",
        "prompt": "Generate 10 unique Desktop App tasks (Electron/Tauri/MacOS). Focus on cross-platform windowing and native APIs. Format: JSON array of objects with keys 'instruction' (the task) and 'output' (the code solution). Output ONLY raw JSON."
    },
    "ai_eng": {
        "file": "ai_eng_training.jsonl",
        "prompt": "Generate 10 unique AI Engineering tasks (PyTorch/RAG/LangChain). Focus on training loops, vector DBs, and agent logic. Format: JSON array of objects with keys 'instruction' (the task) and 'output' (the code solution). Output ONLY raw JSON."
    },
    "devops": {
        "file": "devops_training.jsonl",
        "prompt": "Generate 10 unique DevOps tasks (Docker/K8s/CI-CD/Linux). Focus on deployment, containers, and bash scripting. Format: JSON array of objects with keys 'instruction' (the task) and 'output' (the code solution). Output ONLY raw JSON."
    }
}

def get_next_key():
    global current_key_idx
    k = KEYS[current_key_idx]
    current_key_idx = (current_key_idx + 1) % len(KEYS)
    return k

def generate_batch(task_name):
    task = TASKS[task_name]
    
    # Rotate Key
    api_key = get_next_key()
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": task["prompt"]}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "responseMimeType": "application/json"
        }
    }
    
    # print(f"DEBUG: Using Key ...{api_key[-4:]}") # Noisy log
    try:
        response = requests.post(api_url, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code != 200:
            print(f"[{task_name.upper()}] API Error {response.status_code} (Key ...{api_key[-4:]})")
            if response.status_code == 429:
                time.sleep(2) # Short sleep, next key might be fresh
            return

        result = response.json()
        
        # Extract text
        try:
            text = result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            print(f"[{task_name.upper()}] Malformed response: {result}")
            return

        # Cleanup (just in case model sends markdown despite MIME type)
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
            
        data = json.loads(text)
        
        filepath = os.path.join(OUTPUT_DIR, task["file"])
        with open(filepath, "a") as f:
            for entry in data:
                f.write(json.dumps(entry) + "\n")
        
        print(f"[{task_name.upper()}] Generated {len(data)} samples.")
        
    except Exception as e:
        print(f"[{task_name.upper()}] Error: {e}")

# Priority Order
PRIORITY_ORDER = ["backend", "frontend", "architect", "devops", "ios", "android", "flutter", "react-native", "desktop", "ai_eng"]
TARGET_COUNT = 1000

def get_current_count(task_name):
    filename = TASKS[task_name]["file"]
    filepath = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(filepath):
        return 0
    try:
        with open(filepath, 'r') as f:
            return sum(1 for _ in f)
    except:
        return 0

def get_next_task():
    # Strict Priority: Find first task under target
    for task in PRIORITY_ORDER:
        count = get_current_count(task)
        if count < TARGET_COUNT:
            print(f"DEBUG: Focus -> {task.upper()} ({count}/{TARGET_COUNT})")
            return task
    
    # If all done, fallback to random or rotation (or just pick first to keep growing)
    print("DEBUG: All targets met. Boosting Architect.")
    return "architect"

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"Starting Secure Generator. Model: {MODEL_NAME}")
    print(f"Target: {OUTPUT_DIR}")
    print("Press Ctrl+C to stop.")
    
    while True:
        # Pick next task in priority order
        task = get_next_task()
        generate_batch(task)
        time.sleep(5) # Rate limit protection (Scaled back)

if __name__ == "__main__":
    main()
