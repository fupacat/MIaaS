# MIaaS Control Plane

The control plane is the central orchestration service for the MIaaS platform. It manages node registration, heartbeats, and deployment coordination.

## Features

- Node registration endpoint
- Heartbeat monitoring
- Node status tracking

## Running Locally

### With Python

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### With Docker

```bash
docker build -t miaas-control-plane .
docker run -p 8080:8080 miaas-control-plane
```

## API Endpoints

- `GET /` - Service health check
- `POST /api/v1/nodes/register` - Register a new node
- `GET /api/v1/nodes` - List all registered nodes
- `POST /api/v1/nodes/{node_id}/heartbeat` - Send node heartbeat

## Testing

Access the API documentation at `http://localhost:8080/docs` when running.
