# A1 Pulse - Requisitos Baseline (v0.1)

**Empresa:** A1 Lab
**Produto:** A1 Pulse
**Versão:** 0.1 (Baseline - sem otimizações)
**Objetivo:** Criar a versão mais simples possível da aplicação para estabelecer baseline de performance

---

## 1. Visão Geral

A1 Pulse é uma plataforma de observabilidade simplificada que permite empresas:
- Rastrear eventos de usuários (analytics)
- Coletar logs de aplicações (debugging)
- Visualizar dados através de queries

**Esta é a versão BASELINE**: implementação mais simples e direta, sem nenhuma otimização. O objetivo é medir a performance inicial e, nos próximos episódios, aplicar otimizações incrementais.

---

## 2. Requisitos Funcionais

### 2.1 Autenticação e Usuários

**RF-001:** Sistema deve permitir registro de usuários
- Entrada: email, password
- Saída: user_id, JWT token
- Validação: email único, password mínimo 8 caracteres

**RF-002:** Sistema deve permitir login de usuários
- Entrada: email, password
- Saída: JWT token (validade: 24h)
- Validação: credenciais corretas

**RF-003:** Sistema deve validar JWT em todas requisições protegidas
- Header: `Authorization: Bearer <token>`
- Extrair `user_id` do token
- Rejeitar tokens expirados ou inválidos

### 2.2 Projetos

**RF-004:** Usuário pode criar projetos
- Entrada: nome do projeto
- Saída: project_id, api_key (gerada automaticamente)
- Limite: sem limite de projetos por usuário (por enquanto)

**RF-005:** Usuário pode listar seus projetos
- Saída: lista de projetos com (id, name, api_key, created_at)
- Filtro: apenas projetos do usuário autenticado

**RF-006:** Usuário pode deletar seus projetos
- Validação: usuário é dono do projeto
- Ação: delete cascade (remove eventos e logs)

### 2.3 Ingestão de Eventos

**RF-007:** Sistema deve aceitar eventos individuais via API
- Autenticação: X-API-Key header
- Entrada: `{name, properties (json), session_id (opcional)}`
- Ação: INSERT direto no banco (sem buffer, sem batch)
- Resposta: 201 Created

**RF-008:** Sistema deve aceitar batch de eventos
- Autenticação: X-API-Key header
- Entrada: `{events: [{...}, {...}, ...]}`
- Ação: INSERT de todos eventos (um por vez, sem otimização)
- Resposta: 201 Created

### 2.4 Ingestão de Logs

**RF-009:** Sistema deve aceitar logs individuais via API
- Autenticação: X-API-Key header
- Entrada: `{level, message, metadata (json)}`
- Levels permitidos: debug, info, warn, error
- Ação: INSERT direto no banco
- Resposta: 201 Created

**RF-010:** Sistema deve aceitar batch de logs
- Autenticação: X-API-Key header
- Entrada: `{logs: [{...}, {...}, ...]}`
- Ação: INSERT de todos logs (um por vez)
- Resposta: 201 Created

### 2.5 Analytics (Leitura de Eventos)

**RF-011:** Usuário pode consultar contagem total de eventos
- Autenticação: JWT
- Entrada: project_id, start_date, end_date, name (opcional)
- Saída: `{count: number}`
- Query: SELECT COUNT(*) com filtros

**RF-012:** Usuário pode consultar top eventos
- Autenticação: JWT
- Entrada: project_id, start_date, end_date, limit
- Saída: `[{name, count}, ...]` ordenado por count DESC
- Query: GROUP BY name, COUNT(*), ORDER BY count DESC

**RF-013:** Usuário pode consultar timeseries de eventos
- Autenticação: JWT
- Entrada: project_id, start_date, end_date, interval (hour/day), name (opcional)
- Saída: `[{timestamp, count}, ...]`
- Query: DATE_TRUNC + GROUP BY + ORDER BY timestamp

