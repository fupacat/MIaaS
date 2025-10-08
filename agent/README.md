# MIaaS Agent

The agent runs on each node in the MIaaS cluster. It registers with the control plane, reports capabilities, and sends periodic heartbeats with system metrics.

## Features

- **Automatic Registration**: Detects system capabilities and registers on startup
- **Capability Detection**: CPU count, total memory, disk space, OS type
- **Periodic Heartbeats**: Sends real-time metrics every 30 seconds (configurable)
- **Auto-Reconnection**: Automatically re-registers if connection to control plane fails
- **Lightweight**: Minimal dependencies (requests, psutil)
- **Docker Support**: Can run as a container or standalone

## How It Works

1. **Startup**: Agent starts and detects system capabilities using `psutil`
2. **Registration**: Sends POST request to `/api/v1/nodes/register` with capabilities
3. **Token Storage**: Receives and stores `node_id` and `node_token` from control plane
4. **Heartbeat Loop**: Every 30 seconds, sends real-time metrics to `/api/v1/nodes/{node_id}/heartbeat`
5. **Failure Handling**: If heartbeat fails, agent re-registers and continues

## Running Locally

### With Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run with default settings
python agent.py

# Or with custom configuration
export CONTROL_PLANE_URL=http://control-plane.example.com:8080
export HEARTBEAT_INTERVAL=60
python agent.py
```

### With Docker

```bash
# Build the image
docker build -t miaas-agent .

# Run with default control plane URL
docker run miaas-agent

# Run with custom control plane
docker run -e CONTROL_PLANE_URL=http://my-control-plane:8080 miaas-agent

# Run with custom heartbeat interval
docker run \
  -e CONTROL_PLANE_URL=http://control-plane:8080 \
  -e HEARTBEAT_INTERVAL=60 \
  miaas-agent
```

### With Docker Compose

The agent is included in the root `docker-compose.yml`:

```bash
# Start both control plane and agent
docker-compose up --build

# View agent logs
docker-compose logs -f agent

# Stop services
docker-compose down
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CONTROL_PLANE_URL` | `http://localhost:8080` | URL of the control plane API |
| `HEARTBEAT_INTERVAL` | `30` | Seconds between heartbeat transmissions |

### Example Configurations

**Development (local control plane):**
```bash
export CONTROL_PLANE_URL=http://localhost:8080
export HEARTBEAT_INTERVAL=30
```

**Production (remote control plane):**
```bash
export CONTROL_PLANE_URL=https://miaas-control.prod.example.com
export HEARTBEAT_INTERVAL=60
```

**Testing (frequent heartbeats):**
```bash
export CONTROL_PLANE_URL=http://localhost:8080
export HEARTBEAT_INTERVAL=5
```

## Capabilities Detected

The agent automatically detects and reports the following capabilities on registration:

| Capability | Description | Example |
|------------|-------------|---------|
| `os` | Operating system type | `"linux"`, `"windows"`, `"darwin"` |
| `cpu_count` | Number of CPU cores | `8` |
| `mem_mb` | Total memory in MB | `32000` |
| `disk_mb` | Total disk space in MB | `500000` |
| `gpus` | GPU information (empty for MVP) | `[]` |

### Example Capability Report

```json
{
  "name": "worker-node-01",
  "ip": "192.168.1.10",
  "capabilities": {
    "os": "linux",
    "cpu_count": 8,
    "mem_mb": 16000,
    "disk_mb": 500000,
    "gpus": []
  }
}
```

## Metrics Collected

The agent sends the following real-time metrics in each heartbeat:

| Metric | Description | Unit |
|--------|-------------|------|
| `cpu_usage` | Current CPU utilization | Percentage (0-100) |
| `mem_usage` | Current memory usage | Percentage (0-100) |
| `disk_free_mb` | Available disk space | Megabytes |
| `running_containers` | List of running containers | Array (empty for MVP) |

### Example Heartbeat Payload

```json
{
  "cpu_usage": 25.5,
  "mem_usage": 60.2,
  "disk_free_mb": 450000,
  "running_containers": []
}
```

## Logs and Debugging

The agent outputs logs to stdout:

```bash
# View logs when running with Docker Compose
docker-compose logs -f agent

# View logs when running standalone Docker
docker logs -f <container-id>
```

**Example log output:**
```
Starting MIaaS agent...
Detected capabilities: {'os': 'linux', 'cpu_count': 4, 'mem_mb': 15995, 'disk_mb': 500000, 'gpus': []}
Registering with control plane...
Registered successfully. Node ID: 3646e270-4a70-495e-9f4b-d099117ccfe9
Starting heartbeat loop (interval: 30s)
Heartbeat sent: CPU 15.2%, Mem 45.3%, Disk 450000 MB free
Heartbeat sent: CPU 18.5%, Mem 47.1%, Disk 449500 MB free
```

## Troubleshooting

### Agent Can't Connect to Control Plane

**Error:** `Failed to register with control plane`

**Solutions:**
- Verify control plane is running: `curl http://localhost:8080/health`
- Check `CONTROL_PLANE_URL` environment variable is correct
- Ensure network connectivity between agent and control plane
- Check firewall rules allow traffic on port 8080

### High CPU Usage

The agent is designed to be lightweight. If CPU usage is high:
- Check `HEARTBEAT_INTERVAL` - increase it to reduce frequency
- Verify no other processes are interfering with metrics collection

### Agent Not Appearing in Node List

1. Check agent logs for registration errors
2. Verify control plane is running: `curl http://localhost:8080/api/v1/nodes`
3. Check database contains node: Look for node_id in control plane logs

## Future Enhancements

Planned features for the agent:

- ✅ Capability detection and heartbeat (MVP complete)
- ⬜ Deployment execution (Docker Compose/K8s)
- ⬜ GPU detection with `nvidia-smi` integration
- ⬜ Container enumeration with Docker API
- ⬜ Log streaming via WebSocket
- ⬜ JWT token authentication
- ⬜ TLS/SSL support for secure communication

## Related Documentation

- [Control Plane README](../control-plane/README.md) - API endpoints
- [Quick Start Guide](../QUICKSTART.md) - Getting started
- [Architecture Document](../MIaaS.md) - System design
- [MVP Summary](../MVP_SUMMARY.md) - Implementation details
