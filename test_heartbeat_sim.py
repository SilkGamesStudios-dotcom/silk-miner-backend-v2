import requests

BASE = "http://127.0.0.1:8000"
USER = "rock5"

rigs = ["EE:01:01:01:01:01", "EE:02:02:02:02:02", "EE:03:03:03:03:03"]

for i, mac in enumerate(rigs):
    requests.post(f"{BASE}/register", params={"mac": mac, "usuario_id": USER})
    requests.post(f"{BASE}/rig/renombrar", params={"mac": mac, "usuario_id": USER, "nuevo_nombre": f"Rig {i+1}"})
    # simula hashrate distinto por rig
    requests.post(f"{BASE}/heartbeat", params={"mac": mac, "hashes_intentados": 4000 + i * 500, "segundos": 5})

r = requests.get(f"{BASE}/stats/live", params={"usuario_id": USER})
print(r.json())