### 2.6 Logs (Leitura)

**RF-014:** Usuário pode listar logs com filtros
- Autenticação: JWT
- Entrada: project_id, start_date, end_date, level (opcional), limit, offset
- Saída: `{logs: [{id, level, message, metadata, created_at}], total: number}`
- Query: SELECT com WHERE + ORDER BY created_at DESC + LIMIT/OFFSET

**RF-015:** Usuário pode ver estatísticas de logs
- Autenticação: JWT
- Entrada: project_id, start_date, end_date
- Saída: `{total, by_level: {debug: n, info: n, warn: n, error: n}}`
- Query: COUNT(*) + GROUP BY level

---

## 3. Requisitos Não-Funcionais

### 3.1 Baseline (Sem Otimizações)

**RNF-001:** Todas as queries devem ser executadas de forma síncrona e direta
- Sem connection pooling customizado (usar padrão do driver)
- Sem prepared statements (queries inline)
- Sem caching (nem em memória, nem Redis)
- Sem batch inserts otimizados (loop de INSERTs individuais)

**RNF-002:** Autenticação deve ser validada em cada requisição
- JWT parsing e validação a cada request
- Sem caching de validação
- Sem rate limiting

**RNF-003:** Ambiente de execução limitado
- Servidor: máximo 2GB RAM
- CPU: limitado (definir nos testes)
- Postgres: configuração padrão, sem tuning
- Sem Redis ou cache externo
- Sem load balancer

**RNF-004:** Métricas devem ser coletadas
- Request/sec (reads e writes separados)
- Latência (P50, P95, P99)
- Erro rate
- CPU e memória do servidor
- Conexões ativas no Postgres

### 3.2 Constraints

**RNF-005:** Limites iniciais (podem estourar, é esperado!)
- Sem limite de requisições por segundo
- Sem limite de tamanho de payload (além do razoável: max 10MB)
- Sem timeout customizado (usar padrão: 30s)

---

## 4. Schema do Banco de Dados

```sql
-- Versão mais simples possível, sem otimizações

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    api_key VARCHAR(64) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    properties JSONB,
    session_id VARCHAR(64),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE logs (
    id BIGSERIAL PRIMARY KEY,
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    level VARCHAR(10) NOT NULL,
    message TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índices MÍNIMOS (apenas PKs e FKs automáticos)
-- SEM índices customizados na baseline!
-- Vamos adicionar nos episódios de otimização
```

**IMPORTANTE:** Não criar índices adicionais! Queremos ver o baseline sem otimizações.

---

## 5. API Endpoints

### 5.1 Autenticação

```
POST /api/v1/auth/register
Body: {
    "email": "user@example.com",
    "password": "password123"
}
Response: 201 {
    "user_id": "uuid",
    "token": "jwt-token"
}

POST /api/v1/auth/login
Body: {
    "email": "user@example.com",
    "password": "password123"
}
Response: 200 {
    "token": "jwt-token"
}
```

### 5.2 Projetos

```
GET /api/v1/projects
Header: Authorization: Bearer <token>
Response: 200 {
    "projects": [
        {
            "id": "uuid",
            "name": "My App",
            "api_key": "key",
            "created_at": "timestamp"
        }
    ]
}

POST /api/v1/projects
Header: Authorization: Bearer <token>
Body: {
    "name": "My App"
}
Response: 201 {
    "id": "uuid",
    "name": "My App",
    "api_key": "generated-key",
    "created_at": "timestamp"
}

DELETE /api/v1/projects/:id
Header: Authorization: Bearer <token>
Response: 204
```

### 5.3 Ingestão

