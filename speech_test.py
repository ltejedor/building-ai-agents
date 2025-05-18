# file: speak.py
import os, json, requests, pathlib, sys

API_KEY = os.getenv("RIME_API_KEY")
assert API_KEY, "RIME_API_KEY missing"

url = "https://users.rime.ai/v1/rime-tts"
payload = {
    "speaker": "arcana:expressive",   # pick any Arcana voice
    "text": " ".join(sys.argv[1:]) or "You've made your agent talk!",
    "modelId": "arcana"
}
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "audio/mp3",
    "Content-Type": "application/json"
}

out = pathlib.Path("agent-talk.mp3")
with requests.post(url, headers=headers, json=payload, stream=True) as r:
    r.raise_for_status()
    with out.open("wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

print(f"Saved {out}")
