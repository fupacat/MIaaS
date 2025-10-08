# MIaaS Developer Onboarding Guide

Welcome to the Model Inference as a Service (MIaaS) project! This guide will help you get started with development.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker & Docker Compose**: For running services locally
- **Git**: For version control
- **VS Code**: Recommended IDE with GitHub Copilot
- **Python 3.9+**: For service development
- **Node.js 16+**: For tooling and scripts (optional)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/fupacat/MIaaS.git
cd MIaaS
```

### 2. Set Up Development Environment

If using VS Code on Windows:
```powershell
./setup.ps1
```

This installs GitHub Copilot extensions and configures your workspace.

### 3. Start the Services

Launch the control plane and agent using Docker Compose:

```bash
docker-compose up --build
```

This will start:
- Control plane on port 8080
- An agent that automatically registers and sends heartbeats

To run in detached mode:
```bash
docker-compose up -d --build
```

Verify services are running:
```bash
docker-compose ps
```

### 4. Verify Installation

Check the control plane health:
```bash
curl http://localhost:8080/health
```

Expected response:
```json
{
  "status": "healthy"
}
```

List registered nodes:
```bash
curl http://localhost:8080/api/v1/nodes
```

View interactive API documentation:
```bash
open http://localhost:8080/docs
```

## Repository Structure

```
MIaaS/
├── control-plane/      # FastAPI orchestration backend
│   ├── app/
│   │   ├── api/v1/     # API endpoints
│   │   │   ├── nodes.py       # Node management
│   │   │   └── deployments.py # Deployment management
│   │   ├── db/         # Database models
│   │   ├── orchestrator/ # Placement engine
│   │   └── models.py   # Pydantic models
│   ├── tests/          # Test suite (27 tests)
│   └── main.py         # Application entry point
├── agent/              # Node agent daemon
│   ├── agent.py        # Capability detection & heartbeat
│   ├── Dockerfile
│   └── requirements.txt
├── ui/                 # React web interface
│   ├── src/
│   │   ├── components/ # NodeCard, NodeList
│   │   └── App.jsx     # Main application
│   └── package.json
├── docs/               # Documentation
│   ├── protocol.md     # API specifications
│   └── onboarding.md   # This file
├── docker-compose.yml  # Multi-container orchestration
├── QUICKSTART.md       # Quick start guide
└── README.md           # Project overview
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write code following the project's style guide
- Add tests for new functionality
- Update documentation as needed

### 3. Test Locally

```bash
# Run control plane tests
cd control-plane
pytest -v

# Run all tests with coverage
pytest --cov=app tests/

# Test API endpoints manually
curl http://localhost:8080/api/v1/nodes
curl http://localhost:8080/api/v1/deployments
```

### 4. Submit a Pull Request

- Push your branch to GitHub
- Create a pull request with a clear description
- Wait for code review and CI checks to pass

## Common Tasks

### Running the Control Plane Locally

```bash
cd control-plane
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Running the Agent Locally

```bash
cd agent
pip install -r requirements.txt
python agent.py
```

Configure the agent with environment variables:
```bash
export CONTROL_PLANE_URL=http://localhost:8080
export HEARTBEAT_INTERVAL=30
python agent.py
```

### Running the UI

```bash
cd ui
npm install
npm run dev
```

The UI will be available at http://localhost:5173

### Running Tests

```bash
# Control plane tests (27 tests total)
cd control-plane
pytest -v

# Run specific test modules
pytest tests/test_api.py -v
pytest tests/test_deployments.py -v
pytest tests/test_models.py -v

