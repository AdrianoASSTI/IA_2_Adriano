import requests

ASTRA_TOKEN    = "AstraCS:AfFgzZlvQvLlUWKgyZFsnvqD:541f4f4355760fdc661d41efce3d78c85dbd1d3848e027da1ef829e71223b8e7"
ASTRA_ENDPOINT = "https://7aa96348-a36e-41d3-9124-151e489625d6-us-east-2.apps.astra.datastax.com"
KEYSPACE       = "default_keyspace"
TABELA         = "leituras_sensor"

headers = {
    "X-Cassandra-Token": ASTRA_TOKEN,
    "Content-Type": "application/json"
}

# ── 1. Buscar todos os registros ─────────────────────────
print("=" * 50)
print("  LEITURAS DOS SENSORES - Cassandra (Astra DB)")
print("=" * 50)

url = f"{ASTRA_ENDPOINT}/api/rest/v2/keyspaces/{KEYSPACE}/{TABELA}/rows"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    dados = response.json()
    registros = dados.get("data", [])
    print(f"\n✅ Conexão bem-sucedida! {len(registros)} registro(s) encontrado(s).\n")
    for row in registros:
        print(f"Sensor: {row['sensor_id']} | "
              f"Data: {row['data_leitura']} | "
              f"Temp: {row['temperatura']}°C | "
              f"Umidade: {row['umidade']}% | "
              f"Status: {row['status']}")
else:
    print(f"❌ Erro {response.status_code}: {response.text}")

# ── 2. Buscar apenas sensor-001 ──────────────────────────
print("\n" + "-" * 50)
print("  Consulta específica: sensor-001 em 2026-05-22")
print("-" * 50)

url2 = f"{ASTRA_ENDPOINT}/api/rest/v2/keyspaces/{KEYSPACE}/{TABELA}/sensor-001/2026-05-22"
response2 = requests.get(url2, headers=headers)

if response2.status_code == 200:
    dados2 = response2.json()
    for row in dados2.get("data", []):
        print(f"Horário: {row['horario']} | "
              f"Temp: {row['temperatura']}°C | "
              f"Umidade: {row['umidade']}% | "
              f"Status: {row['status']}")
else:
    print(f"Erro: {response2.status_code} - {response2.text}")

# ── 3. Buscar apenas sensor-002 ──────────────────────────
print("\n" + "-" * 50)
print("  Consulta específica: sensor-002 em 2026-05-22")
print("-" * 50)

url3 = f"{ASTRA_ENDPOINT}/api/rest/v2/keyspaces/{KEYSPACE}/{TABELA}/sensor-002/2026-05-22"
response3 = requests.get(url3, headers=headers)

if response3.status_code == 200:
    dados3 = response3.json()
    for row in dados3.get("data", []):
        print(f"Horário: {row['horario']} | "
              f"Temp: {row['temperatura']}°C | "
              f"Umidade: {row['umidade']}% | "
              f"Status: {row['status']}")
else:
    print(f"Erro: {response3.status_code} - {response3.text}")
