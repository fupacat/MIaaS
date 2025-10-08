# Control Plane - FastAPI Backend

The Control Plane is the central orchestration component of MIaaS that manages node registration, deployments, and resource allocation.

## Features

- **Node Management**: Register, list, and monitor agent nodes
- **Deployment Management**: Create, track, and manage service deployments
- **Heartbeat Monitoring**: Track node health and resource metrics
- **Orchestrator**: Placement engine for intelligent node selection
- **SQLAlchemy Database**: Persistent storage with SQLite (MVP) or Postgres
- **RESTful API**: Full FastAPI implementation with automatic OpenAPI docs

## Architecture

```
control-plane/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── models.py              # Pydantic request/response models
│   ├── api/
│   │   └── v1/
│   │       ├── nodes.py       # Node management endpoints
│   │       └── deployments.py # Deployment endpoints
│   ├── db/
│   │   ├── database.py        # Database configuration
│   │   └── models.py          # SQLAlchemy ORM models
│   └── orchestrator/
│       └── placement.py       # Node placement engine
└── tests/                     # Comprehensive test suite
```

## API Endpoints

### Node Management

#### Register Node
```
POST /api/v1/nodes/register
```

Register a new node or update an existing one.

**Request body:**
```json
{
  "name": "worker-01",
  "ip": "192.168.1.10",
  "capabilities": {
    "os": "linux",
    "cpu_count": 8,
    "mem_mb": 16000,
    "disk_mb": 500000,
    "gpus": [{"id": 0, "model": "RTX 3090", "mem_mb": 24000}],
    "docker": {"version": "24.0.0", "available": true}
  }
}
```

**Response (201):**
```json
{
  "node_id": "550e8400-e29b-41d4-a716-446655440000",
  "node_token": "node-token-550e8400-e29b-41d4-a716-446655440000",
  "control_plane_url": "http://localhost:8080"
}
```

#### List Nodes
```
GET /api/v1/nodes
```

List all registered nodes with their capabilities and status.

**Response (200):**
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

#### Get Node
```
GET /api/v1/nodes/{node_id}
```

Get details of a specific node.

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "worker-01",
  "ip": "192.168.1.10",
  "capabilities": {...},
  "last_seen": 1234567890.0,
  "status": "online"
}
```

#### Heartbeat
```
POST /api/v1/nodes/{node_id}/heartbeat
```

Update node health and resource metrics.

**Request body:**
```json
{
  "cpu_usage": 45.5,
  "mem_usage": 60.2,
  "disk_free_mb": 450000,
  "running_containers": ["postgres", "redis"]
}
```

**Response (200):**
```json
{
  "status": "ok",
  "timestamp": 1234567890.0
}
```

### Deployment Management

#### Create Deployment
```
POST /api/v1/deployments
```

Create a new deployment request.

**Request body:**
```json
{
  "deployment_id": "deploy-123",
  "template_id": "postgres",
  "rendered_compose": "version: '3.8'\nservices:\n  postgres:\n    image: postgres:16",
  "env": {"POSTGRES_PASSWORD": "secret"},
  "action": "apply"
}
```

**Response (202):**
```json
{
  "deployment_id": "deploy-123",
  "status": "accepted",
  "message": "Deployment request accepted and queued for processing"
}
```

#### List Deployments
```
GET /api/v1/deployments
```

List all deployments.

#### Get Deployment
```
GET /api/v1/deployments/{deployment_id}
```

Get details of a specific deployment.

#### Delete Deployment
```
DELETE /api/v1/deployments/{deployment_id}
```

Mark a deployment for deletion.

### Health & Documentation

```
GET /health          # Health check
GET /                # API information
GET /docs            # Interactive API documentation (Swagger UI)
GET /redoc           # Alternative API documentation
```

## Installation

```bash
cd control-plane
pip install -r requirements.txt
```

## Running the Server

### Development Mode

```bash
cd control-plane
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

The API will be available at:
- API: `http://localhost:8080`
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 4
```

## Testing

Run the full test suite:

```bash
cd control-plane
pytest
```

Run with coverage:

```bash
pytest --cov=app tests/
```

Run specific test files:

```bash
pytest tests/test_api.py -v
pytest tests/test_deployments.py -v
pytest tests/test_models.py -v
```

## Database

### SQLite (Default/MVP)

The default configuration uses SQLite for simplicity:
- Database file: `control_plane.db`
- Created automatically on first run
- Suitable for development and MVP deployments

### PostgreSQL (Production)

For production, update `app/db/database.py`:

```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/miaas"
```

Then install PostgreSQL driver:

```bash
pip install psycopg2-binary
```

## Orchestrator

The placement engine (`app/orchestrator/placement.py`) implements intelligent node selection based on:

- Resource availability (CPU, memory, disk)
- Required capabilities (GPU, Docker version)
- Placement constraints and tags
- Scoring algorithm with configurable weights

Example usage:

```python
from app.orchestrator import PlacementEngine

engine = PlacementEngine()
node_id = engine.select_node(
    nodes=available_nodes,
    requirements={"tags": ["gpu"], "mem_mb": 8000}
)
```

## Development

### Project Structure

- `app/main.py`: FastAPI app initialization and middleware
- `app/models.py`: Pydantic models for API validation
- `app/api/v1/`: API route handlers organized by resource
- `app/db/`: Database models and session management
- `app/orchestrator/`: Placement and scheduling logic
- `tests/`: Comprehensive test coverage

### Adding New Endpoints

1. Create Pydantic models in `app/models.py`
2. Add SQLAlchemy models in `app/db/models.py`
3. Implement router in `app/api/v1/`
4. Include router in `app/main.py`
5. Add tests in `tests/`

### Code Style

Follow PEP 8 and use docstrings for all public functions and classes.

## Environment Variables

```bash
DATABASE_URL=sqlite:///./control_plane.db  # Database connection string
LOG_LEVEL=INFO                              # Logging level
CORS_ORIGINS=*                              # Allowed CORS origins
```

## Next Steps

- [ ] Add authentication (JWT tokens)
- [ ] Implement template rendering with Jinja2
- [ ] Add WebSocket support for real-time logs
- [ ] Integrate Prometheus metrics
- [ ] Add database migrations (Alembic)
- [ ] Implement RBAC for multi-user support

## See Also

- [MIaaS Architecture](../MIaaS.md)
- [Agent Documentation](../agent/README.md)
- [UI Documentation](../ui/README.md)
