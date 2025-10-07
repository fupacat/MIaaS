# Control Plane

The Control Plane is the central component of MIaaS that manages node registration and orchestration.

## Features

- Node registration via REST API
- Node listing and retrieval
- In-memory storage for nodes
- Health check endpoint

## API Endpoints

### Register Node
```
POST /api/v1/nodes/register
```

Register a new node or update an existing one.

**Request body:**
```json
{
  "id": "node-123",
  "hostname": "worker-01",
  "capabilities": ["docker", "compose"],
  "status": "active"
}
```

**Response (201):**
```json
{
  "message": "Node registered successfully",
  "node": {
    "id": "node-123",
    "hostname": "worker-01",
    "capabilities": ["docker", "compose"],
    "status": "active",
    "last_heartbeat": "2025-10-07T12:00:00"
  }
}
```

### List Nodes
```
GET /api/v1/nodes
```

List all registered nodes.

**Response (200):**
```json
{
  "nodes": [
    {
      "id": "node-123",
      "hostname": "worker-01",
      "capabilities": ["docker", "compose"],
      "status": "active",
      "last_heartbeat": "2025-10-07T12:00:00"
    }
  ],
  "count": 1
}
```

### Get Node
```
GET /api/v1/nodes/{node_id}
```

Get details of a specific node.

**Response (200):**
```json
{
  "id": "node-123",
  "hostname": "worker-01",
  "capabilities": ["docker", "compose"],
  "status": "active",
  "last_heartbeat": "2025-10-07T12:00:00"
}
```

### Health Check
```
GET /health
```

Check if the service is healthy.

**Response (200):**
```json
{
  "status": "healthy"
}
```

## Installation

```bash
cd control-plane
pip install -r requirements.txt
```

## Running

```bash
cd control-plane
python -m app.api
```

The server will start on `http://0.0.0.0:5000`.

## Testing

```bash
cd control-plane
pytest
```

## Node Model

A node in the system has the following attributes:

- `id` (string, required): Unique identifier for the node
- `hostname` (string, required): Hostname of the node
- `capabilities` (list, optional): List of capabilities the node supports (e.g., ["docker", "compose"])
- `status` (string, optional): Current status of the node (default: "active")
- `last_heartbeat` (datetime, auto-generated): Timestamp of the last heartbeat received
