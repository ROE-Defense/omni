#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import fnmatch

# cpack.py - Context Packer for LLMs
# Version: 1.0.0 (MVP)
# Built by: Vector (Aurelius Swarm)

def load_gitignore(root_dir):
    """
    Load .gitignore patterns from the root directory.
    Returns a list of patterns.
    """
    gitignore_path = os.path.join(root_dir, '.gitignore')
    patterns = [
        '.git', '.git/*', 
        '__pycache__', '__pycache__/*', 
        '*.pyc', 
        'node_modules', 'node_modules/*',
        '.DS_Store',
        '*.enc', # Security: ignore encrypted keys
        '*.pem', # Security: ignore keys
        '*.jpg', '*.png', '*.gif', '*.ico', # Ignore binaries/images
        'package-lock.json', 'yarn.lock' # Reduce noise
    ]
    
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.append(line)
        except Exception as e:
            sys.stderr.write(f"Warning: Could not read .gitignore: {e}\n")
            
    return patterns

def is_ignored(path, patterns, root_dir):
    """
    Check if a path matches any gitignore pattern.
    Very basic implementation of gitignore matching.
    """
    rel_path = os.path.relpath(path, root_dir)
    name = os.path.basename(path)
    
    for pattern in patterns:
        # Normalize pattern
        if pattern.endswith('/'):
            pattern = pattern[:-1]
            
        # Check match against relative path or filename
        if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(name, pattern):
            return True
        
        # Check directory prefix matching (e.g. node_modules/file.js should match node_modules)
        if pattern in rel_path.split(os.sep):
             return True
             
    return False

def is_binary(file_path):
    """Check if file is binary."""
    try:
        with open(file_path, 'tr') as check_file:
            check_file.read(1024)
            return False
    except:
        return True

def copy_to_clipboard(text):
    """Copy text to clipboard using pbcopy (macOS)."""
    try:
        process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
        return True
    except Exception as e:
        return False

def pack_context(root_dir, output_file=None, clipboard=False):
    """
    Walk directory, read files, and pack into Markdown format.
    """
    patterns = load_gitignore(root_dir)
    packed_content = []
    file_count = 0
    total_chars = 0
    
    tree_structure = []

    # First pass: Generate tree
    packed_content.append(f"# Project Context: {os.path.basename(os.path.abspath(root_dir))}\n")
    packed_content.append("## File Tree\n```text")
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter directories in place
        dirnames[:] = [d for d in dirnames if not is_ignored(os.path.join(dirpath, d), patterns, root_dir)]
        
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            if not is_ignored(full_path, patterns, root_dir):
                rel_path = os.path.relpath(full_path, root_dir)
                tree_structure.append(rel_path)

    packed_content.append("\n".join(tree_structure))
    packed_content.append("```\n\n## File Contents\n")

    # Second pass: Read content
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter directories in place
        dirnames[:] = [d for d in dirnames if not is_ignored(os.path.join(dirpath, d), patterns, root_dir)]
        
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            if is_ignored(full_path, patterns, root_dir):
                continue
                
            if is_binary(full_path):
                continue
                
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f_obj:
                    content = f_obj.read()
                    rel_path = os.path.relpath(full_path, root_dir)
                    ext = os.path.splitext(f)[1].lstrip('.')
                    if not ext: ext = 'text'
                    
                    packed_content.append(f"### {rel_path}\n```{ext}\n{content}\n```\n")
                    file_count += 1
                    total_chars += len(content)
            except Exception as e:
                print(f"Skipping {f}: {e}")

    final_output = "\n".join(packed_content)
    
    print(f"Packed {file_count} files.")
    print(f"Total characters: {total_chars}")
    print(f"Estimated tokens (approx): {total_chars // 4}")

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_output)
        print(f"Output saved to: {output_file}")
    
    if clipboard:
        if copy_to_clipboard(final_output):
            print("Successfully copied to clipboard! 📋")
        else:
            print("Clipboard copy failed (pbcopy not found or error).")
    elif not output_file:
        # Print to stdout if no other output selected
        print("\n" + "="*40 + "\n")
        print(final_output)

def main():
    parser = argparse.ArgumentParser(description="Pack project files into a single context for LLMs.")
    parser.add_argument("path", nargs="?", default=".", help="Root directory to pack (default: current)")
    parser.add_argument("-o", "--output", help="Output file path (e.g., context.md)")
    parser.add_argument("-c", "--clipboard", action="store_true", help="Copy output to clipboard")
    
    args = parser.parse_args()
    
    pack_context(args.path, args.output, args.clipboard)

if __name__ == "__main__":
    main()
