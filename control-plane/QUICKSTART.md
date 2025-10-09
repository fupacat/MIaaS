# Control Plane Quick Start

This guide will help you get the MIaaS Control Plane FastAPI backend up and running in minutes.

## Prerequisites

- Python 3.10 or higher
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

### Option 1: Using Python directly
```bash
python3 main.py
```

### Option 2: Using uvicorn (recommended for development)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

The server will start on `http://localhost:8080`

## API Documentation

Once the server is running, you can access interactive API documentation:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

## Quick API Tests

### Health Check
```bash
curl http://localhost:8080/health
```

Expected response:
```json
{
  "status": "healthy"
}
```

### Register a Node
```bash
curl -X POST http://localhost:8080/api/v1/nodes/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "worker-01",
    "ip": "192.168.1.10",
    "capabilities": {
      "os": "linux",
      "cpu_count": 8,
      "mem_mb": 16000,
      "gpus": []
    }
  }'
```

Expected response:
```json
{
  "node_id": "550e8400-e29b-41d4-a716-446655440000",
  "node_token": "node-token-550e8400-e29b-41d4-a716-446655440000",
  "control_plane_url": "http://localhost:8080"
}
```

### List All Nodes
```bash
curl http://localhost:8080/api/v1/nodes
```

Expected response:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "worker-01",
    "ip": "192.168.1.10",
    "capabilities": {...},
    "last_seen": 1234567890.0,
    "status": "online"
  }
]
```

### Send Node Heartbeat
```bash
# Replace {node_id} with actual node ID from registration
curl -X POST http://localhost:8080/api/v1/nodes/{node_id}/heartbeat \
  -H "Content-Type: application/json" \
  -d '{
    "cpu_usage": 45.5,
    "mem_usage": 60.2,
    "disk_free_mb": 450000,
    "running_containers": ["postgres"]
  }'
```

### Create a Deployment
```bash
curl -X POST http://localhost:8080/api/v1/deployments \
  -H "Content-Type: application/json" \
  -d '{
    "deployment_id": "deploy-postgres-1",
    "template_id": "postgres",
    "rendered_compose": "version: '3.8'\nservices:\n  postgres:\n    image: postgres:16",
    "env": {"POSTGRES_PASSWORD": "secret"},
    "action": "apply"
  }'
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

All 31 tests should pass:
- 11 API endpoint tests
- 8 deployment tests
- 8 model validation tests
- 4 seed data tests

## Project Structure

```
control-plane/
├── app/
│   ├── main.py                 # FastAPI app initialization
│   ├── models.py              # Pydantic request/response models
│   ├── api/v1/
│   │   ├── nodes.py           # Node management endpoints
│   │   └── deployments.py    # Deployment endpoints
│   ├── db/
│   │   ├── database.py        # Database configuration
│   │   └── models.py          # SQLAlchemy ORM models
│   └── orchestrator/
│       └── placement.py       # Node placement engine
├── tests/                      # Test suite
├── main.py                     # Server entry point
└── requirements.txt
```

## Database

The control plane uses SQLite by default (`control_plane.db`). The database is created automatically on first run.

### Seeding Test Data

To quickly populate the database with test nodes:

**Option 1: Shell script (requires running server)**
```bash
./seed_data.sh
```

**Option 2: Python script (direct database access)**
```bash
python seed_data.py
python seed_data.py --clear  # Clear existing data first
```

This will create 3 test nodes with different capabilities including GPU support.

### Reset Database

To reset the database:
```bash
rm control_plane.db
```

## Troubleshooting

### Port Already in Use
Change the port:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8081
```

### Import Errors
Ensure you're in the control-plane directory and dependencies are installed:
```bash
cd control-plane
pip install -r requirements.txt
```

## Next Steps

- Check out the [README.md](README.md) for detailed API documentation
- Explore the code in `app/` directory
- Review tests in `tests/` directory
- Build an agent to register with the Control Plane
- Add authentication and security features
- Implement template rendering with Jinja2

## See Also

- [Full Documentation](README.md)
- [MIaaS Architecture](../MIaaS.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
