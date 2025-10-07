Great — I’ll lay out a complete, ready-to-implement system spec plus a repo skeleton. This will include:

* high-level architecture
* repo layout (files + folders you can create)
* module responsibilities
* runtime data models & API contracts
* agent protocol & sample messages
* component templates / manifests (Docker Compose + k8s snippets)
* security & networking guidance
* CI / testing plan
* MVP roadmap with prioritized tasks and rough effort estimates
* examples: `docker-compose` + minimal FastAPI agent/server snippets

You can take this straight to an implementation sprint.

# 1) High-level architecture (recap)

* **Control plane (web app)** — central API + React UI + orchestrator layer; owns cluster state, templates, RBAC, secrets.
* **Agent (node daemon)** — lightweight service (runs as a container/daemon) on every host; reports capabilities and executes deployment actions (compose/helm/k8s, model pull, start/stop).
* **Component Catalog** — library of templates (docker-compose fragments, helm charts, k8s manifests) for Postgres, Redis, Qdrant, Ollama/vLLM, Kafka, Portainer agent, Traefik, Prometheus/Grafana, etc.
* **Orchestrator** — module that decides placement (which node runs which service) based on capabilities and user choices; executes via the agent.
* **Network & Discovery** — local mDNS + optional WireGuard/Tailscale; control plane issues CA-signed certificates or uses Tailscale auth.
* **UI** — single-page app that lists nodes, services, topology, resource usage, and buttons to provision/tear down components.

# 2) Repo skeleton (top-level)

```
devnet-orchestrator/
├── README.md
├── LICENSE
├── ops/                            # infra to run control-plane itself
│   ├── docker-compose.yml
│   └── traefik/                   # optional ingress for control plane
├── control-plane/                  # FastAPI backend + orchestrator
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── nodes.py
│   │   │   │   ├── templates.py
│   │   │   │   └── deployments.py
│   │   ├── models/                 # pydantic models
│   │   ├── orchestrator/           # placement logic & planner
│   │   ├── templates/              # component templates (yaml/json)
│   │   ├── db/                     # sqlite/postgres migration + store
│   │   └── auth/                   # JWT + API key handling
│   └── Dockerfile
├── agent/                          # node agent (runs on each host)
│   ├── agent/
│   │   ├── agent.py                # main agent
│   │   ├── executor.py             # compose/k8s/command executors
│   │   ├── reporter.py             # capabilities reporter
│   │   └── Dockerfile
│   └── examples/
├── ui/                             # React (or Solid/Vue) SPA
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── api/
│   └── Dockerfile
├── templates/                      # reusable compose/k8s templates & fragments
│   ├── postgres/
│   │   ├── docker-compose.yml.j2
│   │   └── k8s/
│   ├── qdrant/
│   ├── ollama/
│   ├── portainer/
│   └── traefik/
├── docs/
│   ├── protocol.md                 # agent <-> control-plane protocol
│   ├── onboarding.md
│   └── architect.md
├── scripts/
│   ├── build.sh
│   ├── install-agent.sh            # one-liner agent bootstraper
│   └── devctl                      # CLI helper
└── ci/
    └── tests/
```

# 3) Core modules & responsibilities

### Control Plane

* **API**: register nodes, list nodes, present templates, start/stop deployments, query status, manage secrets & credentials.
* **Persistence**: lightweight DB (SQLite for MVP, Postgres for scale).
* **Orchestrator**: placement engine that maps templates to nodes (simple rule-based, then greedy bin-packing).
* **Executor**: sends execution plans to node agents (via HTTPS/gRPC/WebSocket).
* **Template Manager**: renders templates using Jinja2 with per-node variables.
* **Auth**: API key for nodes + JWT for user sessions. Optionally integrate Keycloak later.

### Agent

* **Registration**: on first run, post capabilities to control-plane and receive a node-token.
* **Capability detection**: GPU present, cores, mem, disk, OS, docker/k8s availability, network interfaces, mounts.
* **Executor**: apply docker-compose fragments, helm charts, k8s manifests, download model files, run arbitrary systemctl/docker commands.
* **Health reporting**: heartbeat; streaming logs if requested.
* **Security**: run as non-root where possible; drop privileges; use Docker socket optionally via vetted mount.

### UI

* **Node list & onboarding wizard** (QR / token-based!)
* **Component catalog** with toggles & per-component parameterization (ports, volumes, image tags)
* **Topology map**: display services & node placements
* **Logs & metrics**: live tail + link to Grafana
* **LLM panel**: model management, GPU usage, restart model

### Templates

* For each component: both Docker Compose fragment and k8s manifests, plus variables spec (ports, volumes, envs).
* e.g., `templates/ollama/docker-compose.yml.j2` uses `{{ model_path }}` and `{{ gpu_enabled }}` flags.

# 4) Data models & API contracts (MVP)

### Node model (pydantic)

