import requests, hashlib

BASE = "http://127.0.0.1:8000"
MAC = "AA:BB:CC:DD:EE:01"
USER = "rock_test"

# 1. Registrar rig
r = requests.post(f"{BASE}/register", params={"mac": MAC, "usuario_id": USER, "nombre": "Rock"})
print("register:", r.status_code, r.json())

# 2. Pedir job
r = requests.get(f"{BASE}/job", params={"mac": MAC})
job = r.json()
print("job:", job)

# 3. Minar (buscar nonce que cumpla la dificultad)
prev_hash = job["prev_hash"]
difficulty = job["difficulty"]
nonce = 0
while True:
    data = prev_hash + str(nonce)
    h = hashlib.sha256(data.encode()).hexdigest()
    if h.startswith("0" * difficulty):
        break
    nonce += 1

print(f"nonce encontrado: {nonce}, hash: {h}, intentos: {nonce}")

# 4. Enviar share
r = requests.post(f"{BASE}/submit", params={
    "mac": MAC, "job_id": job["job_id"], "nonce": nonce, "hash_result": h
})
print("submit:", r.status_code, r.json())

# 5. Ver perfil
r = requests.get(f"{BASE}/perfil/{USER}")
print("perfil:", r.json())

# 6. Ranking
r = requests.get(f"{BASE}/ranking")
print("ranking:", r.json())