```
POST /api/v1/ingest/events
Header: X-API-Key: <api-key>
Body: {
    "name": "page_view",
    "properties": {
        "page": "/home",
        "browser": "chrome"
    },
    "session_id": "abc123"
}
Response: 201

POST /api/v1/ingest/events/batch
Header: X-API-Key: <api-key>
Body: {
    "events": [
        {
            "name": "page_view",
            "properties": {"page": "/home"},
            "session_id": "abc123"
        },
        {
            "name": "button_click",
            "properties": {"button": "signup"},
            "session_id": "abc123"
        }
    ]
}
Response: 201

POST /api/v1/ingest/logs
Header: X-API-Key: <api-key>
Body: {
    "level": "error",
    "message": "Database connection failed",
    "metadata": {
        "endpoint": "/api/users",
        "duration_ms": 5000
    }
}
Response: 201

POST /api/v1/ingest/logs/batch
Header: X-API-Key: <api-key>
Body: {
    "logs": [
        {
            "level": "info",
            "message": "Request processed",
            "metadata": {"duration_ms": 100}
        },
        {
            "level": "error",
            "message": "Error occurred",
            "metadata": {"error": "timeout"}
        }
    ]
}
Response: 201
```

### 5.4 Analytics

```
GET /api/v1/analytics/:project_id/events/count
Header: Authorization: Bearer <token>
Query: ?start=2024-01-01T00:00:00Z&end=2024-01-31T23:59:59Z&name=page_view
Response: 200 {
    "count": 123456
}

GET /api/v1/analytics/:project_id/events/top
Header: Authorization: Bearer <token>
Query: ?start=2024-01-01T00:00:00Z&end=2024-01-31T23:59:59Z&limit=10
Response: 200 {
    "events": [
        {"name": "page_view", "count": 5000},
        {"name": "button_click", "count": 3000}
    ]
}

GET /api/v1/analytics/:project_id/events/timeseries
Header: Authorization: Bearer <token>
Query: ?start=2024-01-01T00:00:00Z&end=2024-01-31T23:59:59Z&interval=hour&name=page_view
Response: 200 {
    "data": [
        {"timestamp": "2024-01-01T00:00:00Z", "count": 100},
        {"timestamp": "2024-01-01T01:00:00Z", "count": 150}
    ]
}
```

### 5.5 Logs

```
GET /api/v1/logs/:project_id
Header: Authorization: Bearer <token>
Query: ?start=2024-01-01T00:00:00Z&end=2024-01-31T23:59:59Z&level=error&limit=100&offset=0
Response: 200 {
    "logs": [
        {
            "id": 1,
            "level": "error",
            "message": "Database connection failed",
            "metadata": {"endpoint": "/api/users"},
            "created_at": "2024-01-15T10:30:00Z"
        }
    ],
    "total": 5000
}

GET /api/v1/logs/:project_id/stats
Header: Authorization: Bearer <token>
Query: ?start=2024-01-01T00:00:00Z&end=2024-01-31T23:59:59Z
Response: 200 {
    "total": 100000,
    "by_level": {
        "debug": 50000,
        "info": 30000,
        "warn": 15000,
        "error": 5000
    }
}
```

---

## 6. Stack Tecnológica (Baseline)

- **Linguagem:** Go 1.21+
- **Framework Web:** Gin (ou net/http puro se preferir)
- **Banco de Dados:** PostgreSQL 16 (configuração padrão, sem tuning)
- **Driver DB:** pgx (modo mais simples, sem pooling customizado)
- **Autenticação:** JWT (golang-jwt/jwt)
- **Password Hash:** bcrypt
- **Ambiente:** Docker Compose

**Sem usar:**
- ❌ Redis (sem cache)
- ❌ Message queues (sem async processing)
- ❌ Connection pooling customizado
- ❌ Prepared statements (baseline)
- ❌ Batch inserts otimizados
- ❌ GORM ou ORMs (SQL puro)

---

## 7. Testes de Performance

### 7.1 Objetivo

Medir a performance BASELINE do sistema sob carga mista (write + read simultâneos), simulando uso real onde:
- Aplicações enviam eventos/logs constantemente (writes)
- Usuários consultam dashboards simultaneamente (reads)

