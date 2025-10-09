# MIaaS - Model Inference as a Service

MIaaS is a scalable microservices platform for deploying and managing machine learning model inference workloads. It provides a unified API for submitting inference requests across multiple ML frameworks.

## Architecture Overview

MIaaS follows a microservices architecture with three core components:

### Core Services

1. **Control Plane** (`services/control-plane/`)
   - Central orchestrator for all inference requests
   - Validates requests and manages service lifecycle
   - Handles authentication and rate limiting
   - Exposes REST API on port 8080

2. **Inference Engine** (`services/inference-engine/`)
   - Executes model inference workloads
   - Supports multiple ML frameworks (TensorFlow, PyTorch, ONNX)
   - Scales horizontally based on demand
   - Pulls models from Model Registry

3. **Model Registry** (`services/model-registry/`)
   - Centralized model storage and versioning
   - Manages model metadata and schemas
   - Provides model discovery and retrieval APIs
   - Tracks model lifecycle (active, deprecated, archived)

### Communication Flow

```
Client → Control Plane → Message Queue → Inference Engine → Model Registry
                ↓                              ↓
            Response                        Results
```

1. Client submits inference request to Control Plane
2. Control Plane validates and queues request
3. Inference Engine processes request asynchronously
4. Results returned to client via Control Plane API

### Key Features

- **Multi-Framework Support**: TensorFlow, PyTorch, ONNX, and more
- **Horizontal Scaling**: Auto-scale inference engines based on load
- **Async Processing**: Non-blocking request handling with message queues
- **Model Versioning**: Track and manage multiple model versions
- **RESTful API**: Simple HTTP/JSON interface for all operations

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
├── services/           # Microservices
│   ├── control-plane/  # Request orchestration service
│   ├── inference-engine/ # Model execution service
│   └── model-registry/ # Model storage service
├── ops/                # Operations & deployment
│   └── docker-compose.yml # Container orchestration
├── docs/               # Documentation
│   ├── protocol.md     # API specifications
│   └── onboarding.md   # Developer onboarding guide
├── setup.ps1           # Development environment setup
└── README.md           # This file
```

## Quick Start

### Running the Control Plane

Start the control plane service using Docker Compose:

```bash
cd ops
docker-compose up -d
```

Verify the service is running:
```bash
curl http://localhost:8080/health
```

### Documentation

- **[Protocol Specification](docs/protocol.md)**: API endpoints and communication protocols
- **[Onboarding Guide](docs/onboarding.md)**: Comprehensive developer setup and workflow
- **[CI/CD Documentation](.github/workflows/CI_DOCUMENTATION.md)**: Continuous Integration pipeline details

## CI/CD Pipeline

The project uses automated CI/CD workflows that run on every push and pull request:

- **Control Plane Tests**: Python/FastAPI backend testing
- **Agent Tests**: Node agent validation and testing  
- **UI Build & Lint**: React frontend linting and building
- **Integration Tests**: Cross-component testing
- **Docker Builds**: Container image validation

For detailed information about the CI pipeline, triggers, error handling, and troubleshooting, see the [CI/CD Documentation](.github/workflows/CI_DOCUMENTATION.md).

## Contributing

1. Create a feature branch from `master`
2. Make your changes following the project conventions
3. Ensure CI passes locally before pushing (see [CI/CD Documentation](.github/workflows/CI_DOCUMENTATION.md#local-testing))
4. Submit a pull request with clear description

For detailed contribution guidelines, see [docs/onboarding.md](docs/onboarding.md).
