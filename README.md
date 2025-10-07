# MIaaS - Model Infrastructure as a Service

An open platform for orchestrating AI/ML infrastructure across distributed nodes.

## Overview

MIaaS provides a control plane and agent system for managing distributed infrastructure nodes, with a focus on GPU-enabled systems for AI/ML workloads. This MVP implements the core node registration and management UI.

## Architecture

- **Control Plane**: FastAPI backend that manages node registration and provides REST APIs
- **UI**: React-based web interface for viewing and managing nodes
- **Agent**: (Coming soon) Node agent for capability reporting and task execution

## Quick Start

### Using Docker Compose (Recommended)

```bash
cd ops
docker-compose up --build
```

Then open:
- UI: http://localhost:3000
- API: http://localhost:8000

### Local Development

#### Control Plane
```bash
cd control-plane
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, seed test data
./seed_data.sh
```

#### UI
```bash
cd ui
npm install
npm run dev
```

Then open http://localhost:5173

## Features

✅ **Node Registration API** - Nodes can register with the control plane
✅ **Node List Display** - UI shows all registered nodes with capabilities
✅ **Real-time Refresh** - Manually refresh node list
✅ **Responsive Design** - Modern card-based layout with dark theme

## Project Structure

```
MIaaS/
├── control-plane/       # FastAPI backend
│   ├── app/
│   │   └── main.py     # API endpoints
│   ├── Dockerfile
│   └── requirements.txt
├── ui/                  # React frontend
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── App.jsx     # Main app
│   │   └── main.jsx
│   ├── Dockerfile
│   └── nginx.conf
├── ops/                 # Deployment configs
│   └── docker-compose.yml
└── docs/               # Documentation

```

## API Endpoints

### `POST /api/v1/nodes/register`
Register a new node with capabilities.

### `GET /api/v1/nodes`
List all registered nodes.

See [control-plane/README.md](control-plane/README.md) for full API documentation.

## Screenshots

![MIaaS UI](https://github.com/user-attachments/assets/c6e2a552-64b5-488f-905d-4dee208a63e2)

## Roadmap

- [x] Control plane API (node registration, listing)
- [x] UI skeleton with node display
- [ ] Node agent implementation
- [ ] Template system for deployments
- [ ] Authentication and authorization
- [ ] Real-time node status updates
- [ ] Component catalog (Postgres, Redis, LLMs, etc.)

## Development Environment Setup

This project uses VS Code and GitHub Copilot for AI-powered development.

### Automated Setup
1. Open PowerShell in this directory
2. Run `./setup.ps1`
3. Open project in VS Code: `code .`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

See [LICENSE](LICENSE) for details.
