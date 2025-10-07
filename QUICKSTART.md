# MIaaS MVP Quick Start

This guide will help you quickly run the MIaaS MVP with the control plane and agent.

## Prerequisites

- Docker and Docker Compose installed
- OR Python 3.11+ installed

## Option 1: Run with Docker Compose (Recommended)

The easiest way to run the MVP is with Docker Compose:

```bash
docker-compose up --build
```

This will:
1. Build and start the control plane on port 8080
2. Build and start an agent that connects to the control plane
3. The agent will register and send heartbeats every 30 seconds

To view logs:
```bash
# All services
docker-compose logs -f

# Control plane only
docker-compose logs -f control-plane

# Agent only
docker-compose logs -f agent
```

To stop:
```bash
docker-compose down
```

## Option 2: Run Locally with Python

### Terminal 1: Start Control Plane

```bash
cd control-plane
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Terminal 2: Start Agent

```bash
cd agent
pip install -r requirements.txt
python agent.py
```

## Verify It's Working

1. Open http://localhost:8080/docs in your browser to see the API documentation
2. Call `GET http://localhost:8080/api/v1/nodes` to see registered nodes
3. Watch the agent logs to see heartbeat messages

Example API calls:

```bash
# List registered nodes
curl http://localhost:8080/api/v1/nodes

# View API docs
open http://localhost:8080/docs
```

## What's Implemented

✅ Control plane with registration and heartbeat endpoints
✅ Agent with automatic registration
✅ Agent sends periodic heartbeats with system metrics
✅ Capability detection (CPU, memory, disk)
✅ Docker support for easy deployment

## Next Steps

See the [Architecture Document](MIaaS.md) for the full roadmap and planned features.
