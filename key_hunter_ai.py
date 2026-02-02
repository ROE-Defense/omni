#!/usr/bin/env python3
import os
import sys
import re
import argparse
import time
import json
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

# key-hunter-ai.py - AI-Native Credential Scanner
# Built by: Sentinel (ROE Defense Systems)
# Version: 2.0.0 (AI-Augmented)

# Regex Signatures (Publicly known patterns)
SIGNATURES = {
    "AWS Access Key": r"(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
    "Google API Key": r"AIza[0-9A-Za-z\\-_]{35}",
    "Slack Token": r"(xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})",
    "Stripe Secret": r"(sk_live_[0-9a-zA-Z]{24})",
    "OpenAI API Key": r"(sk-[a-zA-Z0-9]{48}|sk-proj-[a-zA-Z0-9]{48})",
    "GitHub Token": r"(ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59})",
    "Private Key (PEM)": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----"
}

IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', 'env', '.idea', '.vscode'}
IGNORE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip', '.tar', '.gz', '.mp4', '.mp3', '.exe'}

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'

def get_api_key():
    key = os.environ.get("OPENAI_API_KEY")
    return key

def call_ai_verifier(finding, context_lines):
    """Ask the AI if this looks like a real leak or a test/example."""
    api_key = get_api_key()
    if not api_key:
        return {"status": "SKIPPED", "reason": "No API Key"}

    url = "https://api.openai.com/v1/chat/completions"
    
    prompt = f"""
    You are a Senior Security Engineer. Analyze this potential credential leak.
    
    Type: {finding['type']}
    File: {finding['file']}
    Line: {finding['line']}
    Code Context:
    ```
    {context_lines}
    ```
    
    Determine if this is a FALSE POSITIVE (test data, placeholder, example) or a HIGH PROBABILITY LEAK.
    
    Return strictly JSON:
    {{
        "verdict": "REAL" | "FAKE",
        "confidence": 0-100,
        "reasoning": "short explanation",
        "draft_email": "If REAL, write a polite 2-sentence disclosure email to the maintainer. If FAKE, null."
    }}
    """
    
    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "response_format": {"type": "json_object"}
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return json.loads(result['choices'][0]['message']['content'])
    except Exception as e:
        return {"status": "ERROR", "reason": str(e)}

def scan_file(file_path, enable_ai=False):
    findings = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if len(line) > 500: continue
                
                for name, pattern in SIGNATURES.items():
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        secret = match.group()
                        
                        # Grab context (2 lines before and after)
                        start_ctx = max(0, i - 2)
                        end_ctx = min(len(lines), i + 3)
                        context_snippet = "".join(lines[start_ctx:end_ctx])
                        
                        finding = {
                            "type": name,
                            "file": file_path,
                            "line": i + 1,
                            "secret_preview": secret[:4] + "..." + secret[-4:],
                            "context": context_snippet,
                            "ai_analysis": None
                        }
                        
                        if enable_ai:
                            finding['ai_analysis'] = call_ai_verifier(finding, context_snippet)
                            
                        findings.append(finding)
    except Exception:
        pass
    return findings

def scan_directory(root_dir, enable_ai=False):
    print(f"{Color.BLUE}⚡ Sentinel AI Scanner v2.0{Color.RESET}")
    if enable_ai and not get_api_key():
        print(f"{Color.RED}⚠️  AI Mode enabled but OPENAI_API_KEY not set. Falling back to regex.{Color.RESET}")
        enable_ai = False

    files_to_scan = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for f in filenames:
            if os.path.splitext(f)[1].lower() not in IGNORE_EXTENSIONS:
                files_to_scan.append(os.path.join(dirpath, f))

    total_findings = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(scan_file, f, enable_ai): f for f in files_to_scan}
        for future in futures:
            results = future.result()
            for res in results:
                total_findings += 1
                print(f"\n{Color.YELLOW}📂 {res['file']}:{res['line']} [{res['type']}]{Color.RESET}")
                print(f"   Context: {res['secret_preview']}")
                
                if res.get('ai_analysis') and 'verdict' in res['ai_analysis']:
                    ai = res['ai_analysis']
                    if ai['verdict'] == 'REAL':
                        print(f"   {Color.RED}🤖 AI VERDICT: REAL LEAK ({ai['confidence']}%){Color.RESET}")
                        print(f"   💡 Reason: {ai['reasoning']}")
                        print(f"   ✉️  Draft: {ai['draft_email']}")
                    else:
                        print(f"   {Color.GREEN}🤖 AI VERDICT: FALSE POSITIVE ({ai['confidence']}%){Color.RESET}")
                        print(f"   💡 Reason: {ai['reasoning']}")
                elif enable_ai:
                    print(f"   {Color.RED}🤖 AI Analysis Failed: {res['ai_analysis'].get('reason')}{Color.RESET}")

    print(f"\n{Color.GREEN}✔ Scan Complete. Total Potential Leaks: {total_findings}{Color.RESET}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".", help="Path to scan")
    parser.add_argument("--ai", action="store_true", help="Enable AI verification")
    args = parser.parse_args()
    scan_directory(args.path, args.ai)

if __name__ == "__main__":
    main()