**Importante:** Queremos que o sistema SOFRA e mostre seus limites. Isso é o esperado!

### 7.2 Ambiente de Teste

```yaml
Servidor:
  - CPU: 2 cores
  - RAM: 2GB
  - Disco: SSD
  - OS: Linux (Docker)

Postgres:
  - RAM: 512MB (limite do container)
  - Configuração: padrão (postgresql.conf sem modificações)
  - max_connections: 100 (padrão)

Load Generator:
  - Ferramenta: k6
  - Localização: mesma máquina (eliminar latência de rede)
```

### 7.3 Cenários de Teste

#### Cenário 1: Write Only (Baseline de Ingestão)

**Objetivo:** Medir quantos eventos/logs por segundo o sistema aguenta receber.

```javascript
// k6: write-only.js
export let options = {
  scenarios: {
    events: {
      executor: 'constant-arrival-rate',
      rate: 100,              // 100 req/s
      timeUnit: '1s',
      duration: '5m',
      preAllocatedVUs: 50,
      maxVUs: 100,
    },
    logs: {
      executor: 'constant-arrival-rate',
      rate: 50,               // 50 req/s
      timeUnit: '1s',
      duration: '5m',
      preAllocatedVUs: 25,
      maxVUs: 50,
    }
  }
};
```

**Métricas esperadas:**
- Throughput: ? req/s (descobrir)
- Latência P95: ? ms
- Erro rate: < 1%
- Postgres connections: ?
- CPU: %
- Memória: MB

**Variações:**
1. **100 req/s** (warm up)
2. **500 req/s** (stress)
3. **1000 req/s** (breaking point)
4. **2000 req/s** (além do limite - esperamos falhas!)

#### Cenário 2: Read Only (Baseline de Queries)

**Objetivo:** Medir performance de queries analíticas com banco populado (1M+ eventos, 500k+ logs).

```javascript
// k6: read-only.js
export let options = {
  scenarios: {
    analytics_count: {
      executor: 'constant-arrival-rate',
      rate: 10,
      timeUnit: '1s',
      duration: '3m',
      preAllocatedVUs: 10,
    },
    analytics_top: {
      executor: 'constant-arrival-rate',
      rate: 10,
      timeUnit: '1s',
      duration: '3m',
      preAllocatedVUs: 10,
    },
    analytics_timeseries: {
      executor: 'constant-arrival-rate',
      rate: 5,                // Mais pesada
      timeUnit: '1s',
      duration: '3m',
      preAllocatedVUs: 10,
    },
    logs_list: {
      executor: 'constant-arrival-rate',
      rate: 10,
      timeUnit: '1s',
      duration: '3m',
      preAllocatedVUs: 10,
    },
    logs_stats: {
      executor: 'constant-arrival-rate',
      rate: 5,
      timeUnit: '1s',
      duration: '3m',
      preAllocatedVUs: 10,
    }
  }
};
```

**Métricas esperadas:**
- Latência P50: ? ms
- Latência P95: ? ms
- Latência P99: ? ms (queries pesadas)
- Throughput: ? req/s
- CPU: %
- Query duration (EXPLAIN ANALYZE)

**Variações de dataset:**
1. 100k eventos (pequeno)
2. 1M eventos (médio)
3. 10M eventos (grande - vai sofrer!)

#### Cenário 3: Mixed Load (REALISTA - PRINCIPAL) 🎯

**Objetivo:** Simular carga real com writes e reads simultâneos.

**Proporção realista:**
- 70% writes (ingestão constante)
- 30% reads (dashboards sendo consultados)

