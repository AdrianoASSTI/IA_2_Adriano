# Relatório — API com Banco de Dados Cassandra (Astra DB)

**Disciplina:** Banco de Dados  
**Aluno:** Adriano  
**Data:** 18 de junho de 2026  

---

## 1. Objetivo

O objetivo desta atividade foi replicar o tutorial de uso do banco de dados Apache Cassandra por meio da plataforma DataStax Astra DB e, como etapa adicional, conectar-se à API REST do banco e retornar dados utilizando Python.

---

## 2. O que é o Apache Cassandra?

O Apache Cassandra é um banco de dados NoSQL distribuído, projetado para lidar com grandes volumes de dados com alta disponibilidade e sem ponto único de falha. Diferente dos bancos relacionais tradicionais (como MySQL e PostgreSQL), o Cassandra:

- Escala horizontalmente (adiciona mais máquinas em vez de melhorar uma só)
- É otimizado para escrita e leitura rápidas em grande escala
- Organiza os dados em **keyspaces** e **tabelas**, não em bancos e schemas
- Exige que a modelagem de dados seja pensada a partir das **consultas** que serão feitas, e não dos relacionamentos entre entidades

---

## 3. Ferramenta Utilizada: DataStax Astra DB

O **DataStax Astra DB** é uma plataforma gerenciada na nuvem que oferece o Apache Cassandra como serviço (DBaaS). Ela elimina a necessidade de instalar e configurar o Cassandra localmente, além de disponibilizar uma API REST para acesso remoto ao banco.

**Configurações utilizadas:**

| Parâmetro       | Valor                            |
|-----------------|----------------------------------|
| Nome do banco   | tutorial-cassandra-sensores      |
| Provedor        | Amazon Web Services (AWS)        |
| Região          | us-east-2                        |
| Keyspace padrão | default_keyspace                 |

---

## 4. Etapa 1 — Criação da Tabela via CQL Console

Após a criação e ativação do banco no painel do Astra DB, foi utilizado o **CQL Console** (interface de terminal para Cassandra Query Language) para executar os comandos.

### 4.1 Seleção do Keyspace

```sql
DESCRIBE KEYSPACES;
USE default_keyspace;
```

Um **keyspace** no Cassandra equivale a um banco de dados nos sistemas relacionais. O `default_keyspace` é o espaço padrão disponível após a criação do banco.

### 4.2 Criação da Tabela

```sql
CREATE TABLE IF NOT EXISTS leituras_sensor (
  sensor_id    text,
  data_leitura date,
  horario      timestamp,
  temperatura  decimal,
  umidade      decimal,
  status       text,
  PRIMARY KEY ((sensor_id, data_leitura), horario)
) WITH CLUSTERING ORDER BY (horario DESC);
```

**Explicação da chave primária:**

- `(sensor_id, data_leitura)` → **chave de partição**: define como os dados são distribuídos entre os nós do cluster. Todos os registros do mesmo sensor na mesma data ficam na mesma partição.
- `horario` → **chave de clustering**: define a ordenação dos registros dentro de cada partição (do mais recente para o mais antigo).

Essa estrutura foi escolhida para responder eficientemente à pergunta: *"Quais são as leituras de um sensor em uma determinada data?"*

### 4.3 Inserção de Dados

Foram inseridos 3 registros de sensores:

```sql
INSERT INTO leituras_sensor (sensor_id, data_leitura, horario, temperatura, umidade, status)
VALUES ('sensor-001', '2026-05-22', '2026-05-22 10:30:00', 25.4, 60.2, 'OK');

INSERT INTO leituras_sensor (sensor_id, data_leitura, horario, temperatura, umidade, status)
VALUES ('sensor-001', '2026-05-22', '2026-05-22 10:35:00', 25.7, 61.0, 'OK');

INSERT INTO leituras_sensor (sensor_id, data_leitura, horario, temperatura, umidade, status)
VALUES ('sensor-002', '2026-05-22', '2026-05-22 10:30:00', 28.1, 58.5, 'ALERTA');
```

### 4.4 Consulta dos Dados

