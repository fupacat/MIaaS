# Control Plane Quick Start

This guide will help you get the Control Plane up and running in minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Navigate to the control-plane directory:
   ```bash
   cd control-plane
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Start the Control Plane server:
```bash
python -m app.api
```

The server will start on `http://0.0.0.0:5000`

## Testing the API

### Health Check
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy"
}
```

### Register a Node
```bash
curl -X POST http://localhost:5000/api/v1/nodes/register \
  -H "Content-Type: application/json" \
  -d '{
    "id": "node-1",
    "hostname": "worker-01",
    "capabilities": ["docker", "compose"],
    "status": "active"
  }'
```

Expected response:
```json
{
  "message": "Node registered successfully",
  "node": {
    "id": "node-1",
    "hostname": "worker-01",
    "capabilities": ["docker", "compose"],
    "status": "active",
    "last_heartbeat": "2025-10-07T16:00:00+00:00"
  }
}
```

### List All Nodes
```bash
curl http://localhost:5000/api/v1/nodes
```

Expected response:
```json
{
  "count": 1,
  "nodes": [
    {
      "id": "node-1",
      "hostname": "worker-01",
      "capabilities": ["docker", "compose"],
      "status": "active",
      "last_heartbeat": "2025-10-07T16:00:00+00:00"
    }
  ]
}
```

### Get Specific Node
```bash
curl http://localhost:5000/api/v1/nodes/node-1
```

## Running Tests

Run all tests:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run tests with coverage:
```bash
pytest --cov=app tests/
```

## Next Steps

- Check out the [README.md](README.md) for detailed API documentation
- Explore the code in `app/` directory
- Review tests in `tests/` directory
- Build an agent to register with the Control Plane (see issue #3)