```javascript
// k6: mixed-load.js
export let options = {
  scenarios: {
    // WRITES (70% da carga)
    ingest_events: {
      executor: 'constant-arrival-rate',
      rate: 70,               // 70 req/s
      timeUnit: '1s',
      duration: '10m',
      preAllocatedVUs: 50,
      exec: 'ingestEvent',
    },
    ingest_logs: {
      executor: 'constant-arrival-rate',
      rate: 30,               // 30 req/s
      timeUnit: '1s',
      duration: '10m',
      preAllocatedVUs: 20,
      exec: 'ingestLog',
    },

    // READS (30% da carga)
    read_analytics: {
      executor: 'constant-arrival-rate',
      rate: 20,               // 20 req/s
      timeUnit: '1s',
      duration: '10m',
      preAllocatedVUs: 15,
      exec: 'queryAnalytics',
    },
    read_logs: {
      executor: 'constant-arrival-rate',
      rate: 10,               // 10 req/s
      timeUnit: '1s',
      duration: '10m',
      preAllocatedVUs: 10,
      exec: 'queryLogs',
    },
  }
};

export function ingestEvent() {
  // POST /ingest/events
}

export function ingestLog() {
  // POST /ingest/logs
}

export function queryAnalytics() {
  // GET /analytics/:id/events/timeseries (query pesada!)
}

export function queryLogs() {
  // GET /logs/:id?level=error
}
```

**Fases do teste:**

```javascript
Fase 1: Ramp-up (2 min)
  - 0 → 130 req/s total (100 write + 30 read)

Fase 2: Sustain (5 min)
  - 130 req/s constante

Fase 3: Spike (1 min)
  - 130 → 300 req/s (simular pico de tráfego)

Fase 4: Sustain High (2 min)
  - 300 req/s constante (vai sofrer!)

Fase 5: Ramp-down (1 min)
  - 300 → 0 req/s
```

**Métricas críticas:**
- ✅ Throughput real alcançado (req/s)
- ✅ Latência P95 (writes vs reads separados)
- ✅ Erro rate (%) por endpoint
- ✅ Database connection pool exhaustion
- ✅ CPU utilization (%)
- ✅ Memory usage (MB)
- ✅ Postgres slow queries (> 1s)
- ✅ Request queue time
- ✅ Time to first byte (TTFB)

#### Cenário 4: Burst Traffic (Pico)

**Objetivo:** Simular carga de pico repentino (ex: produto viralizou, dashboard aberto em telão).

```javascript
export let options = {
  stages: [
    { duration: '30s', target: 50 },    // Normal
    { duration: '10s', target: 500 },   // PICO REPENTINO!
    { duration: '1m', target: 500 },    // Sustentar pico
    { duration: '30s', target: 50 },    // Volta ao normal
  ],
};
```

**Expectativa:** Sistema vai sofrer, mas deve:
- Não crashar
- Retornar erros 429/503 (em vez de timeout)
- Recuperar quando carga diminuir

#### Cenário 5: Endurance Test (Longevidade)

**Objetivo:** Verificar memory leaks, connection leaks, degradação ao longo do tempo.

```javascript
export let options = {
  stages: [
    { duration: '1h', target: 100 },    // Carga moderada por 1 hora
  ],
};
```

**Métricas observadas:**
- Memória cresce linearmente? (leak!)
- Conexões DB aumentam? (leak!)
- Latência aumenta com o tempo? (degradação!)
- Disco cresce? (logs não rotacionados?)

### 7.4 Métricas e Coleta

#### Ferramentas:

```yaml
k6:
  - Métricas de carga (req/s, latência, erros)
  - Output: InfluxDB + Grafana (dashboard em tempo real)

Prometheus + Node Exporter:
  - CPU, memória, disco, network do servidor

Postgres:
  - pg_stat_statements (query performance)
  - pg_stat_activity (conexões ativas)
  - EXPLAIN ANALYZE (query plans)

Custom Metrics (app):
  - Histogram de latência por endpoint
  - Counter de requisições por tipo
  - Gauge de conexões DB ativas
```

#### Dashboard Grafana (ao vivo durante testes):

