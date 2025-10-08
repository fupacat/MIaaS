# MIaaS Quick Start Guide

Get MIaaS up and running in 5 minutes! This guide covers the control plane, agent, and UI.

## Prerequisites

Choose one of the following:
- **Docker & Docker Compose** (recommended - easiest setup)
- **Python 3.10+** (for local development)
- **Node.js 18+** (only needed for UI development)

## Option 1: Docker Compose (Recommended)

The easiest way to get everything running:

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/fupacat/MIaaS.git
cd MIaaS

# Start all services
docker-compose up --build
```

This will:
1. ✅ Build and start the **control plane** on port 8080
2. ✅ Build and start an **agent** that auto-registers with the control plane
3. ✅ Agent begins sending heartbeats every 30 seconds with system metrics

### View Logs

```bash
# All services
docker-compose logs -f

# Control plane only
docker-compose logs -f control-plane

# Agent only
docker-compose logs -f agent
```

### Stop Services

```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v
```

## Option 2: Run Locally (Development Mode)

Running components individually is useful for development and debugging.

### Terminal 1: Start Control Plane

```bash
cd control-plane
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

The control plane will start with auto-reload enabled for development.

### Terminal 2: Start Agent

```bash
cd agent
pip install -r requirements.txt
python agent.py
```

The agent will register with the control plane and begin sending heartbeats.

### Terminal 3 (Optional): Start UI

```bash
cd ui
npm install
npm run dev
```

The UI will be available at http://localhost:5173

## Verify It's Working

### 1. Access the API Documentation

Open your browser to see interactive API docs:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

### 2. Check Health Status

```bash
curl http://localhost:8080/health
```

Expected response:
```json
{"status": "healthy"}
```

### 3. List Registered Nodes

```bash
curl http://localhost:8080/api/v1/nodes
```

You should see at least one node (the agent that started):
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "agent-hostname",
    "ip": "172.18.0.3",
    "status": "online",
    "last_seen": 1704067200.123,
    "capabilities": {
      "os": "linux",
      "cpu_count": 4,
      "mem_mb": 16000,
      "disk_mb": 500000,
      "gpus": []
    }
  }
]
```

### 4. Watch Agent Logs

Monitor the agent's heartbeat messages:
```bash
docker-compose logs -f agent
```

You should see output like:
```
agent_1 | Starting MIaaS agent...
agent_1 | Detected capabilities: {'os': 'linux', 'cpu_count': 4, ...}
agent_1 | Registering with control plane...
agent_1 | Registered successfully. Node ID: 550e8400-...
agent_1 | Starting heartbeat loop (interval: 30s)
agent_1 | Heartbeat sent: CPU 15.2%, Mem 45.3%, Disk 450000 MB free
```

### 5. View UI (Optional)

If you're running the UI:
- Open http://localhost:5173
- You should see node cards displaying your registered nodes

## Example API Usage

### Node Management

```bash
# List all nodes
curl http://localhost:8080/api/v1/nodes

# Get specific node details
curl http://localhost:8080/api/v1/nodes/{node_id}

# Node registration is done automatically by agents
# but here's the format:
curl -X POST http://localhost:8080/api/v1/nodes/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "worker-02",
    "ip": "192.168.1.20",
    "capabilities": {
      "os": "linux",
      "cpu_count": 8,
      "mem_mb": 32000,
      "disk_mb": 1000000,
      "gpus": []
    }
  }'
```

### Deployment Management

```bash
# Create a deployment
curl -X POST http://localhost:8080/api/v1/deployments \
  -H "Content-Type: application/json" \
  -d '{
    "deployment_id": "postgres-prod-01",
    "template_id": "postgres",
    "rendered_compose": "version: '\''3.8'\''\nservices:\n  postgres:\n    image: postgres:15",
    "env": {"POSTGRES_PASSWORD": "secret123"},
    "action": "apply"
  }'

# List all deployments
curl http://localhost:8080/api/v1/deployments

# Get deployment status
curl http://localhost:8080/api/v1/deployments/postgres-prod-01

# Delete a deployment
curl -X DELETE http://localhost:8080/api/v1/deployments/postgres-prod-01
```

## What's Implemented

✅ **Control Plane**
- FastAPI backend with REST API
- Node registration and management
- Heartbeat monitoring
- Deployment tracking
- Database persistence (SQLite)
- Interactive API documentation

✅ **Agent**
- Automatic capability detection
- Registration with control plane
- Periodic heartbeat with system metrics
- Auto-reconnection on failures
- Docker containerization

✅ **UI**
- React-based web interface
- Node list visualization
- Real-time status display
- Responsive design

✅ **Infrastructure**
- Docker Compose orchestration
- Multi-container deployment
- Comprehensive test suite (27 tests)

## Configuration Options

### Agent Configuration

```bash
# Custom control plane URL
export CONTROL_PLANE_URL=http://my-control-plane:8080

# Custom heartbeat interval (seconds)
export HEARTBEAT_INTERVAL=60

python agent.py
```

### Control Plane Configuration

```bash
# Custom database URL
export DATABASE_URL=postgresql://user:pass@localhost/miaas

# Custom log level
export LOG_LEVEL=DEBUG

# CORS origins (comma-separated)
export CORS_ORIGINS=http://localhost:3000,http://localhost:5173

uvicorn app.main:app --port 8080
```

## Troubleshooting

### Port Already in Use

If port 8080 is in use:
```bash
# Stop existing services
docker-compose down

# Or use a different port
uvicorn app.main:app --port 8081
```

### Agent Can't Connect

If the agent can't reach the control plane:
```bash
# Check control plane is running
curl http://localhost:8080/health

# Check Docker network
docker network inspect miaas_miaas-network

# Verify agent can resolve control-plane hostname
docker-compose exec agent ping control-plane
```

### Database Locked

If you see database lock errors:
```bash
# Stop all services and remove volumes
docker-compose down -v

# Restart
docker-compose up --build
```

## Next Steps

Now that you have MIaaS running:

1. **Explore the API**: Open http://localhost:8080/docs and try different endpoints
2. **Add More Agents**: Deploy the agent on multiple nodes to build a cluster
3. **Review the Code**: Check out `control-plane/app/` and `agent/agent.py`
4. **Read the Docs**:
   - [Architecture Document](MIaaS.md) - Full system design
   - [Control Plane README](control-plane/README.md) - API details
   - [Agent README](agent/README.md) - Agent configuration
   - [UI README](ui/README.md) - UI development
   - [Onboarding Guide](docs/onboarding.md) - Developer workflow
5. **Run the Tests**: `cd control-plane && pytest -v`
6. **Contribute**: Check out open issues and submit PRs!

## Need Help?

- **Documentation**: See [docs/](docs/) directory
- **Issues**: https://github.com/fupacat/MIaaS/issues
- **Discussions**: https://github.com/fupacat/MIaaS/discussions
