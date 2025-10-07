# MIaaS Agent

The agent runs on each node in the MIaaS cluster. It registers with the control plane, reports capabilities, and sends periodic heartbeats with system metrics.

## Features

- Automatic registration with control plane
- Capability detection (CPU, memory, disk)
- Periodic heartbeat with system metrics
- Automatic re-registration on connection failure

## Running Locally

### With Python

```bash
pip install -r requirements.txt
python agent.py
```

### With Docker

```bash
docker build -t miaas-agent .
docker run -e CONTROL_PLANE_URL=http://localhost:8080 miaas-agent
```

## Configuration

Environment variables:

- `CONTROL_PLANE_URL` - URL of the control plane (default: `http://localhost:8080`)
- `HEARTBEAT_INTERVAL` - Seconds between heartbeats (default: `30`)

## Metrics Collected

- CPU usage percentage
- Memory usage percentage
- Free disk space in MB
- Running containers (placeholder for future implementation)
