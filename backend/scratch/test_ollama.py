import requests
try:
    resp = requests.get("http://localhost:11434/api/tags", timeout=5)
    print(f"Ollama Status: {resp.status_code}")
    print(f"Models: {[m['name'] for m in resp.json()['models']]}")
except Exception as e:
    print(f"Error: {e}")