# With coverage report
pytest --cov=app tests/
```

### Debugging

1. Check logs:
   ```bash
   # All services
   docker-compose logs -f
   
   # Specific service
   docker-compose logs -f control-plane
   docker-compose logs -f agent
   ```

2. Access a running container:
   ```bash
   docker-compose exec control-plane /bin/bash
   docker-compose exec agent /bin/bash
   ```

3. View database contents (SQLite):
   ```bash
   docker-compose exec control-plane sqlite3 control_plane.db ".tables"
   docker-compose exec control-plane sqlite3 control_plane.db "SELECT * FROM nodes;"
   ```

### Adding a New API Endpoint

1. Define Pydantic models in `control-plane/app/models.py`
2. Add SQLAlchemy models in `control-plane/app/db/models.py`
3. Create router in `control-plane/app/api/v1/`
4. Register router in `control-plane/app/main.py`
5. Add tests in `control-plane/tests/`
6. Update API documentation in `control-plane/README.md`

## Architecture Overview

MIaaS orchestrates AI/ML infrastructure across distributed nodes:

- **Control Plane**: FastAPI backend that manages node registration, heartbeat monitoring, and deployment orchestration
- **Agent**: Python daemon running on each node that reports capabilities and executes deployments
- **UI**: React web interface for visualizing nodes and managing deployments

## Key Concepts

### Node Registration Flow

1. Agent starts and detects system capabilities (CPU, memory, disk, GPU)
2. Agent registers with Control Plane via POST to `/api/v1/nodes/register`
3. Control Plane assigns a unique node_id and token
4. Agent stores credentials and begins heartbeat loop

### Heartbeat Mechanism

1. Agent sends heartbeat every 30 seconds (configurable)
2. Heartbeat includes real-time metrics: CPU usage, memory usage, disk space
3. Control Plane updates node's `last_seen` timestamp and status
4. Nodes without heartbeat for extended period marked as offline

### Deployment Flow (Planned)

1. User creates deployment via UI or API
2. Control Plane's orchestrator selects optimal node based on requirements
3. Deployment request sent to agent on selected node
4. Agent executes deployment (Docker Compose/K8s)
5. Status updates streamed back to Control Plane

### Database Schema

- **Nodes**: id, name, ip, capabilities, last_seen, status
- **Deployments**: id, template_id, node_id, status, created_at
- Storage: SQLite (MVP) or PostgreSQL (production)

## API Endpoints

### Node Management

```bash
# Register a node
POST /api/v1/nodes/register
{
  "name": "worker-01",
  "ip": "192.168.1.10",
  "capabilities": {
    "os": "linux",
    "cpu_count": 8,
    "mem_mb": 32000,
    "disk_mb": 500000,
    "gpus": [{"id": 0, "model": "RTX 3090", "mem_mb": 24000}]
  }
}

# List all nodes
GET /api/v1/nodes

# Get specific node
GET /api/v1/nodes/{node_id}

# Send heartbeat
POST /api/v1/nodes/{node_id}/heartbeat
{
  "cpu_usage": 25.5,
  "mem_usage": 60.2,
  "disk_free_mb": 450000,
  "running_containers": []
}
```

### Deployment Management

```bash
# Create deployment
POST /api/v1/deployments
{
  "deployment_id": "postgres-prod-01",
  "template_id": "postgres",
  "rendered_compose": "version: '3.8'...",
  "env": {"POSTGRES_PASSWORD": "secret"},
  "action": "apply"
}

# List deployments
GET /api/v1/deployments

# Get deployment status
GET /api/v1/deployments/{deployment_id}

# Delete deployment
DELETE /api/v1/deployments/{deployment_id}
```

## Resources

- [Quick Start Guide](../QUICKSTART.md) - Get running in minutes
- [Control Plane README](../control-plane/README.md) - Detailed API documentation
- [Agent README](../agent/README.md) - Agent configuration
- [UI README](../ui/README.md) - UI development guide
- [Architecture Document](../MIaaS.md) - Full system design
- [MVP Summary](../MVP_SUMMARY.md) - Implementation details

## Getting Help

- **Slack**: #miaas-dev channel
- **Email**: dev-team@miaas.example.com
- **Office Hours**: Tuesdays 2-3 PM PST

## Contributing

We welcome contributions! Please:

1. Read the contribution guidelines
2. Follow the code style guide
3. Write tests for new features
4. Update documentation
5. Be respectful and collaborative

Happy coding! 🚀
