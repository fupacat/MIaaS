# MIaaS Control Plane

FastAPI-based control plane for managing nodes in the MIaaS cluster.

## Features

- Node registration API
- Node listing with capabilities
- CORS-enabled for UI integration
- In-memory storage (MVP)

## API Endpoints

### GET `/`
Health check endpoint
```json
{
  "message": "MIaaS Control Plane API",
  "version": "0.1.0"
}
```

### POST `/api/v1/nodes/register`
Register a new node with the control plane.

**Request:**
```json
{
  "name": "node-1",
  "ip": "192.168.1.100",
  "capabilities": {
    "cpu": "8 cores",
    "memory": "16GB",
    "gpu": "NVIDIA RTX 3090",
    "docker": true
  }
}
```

**Response:**
```json
{
  "node_id": "uuid",
  "node_token": "node-token-uuid"
}
```

### GET `/api/v1/nodes`
List all registered nodes.

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "node-1",
    "ip": "192.168.1.100",
    "capabilities": { ... },
    "last_seen": 1234567890.123,
    "status": "online"
  }
]
```

## Development

### Run locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Seed test data
```bash
./seed_data.sh
```

### Build Docker image
```bash
docker build -t miaas-control-plane .
```

### Run with Docker
```bash
docker run -p 8000:8000 miaas-control-plane
```

## Testing

```bash
# Check API health
curl http://localhost:8000/

# List nodes
curl http://localhost:8000/api/v1/nodes

# Register a node
curl -X POST http://localhost:8000/api/v1/nodes/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-node",
    "ip": "192.168.1.100",
    "capabilities": {"cpu": "8 cores", "docker": true}
  }'
```
