import subprocess
import os
import time
import sys

# Configuration
OMNI_CMD = ["venv/bin/python3", "omni.py"]
ENV = os.environ.copy()
ENV["OMNI_HEADLESS"] = "true"
TIMEOUT = 300  # 5 minutes per test

TESTS = [
    {
        "name": "Snake Game",
        "prompt": "Make a single-file HTML snake game that looks like a Matrix simulation. Include '<!-- filename: public/matrix_snake.html -->' at the top.",
        "expected_file": "public/matrix_snake.html",
        "validation": lambda content: "canvas" in content and "script" in content
    },
    {
        "name": "Stock Dashboard",
        "prompt": "Create a React component 'StockDash.jsx' that shows a mock stock chart using Recharts. Include '# filename: public/StockDash.jsx'. Also create a python script 'stock_api.py' to serve data. Include '# filename: public/stock_api.py'.",
        "expected_file": "public/StockDash.jsx",
        "validation": lambda content: "Recharts" in content or "recharts" in content
    },
    {
        "name": "File Deduplicator",
        "prompt": "Write a python script to find duplicate files in the current directory based on hash. Include '# filename: public/dedup.py'.",
        "expected_file": "public/dedup.py",
        "validation": lambda content: "hashlib" in content and "os.walk" in content
    }
]

def run_test(test):
    print(f"Running Test: {test['name']}...")
    start_time = time.time()
    
    # Ensure public dir exists
    os.makedirs("public", exist_ok=True)
    
    # Run Omni
    try:
        proc = subprocess.run(
            OMNI_CMD + [test["prompt"]],
            env=ENV,
            capture_output=True,
            text=True,
            timeout=TIMEOUT
        )
        print(proc.stdout)
        if proc.returncode != 0:
            print(f"❌ Omni failed with code {proc.returncode}")
            print(proc.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ Timed out after {TIMEOUT}s")
        return False

    # Check File
    if os.path.exists(test["expected_file"]):
        with open(test["expected_file"], "r") as f:
            content = f.read()
            if test["validation"](content):
                print(f"✅ PASS: {test['name']}")
                return True
            else:
                print(f"❌ FAIL: File content validation failed for {test['expected_file']}")
                return False
    else:
        print(f"❌ FAIL: File {test['expected_file']} not created.")
        return False

def main():
    results = []
    print("Starting Benchmark Suite...")
    
    for test in TESTS:
        success = run_test(test)
        results.append((test["name"], "PASS" if success else "FAIL"))
        print("-" * 40)

    # Report
    with open("BENCHMARK.md", "a") as f:
        f.write("\n## Automated Run Results\n")
        for name, status in results:
            f.write(f"- **{name}:** {status}\n")
    
    print("\nFinal Results:")
    for name, status in results:
        print(f"{name}: {status}")

if __name__ == "__main__":
    main()
