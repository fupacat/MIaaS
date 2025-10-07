# MIaaS Copilot Agent Instructions

## Repository Overview
**MIaaS (Model Infrastructure as a Service)** is an orchestration platform for deploying AI/ML infrastructure across distributed nodes. Currently in early planning phase - the repository contains architectural documentation and setup scripts, but NO implemented code yet.

**Key Files:**
- `MIaaS.md` - Complete system architecture, API contracts, data models, MVP roadmap
- `README.md` - VS Code + Copilot environment setup instructions
- `setup.ps1` - PowerShell automation script for repo initialization
- `docs/index.md` - GitHub Pages documentation landing page

**Target Architecture** (per MIaaS.md):
- **Control Plane**: FastAPI backend with orchestrator, template manager, and persistence (SQLite/Postgres)
- **Agent**: Python daemon on each node for capability reporting and deployment execution
- **UI**: React SPA for node management and service deployment
- **Templates**: Jinja2 templates for Docker Compose/K8s (Postgres, Ollama, Qdrant, Redis, etc.)

## Repository Structure
```
/
├── .github/
│   ├── workflows/          # CI/CD pipelines
│   │   ├── ci.yml         # Main CI - Python setup, test discovery, lint
│   │   ├── main.yml       # Duplicate CI workflow
│   │   ├── add-to-backlog.yml  # Auto-add issues to project
│   │   └── agent-triage-enrichment.yml  # Weekly backlog enrichment
│   ├── ISSUE_TEMPLATE/    # Bug, feature, story templates
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/                  # GitHub Pages content
├── MIaaS.md              # Complete architectural specification
├── README.md             # Setup instructions
└── setup.ps1             # Automated VS Code + GitHub setup
```

**Future Structure** (when implementing, per MIaaS.md):
- `control-plane/` - FastAPI app, orchestrator, DB, auth
- `agent/` - Node agent (agent.py, executor.py, reporter.py)
- `ui/` - React frontend
- `templates/` - Jinja2 compose/k8s templates
- `ops/` - Infrastructure for running control-plane itself
- `scripts/` - Build scripts, install-agent.sh, devctl CLI
- `ci/tests/` - Unit, integration, contract tests

## Build & Validation Commands

### Current State (Documentation Only)
**NO Python code exists yet.** CI workflows are configured but currently no-op:

```bash
# Python setup (no requirements.txt exists currently)
python3 --version  # Works: Python 3.12.3
pip3 --version     # Works

# Test discovery (no tests exist yet)
python3 -m unittest discover ci/tests  # WILL FAIL: ci/tests/ doesn't exist

# Linting (not installed by default)
flake8 .  # WILL FAIL: flake8 not available unless manually installed
```

### When Code Implementation Begins
Based on MIaaS.md architecture, these commands will be needed:

**Dependencies:**
```bash
# For control-plane (FastAPI)
pip install fastapi uvicorn pydantic sqlalchemy jinja2 pyjwt

# For agent  
pip install requests psutil docker

# For testing
pip install pytest httpx testcontainers

# For linting
pip install flake8 black
```

**Development workflow:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run control-plane locally (when implemented)
cd control-plane && uvicorn app.main:app --reload --port 8080

# 3. Run agent (when implemented)
cd agent && python3 agent/agent.py

# 4. Run tests (when created)
pytest ci/tests/ -v

# 5. Lint code
flake8 . --max-line-length=120
black . --check

# 6. Build Docker containers (when Dockerfiles exist)
docker-compose -f ops/docker-compose.yml build
docker-compose -f ops/docker-compose.yml up
```

## CI/CD Pipeline Details

**Triggers:** Push/PR to `main` or `master` branches

**Workflow: .github/workflows/ci.yml**
1. Checkout code
2. Set up Python 3.x
3. Install dependencies: `pip install -r requirements.txt` (continues on error if file missing)
4. Run tests: `python -m unittest discover ci/tests` (only if directory exists)
5. Lint: `flake8 .` (only if flake8 is available)
6. Build: Echo placeholder

**Workflow: .github/workflows/main.yml** (duplicate, similar to ci.yml)

**Weekly Automation:**
- `agent-triage-enrichment.yml` - Runs Mondays 6am UTC, checks backlog issues for "fully fleshed out" status
- `add-to-backlog.yml` - Auto-adds issues with 'backlog' label to project board

**Dependabot:** Weekly updates for pip packages and GitHub Actions

## Development Workflow

### Issue & Story Handling
- **Only work on issues in "Ready" state** with "fully fleshed out" checkbox marked
- Branch naming: `feature/{issue-number}-description` or `bug/{issue-number}-description`
- Reference issues in commits: `Closes #42`
- CI must pass before merge

### PR Requirements (from template)
- [ ] Code compiles and passes tests
- [ ] Linting and formatting checks pass
- [ ] Documentation updated
- [ ] Linked to issue
- [ ] No sensitive data

### Testing Strategy (per MIaaS.md)
When implementing:
- **Unit tests**: Template rendering, placement logic, capability detection
- **Integration tests**: Docker-in-Docker for agent compose execution
- **Contract tests**: FastAPI endpoints using pytest + httpx + testcontainers
- **E2E tests**: Spin up control-plane + agent, deploy hello-world compose

## Critical Notes & Workarounds

### Current State Workarounds
1. **No requirements.txt**: Create one when adding Python dependencies. CI will continue-on-error if missing.
2. **No tests yet**: CI checks for `ci/tests/` before running - won't fail if absent.
3. **No flake8**: CI checks if flake8 command exists before running - won't fail if missing.
4. **Duplicate CI workflows**: Both `ci.yml` and `main.yml` exist - consider consolidating.

### When Implementing Code
1. **Docker socket security**: Agent should NOT mount `/var/run/docker.sock` by default - use opt-in (per MIaaS.md security section)
2. **Template rendering**: Use Jinja2 with strict undefined mode to catch missing variables
3. **Agent auth**: Use node-specific JWT tokens issued at registration (per MIaaS.md protocol section)
4. **Database**: Start with SQLite for MVP, design for Postgres migration (per MIaaS.md)
5. **Python version**: Target Python 3.10+ (asyncio features needed for agent)

### PowerShell Setup Script Notes
- `setup.ps1` requires PowerShell 7+ and GitHub CLI (`gh`)
- Installs Copilot extensions, creates repo, pushes initial commit
- Interactive - prompts for repo name and owner
- Check `gh auth status` if repo creation fails

## Technology Stack (from MIaaS.md)
- **Backend**: FastAPI (Python) with Pydantic models
- **Agent**: Python (asyncio) - Go option for compiled binary later
- **UI**: React + Tailwind/Mantine
- **Templates**: Jinja2
- **Database**: SQLite (MVP) → Postgres (production)
- **Auth**: PyJWT, optional Keycloak later
- **Container execution**: Docker Compose CLI or Python Docker SDK
- **Testing**: pytest, httpx, testcontainers

## Project Board States
- **Backlog**: Needs enrichment/context
- **Ready**: Fully specified, ready for implementation
- **In progress**: Active work
- **In review**: Awaiting approval
- **Done**: Merged and closed

## Key Principles
1. **Trust these instructions** - only search if information is incomplete or incorrect
2. **Reference MIaaS.md** for all architectural decisions and implementation details
3. **Check issue state** before starting work - must be in "Ready" with "fully fleshed out" checked
4. **Run CI locally** before pushing - ensure tests pass and code lints
5. **Update docs** - Keep README.md and docs/ synchronized with code changes
6. **Security first** - No hardcoded secrets, use environment variables and secure secret storage