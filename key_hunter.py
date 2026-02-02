#!/usr/bin/env python3
import os
import sys
import re
import argparse
import time
from concurrent.futures import ThreadPoolExecutor

# key-hunter.py - White Hat Credential Scanner
# Built by: Sentinel (Aurelius Systems)
# Version: 1.0.0

# Regex Signatures (Publicly known patterns)
SIGNATURES = {
    "AWS Access Key": r"(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
    "Google API Key": r"AIza[0-9A-Za-z\\-_]{35}",
    "Slack Token": r"(xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})",
    "Stripe Secret": r"(sk_live_[0-9a-zA-Z]{24})",
    "OpenAI API Key": r"(sk-[a-zA-Z0-9]{48}|sk-proj-[a-zA-Z0-9]{48})",
    "GitHub Token": r"(ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59})",
    "Private Key (PEM)": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
    "Generic Secret": r"(api_key|access_token|secret_key|password)\s*[:=]\s*['\"][a-zA-Z0-9_\\-]{20,}['\"]"
}

IGNORE_DIRS = {
    '.git', 'node_modules', '__pycache__', 'venv', 'env', '.idea', '.vscode'
}

IGNORE_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip', '.tar', '.gz', '.mp4', '.mp3',
    '.lock', '.svg', '.woff', '.woff2', '.ttf', '.eot', '.exe', '.dll', '.so', '.dylib', '.class'
}

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def scan_file(file_path):
    findings = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                # Skip massive lines (minified code)
                if len(line) > 500:
                    continue
                
                for name, pattern in SIGNATURES.items():
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        secret = match.group()
                        # Redact sensitive part for display
                        redacted = secret[:4] + "*" * (len(secret) - 8) + secret[-4:] if len(secret) > 8 else "***"
                        findings.append({
                            "type": name,
                            "line": i + 1,
                            "secret_preview": redacted,
                            "raw_match": secret # In a real run, never log this to disk unencrypted
                        })
    except Exception as e:
        # sys.stderr.write(f"Error reading {file_path}: {e}\n")
        pass
    return findings

def scan_directory(root_dir):
    start_time = time.time()
    scanned_files = 0
    total_findings = 0
    
    print(f"{Color.BLUE}⚡ Scanning directory: {root_dir}{Color.RESET}")
    print(f"{Color.BLUE}ℹ️  Signatures loaded: {len(SIGNATURES)}{Color.RESET}\n")

    files_to_scan = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Ignore dirs
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in IGNORE_EXTENSIONS:
                continue
            files_to_scan.append(os.path.join(dirpath, f))

    # Parallel Scan
    results = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_file = {executor.submit(scan_file, f): f for f in files_to_scan}
        for future in future_to_file:
            f = future_to_file[future]
            scanned_files += 1
            findings = future.result()
            if findings:
                results[f] = findings
                total_findings += len(findings)

    # Report
    for f, findings in results.items():
        print(f"{Color.YELLOW}📂 {f}{Color.RESET}")
        for find in findings:
            print(f"  {Color.RED}✖  FOUND: {find['type']}{Color.RESET} at line {find['line']}")
            print(f"     Preview: {find['secret_preview']}")
        print("")

    duration = time.time() - start_time
    print(f"{Color.GREEN}✔ Scan Complete.{Color.RESET}")
    print(f"  Files: {scanned_files}")
    print(f"  Findings: {total_findings}")
    print(f"  Time: {duration:.2f}s")

def main():
    parser = argparse.ArgumentParser(description="Sentinel: White Hat Credential Scanner")
    parser.add_argument("path", nargs="?", default=".", help="Directory to scan")
    args = parser.parse_args()
    
    scan_directory(args.path)

if __name__ == "__main__":
    main()
