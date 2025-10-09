# MIaaS Documentation

Welcome to the MIaaS (Model Infrastructure as a Service) project!

## Overview

MIaaS is an orchestration platform for deploying and managing AI/ML infrastructure across distributed nodes. It provides centralized management for node registration, capability tracking, and service deployments.

## 🚀 Quick Start

Get up and running in minutes:

```bash
# Clone the repository
git clone https://github.com/fupacat/MIaaS.git
cd MIaaS

# Start with Docker Compose
docker-compose up --build

# View API documentation
open http://localhost:8080/docs
```

See the [Quick Start Guide](../QUICKSTART.md) for more details.

## 📚 Documentation

### Getting Started
- **[Quick Start Guide](../QUICKSTART.md)** - Get running in 5 minutes
- **[README](../README.md)** - Project overview and setup
- **[Onboarding Guide](onboarding.md)** - Comprehensive developer guide

### Component Documentation
- **[Control Plane README](../control-plane/README.md)** - API endpoints and architecture
- **[Control Plane Quick Start](../control-plane/QUICKSTART.md)** - Run the backend
- **[Agent README](../agent/README.md)** - Agent configuration and capabilities
- **[UI README](../ui/README.md)** - React UI development

### Architecture & Design
- **[Architecture Document](../MIaaS.md)** - Complete system design and roadmap
- **[MVP Summary](../MVP_SUMMARY.md)** - Current implementation status
- **[Protocol Specification](protocol.md)** - API contracts and communication

## 🎯 Current Features

✅ **Node Management**
- Automatic node registration
- Real-time capability detection (CPU, memory, disk, GPU)
- Heartbeat monitoring with system metrics
- Node status tracking

✅ **Control Plane**
- FastAPI-based REST API
- Database-backed persistence (SQLite/Postgres)
- Orchestrator with intelligent placement
- Interactive API documentation (Swagger/ReDoc)

✅ **Agent**
- Lightweight Python daemon
- Auto-reconnection on failures
- Configurable heartbeat intervals
- System metrics collection

✅ **UI**
- React-based web interface
- Node visualization with status cards
- Real-time node list updates
- Modern dark theme

## 🔧 Development

### Prerequisites
- Docker & Docker Compose
- Python 3.10+ (for local development)
- Node.js 18+ (for UI development)

### Running Tests
```bash
cd control-plane
pytest -v --cov=app tests/
```

All 27 tests pass covering:
- 11 API endpoint tests
- 8 deployment tests  
- 8 model validation tests

### API Endpoints

**Node Management:**
- `POST /api/v1/nodes/register` - Register nodes
- `GET /api/v1/nodes` - List all nodes
- `GET /api/v1/nodes/{node_id}` - Get node details
- `POST /api/v1/nodes/{node_id}/heartbeat` - Send heartbeat

**Deployment Management:**
- `POST /api/v1/deployments` - Create deployment
- `GET /api/v1/deployments` - List deployments
- `GET /api/v1/deployments/{id}` - Get deployment
- `DELETE /api/v1/deployments/{id}` - Delete deployment

## 🛣️ Roadmap

See [MIaaS.md](../MIaaS.md) for the complete roadmap including:
- Template rendering with Jinja2
- JWT authentication
- WebSocket for real-time logs
- Docker Compose deployment execution
- GPU detection and management
- Multi-tenant support

## 🤝 Contributing

We welcome contributions! Please:
1. Read the [Onboarding Guide](onboarding.md)
2. Create a feature branch
3. Add tests for new features
4. Update documentation
5. Submit a pull request

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/fupacat/MIaaS/issues)
- **Discussions**: [GitHub Discussions](https://github.com/fupacat/MIaaS/discussions)
- **Documentation**: This site and linked guides

## Status

✅ **MVP Complete** - Control plane, agent, and UI are functional with core features implemented.
