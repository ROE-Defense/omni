import os
import re
import subprocess
import sys
import time
import logging

LOG_FILE = "/tmp/omni_executor.log"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s - %(message)s')

WORKSPACE_DIR = os.path.expanduser("~/.omni/workspace")
try:
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
except:
    WORKSPACE_DIR = "/tmp/omni_workspace"
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

class AutoExecutor:
    def __init__(self):
        self.active_process = None

    def process(self, text: str) -> dict:
        matches = re.findall(r'```\s*([\w\+\-\.]+)?\s*\n?(.*?)```', text, re.DOTALL)
        clean_text = re.sub(r'```\s*(\w+)?\n(.*?)```', '', text, flags=re.DOTALL).strip()
        if not clean_text: clean_text = "Task completed."

        artifacts = []
        last_saved_file = None 

        for i, (lang, code) in enumerate(matches):
            lang = lang.lower().strip() if lang else "txt"
            filename = self._get_filename(code, lang)
            filepath = os.path.join(WORKSPACE_DIR, filename)
            
            # Is this really a script?
            is_executable = filename.endswith(".sh")
            
            try:
                with open(filepath, "w") as f: f.write(code)
                artifacts.append({
                    "filename": filename,
                    "lang": lang,
                    "path": filepath,
                    "content": code
                })
                last_saved_file = filepath 
                logging.info(f"Saved: {filepath}")
            except Exception as e:
                logging.error(f"Save failed: {e}")

            if is_executable:
                if last_saved_file and not last_saved_file.endswith(".sh"):
                    # Smart Repair Logic
                    referenced_py = re.search(r'python3? \s*([\w\.-]+)', code)
                    if referenced_py:
                        ref_file = referenced_py.group(1)
                        ref_path = os.path.join(WORKSPACE_DIR, ref_file)
                        if not os.path.exists(ref_path):
                            code = code.replace(ref_file, os.path.basename(last_saved_file))
                            # Update the file on disk
                            with open(filepath, "w") as f: f.write(code)

                # We don't auto-execute here anymore (we wait for UI launch), 
                # but we could mark it as the entry point if we wanted.
                # Since the UI finds the entry point, we just save it.

        return {
            "text": clean_text,
            "artifacts": artifacts
        }

    def _get_filename(self, code, lang):
        match = re.search(r'#\s*filename:\s*([\w\.-]+)', code)
        if match: return match.group(1)
        match_js = re.search(r'//\s*filename:\s*([\w\.-]+)', code)
        if match_js: return match_js.group(1)
        
        stripped = code.strip()
        
        # Heuristics
        if "==" in stripped and not "if " in stripped:
            return "requirements.txt"
        if stripped.startswith('{') or stripped.startswith('['):
            return "package.json" if "dependencies" in stripped else f"data_{int(time.time())}.json"
        if "import " in stripped or "def " in stripped:
            return f"generated_{int(time.time())}.py"
        if "npm install" in stripped or "pip install" in stripped or stripped.startswith("#!/bin/bash"):
            return f"launch_{int(time.time())}.sh"
        
        ext = "py" if lang in ["python", "py"] else lang
        if lang == "bash": ext = "sh"
        if lang in ["js", "javascript", "jsx"]: ext = "js"
        if lang == "json": ext = "json"
        if lang == "flask": ext = "txt" # Fix for model hallucinating 'flask' lang for requirements
        
        timestamp = int(time.time())
        return f"generated_{timestamp}.{ext}"

    def _run_python(self, filepath):
        return self._run_bash(f"python3 {filepath}")

    def _run_bash(self, command_or_path):
        try:
            is_file = os.path.exists(command_or_path)
            if is_file:
                target_script = command_or_path
            else:
                target_script = os.path.join(WORKSPACE_DIR, "temp_run.sh")
                with open(target_script, "w") as f: f.write(command_or_path)
            
            launcher_path = target_script + ".command"
            venv_bin = os.path.abspath("./venv/bin")
            
            with open(launcher_path, "w") as f:
                f.write("#!/bin/bash\n")
                f.write(f'export PATH="{venv_bin}:$PATH"\n')
                f.write(f'cd "{WORKSPACE_DIR}"\n')
                f.write("echo '🚀 Omni Executor: Preparing Environment...'\n")
                
                if os.path.exists(os.path.join(WORKSPACE_DIR, "requirements.txt")):
                    f.write("echo '📦 Installing Python dependencies...'\n")
                    f.write("pip install -r requirements.txt\n")
                
                if os.path.exists(os.path.join(WORKSPACE_DIR, "package.json")):
                     # Don't install if node_modules exists to save time, unless forced
                    if not os.path.exists(os.path.join(WORKSPACE_DIR, "node_modules")):
                        f.write("echo '📦 Installing Node dependencies...'\n")
                        f.write("npm install\n")

                if is_file: f.write(f'bash "{target_script}"\n')
                else: f.write(f'bash "{target_script}"\n')

                f.write('echo "\n[Process completed. Press Enter to close]"\n')
                f.write('read\n')
            
            os.chmod(launcher_path, 0o755)
            subprocess.Popen(["open", launcher_path])
            return f"🚀 Executed: {os.path.basename(launcher_path)}"
        except Exception as e:
            return f"❌ Launch Failed: {e}"
