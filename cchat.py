#!/usr/bin/env python3
import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from cpack import pack_context

# cchat.py - Context Chat
# Interact with your codebase using an LLM API.
# Built by: Vector (Aurelius Swarm)

def get_api_key():
    """Retrieve API key from environment."""
    # Support OpenAI style for now as it's the standard schema
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("Error: OPENAI_API_KEY environment variable not found.")
        print("Please export it: export OPENAI_API_KEY='sk-...'")
        sys.exit(1)
    return key

def call_llm(context, prompt, model="gpt-4o"):
    """Call LLM API using standard library (no pip required)."""
    api_key = get_api_key()
    url = "https://api.openai.com/v1/chat/completions"
    
    system_prompt = (
        "You are an expert software engineer. "
        "You are provided with a codebase context in Markdown format. "
        "Answer the user's question based strictly on this context. "
        "Be concise and provide code snippets where relevant."
    )
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\n---\n\nQuestion: {prompt}"}
        ],
        "temperature": 0.2
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    except urllib.error.HTTPError as e:
        print(f"\nAPI Error: {e.code} - {e.reason}")
        error_body = e.read().decode('utf-8')
        print(f"Details: {error_body}")
        sys.exit(1)
    except Exception as e:
        print(f"\nNetwork Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Chat with your codebase.")
    parser.add_argument("prompt", help="The question or instruction for the AI.")
    parser.add_argument("--path", default=".", help="Root directory to pack (default: current)")
    parser.add_argument("--model", default="gpt-4o", help="Model to use (default: gpt-4o)")
    
    args = parser.parse_args()
    
    print("📦 Packing context...")
    # Capture cpack output by redirecting stdout temporarily or modifying cpack to return string
    # Since we imported cpack, let's capture the output to a temporary file or modify cpack.
    # For MVP speed, we'll write to a temp file using the existing logic.
    
    temp_file = ".cchat_context.tmp"
    pack_context(args.path, output_file=temp_file, clipboard=False)
    
    with open(temp_file, 'r', encoding='utf-8') as f:
        context_data = f.read()
    
    # Cleanup
    os.remove(temp_file)
    
    print(f"🧠 Thinking ({args.model})...")
    answer = call_llm(context_data, args.prompt, args.model)
    
    print("\n" + "="*40 + "\n")
    print(answer)
    print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    main()
