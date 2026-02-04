import requests
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

if not key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit(1)

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"

try:
    r = requests.get(url)
    if r.status_code == 200:
        models = r.json().get('models', [])
        print("AVAILABLE MODELS:")
        for m in models:
            if "gemini" in m['name']:
                print(f" - {m['name']} ({m.get('displayName')})")
    else:
        print(f"Error: {r.status_code} - {r.text}")
except Exception as e:
    print(f"Error: {e}")
