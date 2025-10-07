# MIaaS Developer Onboarding Guide

Welcome to the Model Inference as a Service (MIaaS) project! This guide will help you get started with development.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker & Docker Compose**: For running services locally
- **Git**: For version control
- **VS Code**: Recommended IDE with GitHub Copilot
- **Python 3.9+**: For service development
- **Node.js 16+**: For tooling and scripts (optional)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/fupacat/MIaaS.git
cd MIaaS
```

### 2. Set Up Development Environment

If using VS Code on Windows:
```powershell
./setup.ps1
```

This installs GitHub Copilot extensions and configures your workspace.

### 3. Start the Services

Launch the control plane using Docker Compose:

```bash
cd ops
docker-compose up -d
```

Verify services are running:
```bash
docker-compose ps
```

### 4. Verify Installation

Check the control plane health:
```bash
curl http://localhost:8080/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Repository Structure

```
MIaaS/
├── services/           # Microservices
│   ├── control-plane/  # Request orchestration
│   ├── inference-engine/ # Model execution
│   └── model-registry/ # Model storage
├── ops/                # Operations & deployment
│   └── docker-compose.yml
├── docs/               # Documentation
│   ├── protocol.md     # API specifications
│   └── onboarding.md   # This file
├── setup.ps1           # Development setup script
└── README.md           # Project overview
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write code following the project's style guide
- Add tests for new functionality
- Update documentation as needed

### 3. Test Locally

```bash
# Run unit tests
pytest

# Run integration tests
docker-compose up --build
```

### 4. Submit a Pull Request

- Push your branch to GitHub
- Create a pull request with a clear description
- Wait for code review and CI checks to pass

## Common Tasks

### Adding a New Service

1. Create a new directory under `services/`
2. Add a `Dockerfile` for containerization
3. Update `ops/docker-compose.yml` to include the service
4. Document the service API in `docs/protocol.md`

### Running Tests

```bash
# Unit tests
pytest tests/

# Integration tests
pytest tests/integration/

# With coverage
pytest --cov=services tests/
```

### Debugging

1. Check logs:
   ```bash
   docker-compose logs -f control-plane
   ```

2. Access a running container:
   ```bash
   docker-compose exec control-plane /bin/bash
   ```

3. Use VS Code debugger with Docker attach

## Architecture Overview

MIaaS is built on a microservices architecture:

- **Control Plane**: Central orchestrator that receives inference requests, validates them, and routes to appropriate inference engines
- **Inference Engine**: Executes ML model inference using various frameworks (TensorFlow, PyTorch, etc.)
- **Model Registry**: Manages model versions, metadata, and storage

## Key Concepts

### Inference Request Flow

1. Client submits inference request to Control Plane
2. Control Plane validates request and model availability
3. Request is queued for processing
4. Inference Engine pulls request, loads model, and executes
5. Results are returned to client via Control Plane

### Model Management

- Models are versioned and stored in the Model Registry
- Each model has metadata (framework, input/output schemas)
- Models can be deployed, deprecated, or archived

## Resources

- [Protocol Specification](protocol.md) - API documentation
- [Architecture Overview](../README.md) - High-level design
- Project Wiki - Detailed guides and examples
- Issue Tracker - Report bugs or request features

## Getting Help

- **Slack**: #miaas-dev channel
- **Email**: dev-team@miaas.example.com
- **Office Hours**: Tuesdays 2-3 PM PST

## Contributing

We welcome contributions! Please:

1. Read the contribution guidelines
2. Follow the code style guide
3. Write tests for new features
4. Update documentation
5. Be respectful and collaborative

Happy coding! 🚀