```
┌─────────────────────────────────────┐
│  A1 Pulse - Baseline Performance   │
├─────────────────────────────────────┤
│ Requests/sec:  [ 147 req/s ]        │
│   - Writes:     102 req/s (69%)     │
│   - Reads:       45 req/s (31%)     │
│                                      │
│ Latency P95:   [ 450ms ]            │
│   - Writes:     120ms               │
│   - Reads:     1200ms (!) ⚠️         │
│                                      │
│ Error Rate:    [ 2.3% ] ⚠️           │
│                                      │
│ Database:                            │
│   - Connections: 87/100 🟡          │
│   - Slow queries: 23                │
│   - Deadlocks: 0                    │
│                                      │
│ System:                              │
│   - CPU: 78% 🟡                      │
│   - Memory: 1.8GB/2GB 🔴            │
│   - Disk I/O: 45MB/s                │
└─────────────────────────────────────┘
```

### 7.5 Critérios de Sucesso (Baseline)

**Não esperamos alta performance!** Queremos estabelecer baseline.

Critérios mínimos (para não ser considerado "quebrado"):

```
✅ OBRIGATÓRIO (sistema funcional):
  - Erro rate < 5% em carga moderada (100 req/s)
  - Não crashar durante testes
  - Recuperar após pico de carga
  - Sem memory leaks óbvios (1h endurance test)

📊 BASELINE (vamos melhorar depois):
  - Throughput: ? req/s (a descobrir)
  - Latência P95 writes: < 1s
  - Latência P95 reads: < 5s (queries pesadas!)
  - Connection pool: não esgotar em carga moderada
```

**Importante:** Se baseline for muito ruim (< 50 req/s), pode haver bug. Se for razoável (100-500 req/s), está perfeito para começar a série!

### 7.6 Procedimento de Teste

```bash
# 1. Setup ambiente
docker-compose up -d
go run cmd/server/main.go

# 2. Popular banco (baseline de 1M eventos)
go run scripts/seed.go --events=1000000 --logs=500000

# 3. Rodar testes em sequência
k6 run tests/01-write-only.js --out influxdb=http://localhost:8086
# Aguardar 2 minutos (cooldown)

k6 run tests/02-read-only.js --out influxdb=http://localhost:8086
# Aguardar 2 minutos

k6 run tests/03-mixed-load.js --out influxdb=http://localhost:8086
# Aguardar 5 minutos

k6 run tests/04-burst.js --out influxdb=http://localhost:8086
# Aguardar 2 minutos

k6 run tests/05-endurance.js --out influxdb=http://localhost:8086

# 4. Gerar relatório
k6 summary report.json --summary-export=baseline-results.json
```

### 7.7 Relatório de Baseline

Ao final, gerar documento `BASELINE-RESULTS.md`:

```markdown
# A1 Pulse - Baseline Performance Results

Data: 2024-XX-XX
Versão: 0.1 (baseline, sem otimizações)

## Ambiente
- CPU: 2 cores
- RAM: 2GB
- Postgres: 512MB, config padrão
- Dataset: 1M eventos, 500k logs

## Resultados

### Write Performance
- Max throughput: XXX req/s
- P95 latency: XXX ms
- Error rate: X.X%

### Read Performance
- P95 latency: XXX ms
- P99 latency: XXX ms (queries pesadas)
- Slowest query: XXX ms

### Mixed Load (Realista)
- Total throughput: XXX req/s
- Write P95: XXX ms
- Read P95: XXX ms
- Error rate: X.X%

### Gargalos Identificados
1. [ ] Connection pool esgotado
2. [ ] Queries sem índices (seq scan)
3. [ ] CPU 100%
4. [ ] Memória esgotada
5. [ ] Disk I/O alto

## Próximos Passos
Episódio 1: [otimização identificada]
Episódio 2: [próxima otimização]
...
```

---