```py
Node {
  id: str           # uuid
  name: str
  ip: str
  os: str
  cpu_count: int
  total_memory_mb: int
  disks: [{ mount, total_mb, free_mb }]
  gpus: [{ id, model, mem_mb }] | []
  docker: {version, available: bool}
  k8s: {version, available: bool}
  last_seen: datetime
  tags: List[str]  # e.g., ["gpu", "infra", "hypervisor"]
  status: "online" | "offline"
}
```

### Agent <-> Control Plane registration (HTTP POST)

* Endpoint: `POST /api/v1/nodes/register`
* Body: `{ "name": "...", "capabilities": {...}, "agent_version": "0.1" }`
* Response: `{ "node_id": "...", "node_token": "JWT-or-API-key", "control_plane_url": "..." }`

### Heartbeat (WebSocket or periodic POST)

* `POST /api/v1/nodes/{node_id}/heartbeat` with metrics: cpu, mem, gpu_util, disk free, running containers[].

### Deploy request (control → agent)

* `POST /api/v1/nodes/{node_id}/deploy` body:

```json
{
  "deployment_id": "uuid",
  "template_id": "postgres",
  "rendered_compose": "<string: rendered docker-compose yaml>",
  "env": {"POSTGRES_PASSWORD": "..."},
  "action": "apply"   // or "remove"
}
```

* agent responds with `202 accepted` and streams logs `/api/v1/deployments/{id}/logs`.

# 5) Agent protocol & sample messages

Prefer HTTP(S) for simplicity. Use mutual TLS or node-token-based JWT for auth.

* **Registration**: agent POSTs `/register` with host facts.
* **Heartbeat**: every 30s via `/heartbeat`.
* **Command execution**: control posts `/deploy` with a plan. Plan includes steps:

  * `pull_image`: `<image>`
  * `create_volume`: `<name>`
  * `run_compose`: `<compose_yaml>`
  * `exec`: shell command (for model download)
* **Streaming**: websocket `/ws/logs?deployment={id}` for live logs.

# 6) Placement rules (orchestrator)

Start simple:

1. Filter nodes by required tags (e.g., require `gpu`).
2. For each service instance:

   * Sort nodes by `score = free_memory * w1 + free_disk * w2 + (gpu_available ? w3 : 0)`
   * Pick highest score respecting port conflicts.
3. If not enough capacity, show suggestion (e.g., “Move Redis to hypervisor”).

# 7) Component templates (MVP examples)

Provide Docker Compose Jinja2 fragments:

`templates/postgres/docker-compose.yml.j2`

```yaml
version: '3.8'
services:
  postgres_{{ instance_name }}:
    image: postgres:16
    environment:
      - POSTGRES_USER={{ db_user }}
      - POSTGRES_PASSWORD={{ db_password }}
      - POSTGRES_DB={{ db_name }}
    volumes:
      - {{ volume_path }}:/var/lib/postgresql/data
    ports:
      - "{{ host_port }}:5432"
    restart: unless-stopped
```

`templates/ollama/docker-compose.yml.j2`

```yaml
version: '3.8'
services:
  ollama:
    image: ollama/ollama:latest
    environment:
      - MODEL_PATH={{ model_path }}
    volumes:
      - {{ models_path }}:/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    ports:
      - "{{ host_port }}:8001"
    command: ["server", "--port", "8001"]
```

(If using docker-compose v2 you may need `runtime: nvidia` or `--gpus` invocation—agent will handle correct `docker compose` invocation parameters by node.)

# 8) Security & networking

* **Node authentication**: upon registration control plane issues node-specific JWT with short-ish TTL and supports rotation.
* **Communication**: HTTPS only; control plane should expose API over TLS via Traefik; use Let's Encrypt or self-signed CA for local.
* **Least privilege**: avoid mounting host docker socket unless user opts in; offer an alternative (agent uses Podman or kubelet).
* **Secrets**: control-plane stores secrets encrypted at rest (use libsodium or AES-GCM) and only injects at render time to agent.
* **Network exposure**: DB/Kafka bind to internal network only; control-plane will configure firewall (ufw/iptables) via agent if asked.

# 9) Observability

* Agent reports metrics (CPU, MEM, GPU util) periodically to control-plane; control-plane stores in Prometheus (or proxies to Prometheus remote write).
* Logs: agent provides log streaming endpoints that the control-plane can persist to Loki or serve directly.
* Visual: Grafana dashboards embedded in UI panel.

# 10) CI / testing plan

* Unit tests for template rendering & validation.
* Integration tests (with Docker-in-Docker) verifying agent executes compose fragments.
* Contract tests for API endpoints using pytest + httpx + testcontainers.
* End-to-end test: spin up control-plane + agent in CI runner and deploy simple `hello-world` compose.

# 11) MVP Roadmap — prioritized (sprint-style)

**MVP (2–4 sprints, each 1 week)**

Sprint 0 — Planning & infra (1 week)

