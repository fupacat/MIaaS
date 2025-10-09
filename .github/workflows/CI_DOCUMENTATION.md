# CI/CD Workflow Documentation

## Overview

This document explains the CI/CD pipeline for the MIaaS (Model Infrastructure as a Service) project. The pipeline is designed to handle a multi-component architecture with graceful error handling for components that may not exist yet during early development stages.

## Workflow File

**Location**: `.github/workflows/ci.yml`

## Triggers

The CI pipeline runs automatically on:
- **Push** to `main` or `master` branches
- **Pull Requests** targeting `main` or `master` branches

This dual-branch approach supports both `main` (modern convention) and `master` (legacy) branch naming.

## Architecture

The workflow consists of 5 parallel jobs that test different components of the MIaaS platform:

### 1. Control Plane Tests (`control-plane` job)
**Purpose**: Test the FastAPI backend that orchestrates node management and service deployments.

**Steps**:
1. Checkout code
2. Set up Python 3.11
3. Cache pip dependencies for faster builds
4. Install dependencies from `control-plane/requirements.txt`
5. Run pytest tests in `control-plane/tests/`
6. Run flake8 linting (error-only mode)

**Requirements**:
- Python 3.11
- Dependencies: FastAPI, uvicorn, pydantic, sqlalchemy, pytest, httpx

**Error Handling**:
- Fails if `control-plane/requirements.txt` is missing
- Fails if tests fail
- Continues if linting finds non-critical issues

### 2. Agent Tests (`agent` job)
**Purpose**: Test the Python agent that runs on each node for capability reporting and deployment execution.

**Steps**:
1. Checkout code
2. Set up Python 3.11
3. Cache pip dependencies
4. Install dependencies from `agent/requirements.txt`
5. Compile-check `agent/agent.py`
6. Run pytest tests (if `agent/tests/` exists)
7. Run flake8 linting (error-only mode)

**Requirements**:
- Python 3.11
- Dependencies: requests, psutil

**Error Handling**:
- Fails if `agent/requirements.txt` is missing
- Continues if tests don't exist yet (early development)
- Continues if linting finds issues (warning only)

### 3. UI Build & Lint (`ui` job)
**Purpose**: Build and lint the React frontend for node management and service deployment.

**Steps**:
1. Checkout code
2. Set up Node.js 20
3. Cache node_modules for faster builds
4. Install dependencies with `npm ci`
5. Run ESLint on the codebase
6. Build production bundle with Vite

**Requirements**:
- Node.js 20
- Dependencies: React, Vite, ESLint

**Error Handling**:
- Exits gracefully if `ui/package.json` is missing
- Fails if dependencies install fails
- Fails if linting or build fails

### 4. Integration Tests (`integration` job)
**Purpose**: Run integration tests that verify cross-component interactions.

**Steps**:
1. Checkout code
2. Set up Python 3.11
3. Install root `requirements.txt` (if exists)
4. Run unittest discovery in `ci/tests/` directory

**Requirements**:
- Python 3.x
- pytest, pytest-flask (from root requirements.txt)

**Error Handling**:
- Continues if `ci/tests/` doesn't exist (expected in early stages)
- This is graceful to support architectural planning before implementation

### 5. Docker Build (`docker` job)
**Purpose**: Validate that all Docker images can be built successfully.

**Steps**:
1. Checkout code
2. Set up Docker Buildx
3. Build control-plane Docker image
4. Build agent Docker image
5. Build UI Docker image
6. Validate docker-compose.yml syntax

**Requirements**:
- Docker and Docker Buildx

**Error Handling**:
- All steps continue on error (non-blocking)
- Provides warnings if Dockerfiles are missing
- This allows development before containerization is complete

## Caching Strategy

The workflow uses GitHub Actions cache to speed up builds:

- **Python dependencies**: Cached by hashing `requirements.txt` files
- **Node modules**: Cached by hashing `package-lock.json`

Cache keys are OS-specific and include fallback keys for partial cache hits.

## Exit Codes and Failure Handling

### Critical Failures (Pipeline Stops)
- Control-plane dependency installation fails
- Control-plane tests fail
- Agent dependency installation fails
- UI dependency installation fails
- UI linting fails
- UI build fails

### Non-Critical (Continues with Warning)
- Agent tests don't exist yet
- Integration tests directory missing
- Docker builds fail
- Linting finds minor issues

## Local Testing

You can test the CI pipeline locally before pushing:

### Control Plane
```bash
cd control-plane
pip install -r requirements.txt
python -m pytest tests/ -v
flake8 . --select=E9,F63,F7,F82
```

### Agent
```bash
cd agent
pip install -r requirements.txt
python -m py_compile agent.py
flake8 . --select=E9,F63,F7,F82
```

### UI
```bash
cd ui
npm ci
npm run lint
npm run build
```

### Integration Tests
```bash
python -m unittest discover ci/tests
```

### Docker
```bash
docker build -t miaas-control-plane:test ./control-plane
docker build -t miaas-agent:test ./agent
docker build -t miaas-ui:test ./ui
docker-compose config
```

## CI Output Interpretation

### Success Indicators
- ✓ Green checkmarks in GitHub Actions UI
- All jobs show "Success" or "Skipped" (for optional components)
- Test output shows all tests passing

### Warning Indicators
- ⚠ Yellow warning icons (acceptable for early development)
- Messages like "directory not found, skipping tests"
- These are expected when components haven't been implemented yet

### Failure Indicators
- ✗ Red X marks in GitHub Actions UI
- Failed test assertions
- Syntax errors in code
- Missing required dependencies

## Troubleshooting

### "Requirements.txt not found"
**Cause**: Missing dependency file  
**Fix**: Create the appropriate requirements.txt file with needed dependencies

### "Tests failed"
**Cause**: Code changes broke existing functionality  
**Fix**: Review test output, fix the code or update tests if behavior change is intentional

### "Linting errors"
**Cause**: Code style issues or syntax errors  
**Fix**: Run flake8 locally and fix reported issues

### "Docker build failed"
**Cause**: Dockerfile syntax error or missing files  
**Fix**: Test Docker build locally with `docker build -t test ./directory`

### "npm ci failed"
**Cause**: Package.json/package-lock.json mismatch or network issues  
**Fix**: Delete node_modules and package-lock.json, run `npm install` locally, commit new lock file

## Future Enhancements

Potential improvements to the CI pipeline:

1. **Code Coverage**: Add coverage reports for Python and JavaScript tests
2. **Security Scanning**: Add dependency vulnerability scanning (Snyk, npm audit)
3. **Performance Testing**: Add load tests for API endpoints
4. **E2E Tests**: Add Playwright or Cypress tests for UI workflows
5. **Deployment**: Add CD stages for automatic deployment to staging/production
6. **Docker Registry**: Push built images to container registry
7. **Semantic Release**: Automate versioning and changelog generation

## Related Documentation

- **Main Architecture**: See `MIaaS.md` for complete system design
- **Testing Guide**: See `TESTING.md` for manual testing procedures
- **MVP Summary**: See `MVP_SUMMARY.md` for current implementation status
- **Quick Start**: See `QUICKSTART.md` for running the system locally

## Maintenance

**Last Updated**: 2024  
**Maintained By**: MIaaS Development Team  
**Review Cycle**: Update when adding new components or changing CI strategy

For questions or issues with the CI pipeline, please open a GitHub issue with the `ci/cd` label.