## 8. Estrutura de Diretórios

```
a1pulse/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── api/
│   │   ├── handlers/
│   │   │   ├── auth.go
│   │   │   ├── projects.go
│   │   │   ├── ingest.go
│   │   │   ├── analytics.go
│   │   │   └── logs.go
│   │   ├── middleware/
│   │   │   ├── auth.go
│   │   │   └── apikey.go
│   │   └── router.go
│   ├── auth/
│   │   ├── jwt.go
│   │   └── password.go
│   ├── models/
│   │   └── models.go
│   └── repository/
│       ├── users.go
│       ├── projects.go
│       ├── events.go
│       └── logs.go
├── migrations/
│   └── 001_initial_schema.sql
├── scripts/
│   └── seed.go
├── tests/
│   ├── 01-write-only.js
│   ├── 02-read-only.js
│   ├── 03-mixed-load.js
│   ├── 04-burst.js
│   └── 05-endurance.js
├── docker-compose.yml
├── Dockerfile
├── go.mod
├── go.sum
├── README.md
├── REQUISITOS-BASELINE.md
└── .env.example
```

---

## 9. Entregáveis

### Para Episódio 0 (Baseline):

- [ ] Código Go completo e funcional
- [ ] Schema SQL aplicado
- [ ] Docker Compose configurado
- [ ] Script de seed funcionando
- [ ] Todos endpoints implementados e testados manualmente
- [ ] Scripts k6 de teste prontos
- [ ] Grafana dashboard básico configurado
- [ ] README com instruções de setup

### Documentação:

- [ ] REQUISITOS-BASELINE.md (este documento)
- [ ] README.md (getting started)
- [ ] API-DOCS.md (endpoints detalhados)
- [ ] TESTING.md (como rodar testes)

---

## 10. Notas Importantes

### O que NÃO fazer no baseline:

- ❌ Não otimizar queries (queremos ver o problema!)
- ❌ Não adicionar índices além dos básicos (PK/FK)
- ❌ Não usar cache
- ❌ Não usar batch inserts otimizados
- ❌ Não usar connection pooling customizado
- ❌ Não usar prepared statements
- ❌ Não fazer tuning do Postgres
- ❌ Não adicionar rate limiting (queremos ver o limite!)

### O que fazer:

- ✅ Código limpo e legível
- ✅ Erro handling básico
- ✅ Logging simples (stdout)
- ✅ Validações básicas de input
- ✅ Métricas coletadas (mesmo sem otimização)
- ✅ Testes funcionais (garantir que funciona)

### Filosofia:

> "Make it work, make it right, make it fast."
>
> Episódio 0: Make it work (baseline)
> Episódios 1-N: Make it fast (otimizações)

---

## 11. Checklist de Validação

Antes de considerar baseline pronto:

**Funcional:**
- [ ] Registro e login funcionam
- [ ] JWT validation funciona
- [ ] CRUD de projetos funciona
- [ ] Ingestão de eventos funciona
- [ ] Ingestão de logs funciona
- [ ] Queries de analytics retornam dados corretos
- [ ] Queries de logs retornam dados corretos
- [ ] API key authentication funciona

**Performance:**
- [ ] Seed de 1M eventos completa (mesmo que demore)
- [ ] Sistema aguenta pelo menos 50 req/s sem crashar
- [ ] Queries retornam (mesmo que lentas)
- [ ] Não há memory leaks óbvios

**Observabilidade:**
- [ ] Logs aparecem no stdout
- [ ] Métricas são coletadas
- [ ] Grafana dashboard mostra dados
- [ ] Consegue identificar gargalos visualmente

**Documentação:**
- [ ] README explica como rodar
- [ ] Requisitos documentados
- [ ] Testes documentados
- [ ] Resultados de baseline documentados

---

**Versão:** 1.0
**Data:** 2024-XX-XX
**Autor:** A1 Lab
**Status:** Draft