* Repo skeleton + README
* Minimal ops docker-compose for control-plane
* Basic docs (protocol.md, onboarding.md)

Sprint 1 — Core API + Agent registration (1 week)

* FastAPI control-plane: node register, list nodes, heartbeat endpoints
* Agent: registration + capability report
* Simple web UI skeleton showing node list (static)

Sprint 2 — Templates + Deploy flow (1–2 weeks)

* Jinja2 template renderer for docker-compose fragments
* Agent executor: accept `deploy` with compose YAML and run `docker compose up -d` (simple)
* UI: component catalog, deploy button, show deployment logs

Sprint 3 — Auth, security, & discovery (1 week)

* JWT/node-token auth
* Optional mDNS discovery & QR-code onboarding flow
* Basic TLS (self-signed) and local cert handling

Sprint 4 — LLM module + model management (1 week)

* Add Ollama / vLLM template, implement GPU detection & `--gpus` handling
* UI: LLM control panel (model upload/download + start/stop)

Sprint 5 — Observability & polishing (1 week)

* Integrate Prometheus + Grafana (or push metrics to control-plane)
* Logs streaming panel + Grafana link
* Basic RBAC (users + API keys)

Optional later:

* k8s support with Helm charts
* Advanced placement (bin-packing, constraint solver)
* Federated upgrades, backup/restore, model snapshot manager

# 12) Example minimal files (copy/paste)

### Control-plane `app/main.py` (FastAPI minimal)

```py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid, time

app = FastAPI()

nodes = {}

class RegisterReq(BaseModel):
    name: str
    ip: str
    capabilities: dict

@app.post("/api/v1/nodes/register")
def register_node(body: RegisterReq):
    node_id = str(uuid.uuid4())
    nodes[node_id] = {
        "id": node_id,
        "name": body.name,
        "ip": body.ip,
        "capabilities": body.capabilities,
        "last_seen": time.time()
    }
    return {"node_id": node_id, "node_token": f"node-token-{node_id}"}

@app.get("/api/v1/nodes")
def list_nodes():
    return list(nodes.values())
```

### Agent `agent/agent.py` (minimal)

```py
import requests, time, socket, json
CONTROL_PLANE = "http://control-plane.local:8080"
def get_capabilities():
    # very small footprint example
    return {
        "os": "linux",
        "cpu_count": 8,
        "mem_mb": 32000,
        "gpus": []
    }

def register():
    payload = {"name": socket.gethostname(), "ip": "192.168.1.10", "capabilities": get_capabilities()}
    r = requests.post(f"{CONTROL_PLANE}/api/v1/nodes/register", json=payload)
    print("register response", r.text)
    data = r.json()
    return data

if __name__ == "__main__":
    print("Agent starting")
    info = register()
    while True:
        # heartbeat could go here
        time.sleep(30)
```

### Ops `docker-compose.yml` (control-plane minimal)

```yaml
version: '3.8'
services:
  control:
    build: ./control-plane
    ports:
      - "8080:8080"
    volumes:
      - ./control-plane/app:/app
  ui:
    build: ./ui
    ports:
      - "3000:3000"
```

# 13) UX / UI wireframes (text)

* **Landing**: cluster name, top-level status (nodes online, services running)
* **Nodes**: card per node — name, IP, tags (gpu/infra), last seen, quick actions (SSH, open agent UI)
* **Catalog**: grid of components (Postgres, Redis, Qdrant, Ollama, Traefik). Each has "Install" button and parameter modal.
* **Deployment page**: shows rendered compose, selected node(s), and action plan + progress bar + logs.
* **LLM panel**: model list, upload model, start/stop, GPU metrics (util, mem).

# 14) Estimated tech choices

* Backend: FastAPI (Python) — quick to iterate, good ecosystem for pydantic models.
* Agent: Python (asyncio) or Go — Python easier for MVP; Go option for compiled binary later.
* UI: React + Tailwind (or Mantine) — fast to bootstrap a good-looking UI.
* Template rendering: Jinja2
* DB: SQLite for MVP, Postgres for long-term
* Auth: PyJWT + optional Keycloak integration later
* Container execution: agent shells out to `docker compose` or to Docker SDK (Python docker SDK)

# 15) Next steps — immediate deliverables I can produce for you now

I can generate any of the following in this conversation (pick any or multiple; I’ll produce full files you can paste and run):

* A. Full minimal runnable `ops/docker-compose.yml` + `control-plane` FastAPI app + `agent` container that registers and heartbeats (MVP).
* B. A set of Jinja2 templates for Postgres, Redis, Ollama and a control-plane API that can render them and send to agent for deploy.
* C. A small React UI skeleton that lists nodes and offers a simple “Install Postgres” modal.
* D. A ready-to-run `install-agent.sh` script and `agent` Dockerfile.

Tell me which of A/B/C/D (or multiple) you want me to generate now and I’ll output the file contents ready to paste into your repo.