```sql
-- Leituras do sensor-001
SELECT * FROM leituras_sensor
WHERE sensor_id = 'sensor-001'
  AND data_leitura = '2026-05-22'
LIMIT 10;

-- Leituras do sensor-002
SELECT * FROM leituras_sensor
WHERE sensor_id = 'sensor-002'
  AND data_leitura = '2026-05-22';
```

A consulta exige a **chave de partição completa** (`sensor_id` + `data_leitura`) porque o Cassandra não realiza varredura completa da tabela por padrão — ele vai diretamente à partição correta, tornando a busca extremamente eficiente.

---

## 5. Etapa 2 — Conexão via API REST com Python

O DataStax Astra DB disponibiliza uma **API REST** que permite consultar os dados remotamente por meio de requisições HTTP, sem necessidade do driver nativo do Cassandra.

### 5.1 Autenticação

Foi gerado um **token de acesso** com papel de *Database Administrator* no painel do Astra. Esse token é enviado no header de cada requisição HTTP:

```
X-Cassandra-Token: AstraCS:...
```

### 5.2 Endpoint da API

```
https://7aa96348-a36e-41d3-9124-151e489625d6-us-east-2.apps.astra.datastax.com
```

### 5.3 Código Python

```python
import requests

ASTRA_TOKEN    = "AstraCS:..."
ASTRA_ENDPOINT = "https://7aa96348-...-us-east-2.apps.astra.datastax.com"
KEYSPACE       = "default_keyspace"
TABELA         = "leituras_sensor"

headers = {
    "X-Cassandra-Token": ASTRA_TOKEN,
    "Content-Type": "application/json"
}

# Buscar todos os registros
url = f"{ASTRA_ENDPOINT}/api/rest/v2/keyspaces/{KEYSPACE}/{TABELA}/rows"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    dados = response.json()
    for row in dados.get("data", []):
        print(f"Sensor: {row['sensor_id']} | Temp: {row['temperatura']}°C | Status: {row['status']}")
```

### 5.4 Resultado Obtido

A execução do script retornou com sucesso os 3 registros inseridos:

```
✅ Conexão bem-sucedida! 3 registro(s) encontrado(s).

Sensor: sensor-001 | Data: 2026-05-22 | Temp: 25.7°C | Umidade: 61.0% | Status: OK
Sensor: sensor-001 | Data: 2026-05-22 | Temp: 25.4°C | Umidade: 60.2% | Status: OK
Sensor: sensor-002 | Data: 2026-05-22 | Temp: 28.1°C | Umidade: 58.5% | Status: ALERTA

--- Consulta específica: sensor-001 em 2026-05-22 ---
Horário: 2026-05-22T10:35:00Z | Temp: 25.7°C | Umidade: 61.0% | Status: OK
Horário: 2026-05-22T10:30:00Z | Temp: 25.4°C | Umidade: 60.2% | Status: OK

--- Consulta específica: sensor-002 em 2026-05-22 ---
Horário: 2026-05-22T10:30:00Z | Temp: 28.1°C | Umidade: 58.5% | Status: ALERTA
```

---

## 6. Cassandra vs. Banco Relacional

| Característica         | Banco Relacional (MySQL/PostgreSQL) | Apache Cassandra              |
|------------------------|--------------------------------------|-------------------------------|
| Modelagem              | Baseada em entidades e relacionamentos | Baseada nas consultas         |
| Escalabilidade         | Vertical (hardware mais potente)     | Horizontal (mais máquinas)    |
| Consulta sem chave     | Possível (com custo de performance)  | Não recomendado               |
| Ideal para             | Poucos dados, alta complexidade relacional | Grande volume, escrita constante |
| Joins                  | Suportado nativamente                | Não suportado                 |

---

## 7. Conclusão

A atividade permitiu compreender na prática o funcionamento do Apache Cassandra e suas diferenças em relação aos bancos relacionais. O ponto principal é que **a modelagem de dados no Cassandra é orientada pelas consultas**, não pelos relacionamentos entre entidades.

A integração via API REST com Python demonstrou como é possível consumir dados de um banco Cassandra remotamente de forma simples, utilizando apenas requisições HTTP com autenticação por token — sem necessidade de instalar drivers ou configurar conexões complexas.
