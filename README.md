# MIaaS - Model Infrastructure as a Service

MIaaS is an orchestration platform for deploying and managing AI/ML infrastructure across distributed nodes. It provides centralized management for node registration, capability tracking, and service deployments across your infrastructure.

## Architecture Overview

MIaaS consists of three main components working together:

### Core Components

1. **Control Plane** (`control-plane/`)
   - Central orchestration hub built with FastAPI
   - Manages node registration and heartbeat monitoring
   - Handles deployment requests and placement decisions
   - Provides RESTful API on port 8080
   - Database-backed persistent storage (SQLite/Postgres)

2. **Agent** (`agent/`)
   - Lightweight Python daemon running on each node
   - Automatic capability detection (CPU, memory, disk, GPU)
   - Periodic heartbeat with real-time system metrics
   - Receives and executes deployment commands
   - Auto-reconnection on network failures

3. **UI** (`ui/`)
   - React-based web interface for cluster management
   - Real-time node status visualization
   - Interactive deployment management
   - Modern, responsive design with dark theme

### Communication Flow

```
┌─────────┐     Registration      ┌──────────────┐
│  Agent  │ ──────────────────────>│ Control Plane│
│  (Node) │ <──────────────────────│   (FastAPI)  │
└─────────┘     Heartbeats         └──────────────┘
     │                                      │
     │  Deployment Commands                 │
     └──────────────────────────────────────┘
                                            ↑
                                            │  HTTP/REST
                                        ┌───┴────┐
                                        │   UI   │
                                        │(React) │
                                        └────────┘
```

### Key Features

- **Distributed Node Management**: Register and monitor multiple nodes across your infrastructure
- **Real-time Monitoring**: Track CPU, memory, disk usage, and GPU availability
- **Smart Placement**: Orchestrator selects optimal nodes based on resource requirements
- **Deployment Management**: Create, track, and manage service deployments
- **Auto-discovery**: Agents automatically detect and report system capabilities
- **Fault Tolerant**: Automatic re-registration and status tracking

## Development Environment Setup

This project uses VS Code and GitHub Copilot for AI-powered development. All environment setup is automated, including Git and GitHub integration.

## Automated Setup

1. Open PowerShell in this directory.
2. Run the setup script:
   ```powershell
   ./setup.ps1
   ```
3. Open the project in VS Code:
   ```powershell
   code .
   ```

## What the Script Does
- Installs Copilot and Copilot Chat extensions for VS Code
- (Optional) Installs Python extension if uncommented
- Applies workspace settings for Copilot best practices
- Initializes a git repository and configures your user info
- Creates a new GitHub repository and pushes the initial commit

## Manual Steps (if needed)
- Ensure you are using PowerShell 7+
- Check `.vscode/settings.json` for Copilot configuration
- If you want to use a different GitHub repo, update the script accordingly

## Troubleshooting
- If extension install fails, update VS Code and retry
- For more help, see the official Copilot docs

## Repository Structure

```
MIaaS/
├── control-plane/      # FastAPI orchestration backend
│   ├── app/            # Application code
│   │   ├── api/v1/     # API endpoints (nodes, deployments)
│   │   ├── db/         # Database models and sessions
│   │   └── orchestrator/ # Placement engine
│   ├── tests/          # Test suite
│   ├── Dockerfile      # Container build
│   └── requirements.txt
├── agent/              # Node agent daemon
│   ├── agent.py        # Main agent code
│   ├── Dockerfile
│   └── requirements.txt
├── ui/                 # React web interface
│   ├── src/
│   │   ├── components/ # Node cards, lists
│   │   └── App.jsx     # Main application
│   ├── Dockerfile
│   └── package.json
├── docs/               # Documentation
│   ├── onboarding.md   # Developer onboarding
│   ├── protocol.md     # API specifications
│   └── index.md        # Documentation portal
├── docker-compose.yml  # Multi-service orchestration
├── QUICKSTART.md       # Quick start guide
├── MVP_SUMMARY.md      # Implementation summary
└── README.md           # This file
```

## Quick Start

The fastest way to get MIaaS running is with Docker Compose:

```bash
# Start control plane and agent
docker-compose up --build

# In another terminal, verify it's working
curl http://localhost:8080/api/v1/nodes
```

This will:
- Start the control plane on port 8080
- Start an agent that automatically registers
- Begin sending heartbeats every 30 seconds

### View API Documentation

Open your browser to see interactive API docs:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

### Quick API Examples

```bash
# Check health
curl http://localhost:8080/health

# List registered nodes
curl http://localhost:8080/api/v1/nodes

# Get specific node details
curl http://localhost:8080/api/v1/nodes/{node_id}

# List deployments
curl http://localhost:8080/api/v1/deployments
```

### Running Locally (Without Docker)

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions on running components individually.

### Documentation

- **[Quick Start Guide](QUICKSTART.md)**: Get up and running in minutes
- **[Onboarding Guide](docs/onboarding.md)**: Comprehensive developer setup
- **[Control Plane README](control-plane/README.md)**: API endpoints and architecture
- **[Agent README](agent/README.md)**: Agent configuration and capabilities
- **[UI README](ui/README.md)**: React UI development
- **[Architecture Document](MIaaS.md)**: Full system design and roadmap

## Contributing

1. Create a feature branch from `master`
2. Make your changes following the project conventions
3. Test locally using Docker Compose
4. Submit a pull request with clear description

For detailed contribution guidelines, see [docs/onboarding.md](docs/onboarding.md).
