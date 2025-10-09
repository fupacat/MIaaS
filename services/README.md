# Services Directory - Legacy Placeholder

⚠️ **Note**: This directory contains legacy placeholder documentation from the original project concept.

## Current Implementation

The actual implementation of MIaaS uses a different structure:

- **[control-plane/](../control-plane/)** - FastAPI backend (implemented)
- **[agent/](../agent/)** - Node agent daemon (implemented)
- **[ui/](../ui/)** - React web interface (implemented)

## Legacy Services (Not Implemented)

The files in this directory describe the original "Model Inference as a Service" concept:
- `services/control-plane/` - Original inference orchestrator (superseded by `control-plane/`)
- `services/inference-engine/` - Inference execution service (not implemented)
- `services/model-registry/` - Model storage service (not implemented)

## Current Architecture

MIaaS has evolved into a **Model Infrastructure as a Service** platform focused on:
- Distributed node management
- Infrastructure orchestration
- Deployment automation

See the main [README.md](../README.md) and [MIaaS.md](../MIaaS.md) for the current architecture.

## For New Contributors

**Ignore this directory** and refer to:
- [QUICKSTART.md](../QUICKSTART.md) - Get started
- [docs/onboarding.md](../docs/onboarding.md) - Developer guide
- [control-plane/README.md](../control-plane/README.md) - API documentation
- [agent/README.md](../agent/README.md) - Agent configuration
- [ui/README.md](../ui/README.md) - UI development
