# MIaaS Operations

⚠️ **Note**: This directory contains legacy deployment configurations. 

## Recommended Approach

**Use the root-level `docker-compose.yml` instead:**

```bash
cd ..
docker-compose up --build
```

See [QUICKSTART.md](../QUICKSTART.md) for detailed instructions.

## Legacy Files

The files in this directory are from the original project structure:
- `docker-compose.yml` - Legacy compose file (broken, do not use)
- `README.md` - This file

## Current Deployment

For deploying MIaaS, use the root-level files:
- **[docker-compose.yml](../docker-compose.yml)** - Main orchestration file
- **[QUICKSTART.md](../QUICKSTART.md)** - Deployment guide
- **[control-plane/Dockerfile](../control-plane/Dockerfile)** - Control plane container
- **[agent/Dockerfile](../agent/Dockerfile)** - Agent container
- **[ui/Dockerfile](../ui/Dockerfile)** - UI container

---

## Original Content (For Reference Only)

### Quick Start (Outdated)

## Services

### control-plane
- **Port**: 8000
- **Description**: FastAPI backend for node management
- **Health check**: http://localhost:8000/

### ui
- **Port**: 3000
- **Description**: React UI with nginx
- **Access**: http://localhost:3000/

The UI is configured to proxy API requests to the control-plane service via nginx.

## Architecture

```
┌─────────┐         ┌──────────────┐         ┌───────────────┐
│ Browser │ ─────> │  UI (nginx)  │ ─────> │ Control Plane │
│         │ :3000   │     :80      │         │     :8000     │
└─────────┘         └──────────────┘         └───────────────┘
                           │
                           │ Proxy /api -> control-plane:8000
                           ▼
```

## Local Development

For faster iteration during development, run services separately:

### Terminal 1: Control Plane
```bash
cd ../control-plane
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2: UI
```bash
cd ../ui
npm install
npm run dev
```

UI will be at http://localhost:5173 in dev mode.

## Testing

### Seed test data
```bash
# Start the control-plane first
docker compose up control-plane -d

# Then seed data
cd ../control-plane
./seed_data.sh
```

### View logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f control-plane
docker compose logs -f ui
```

## Troubleshooting

### Cannot connect to control-plane
- Ensure control-plane is running: `docker compose ps`
- Check logs: `docker compose logs control-plane`
- Verify port 8000 is not in use: `lsof -i :8000`

### UI shows connection error
- Check that control-plane is healthy at http://localhost:8000/
- Verify CORS is enabled in control-plane
- Check browser console for errors

### Port conflicts
If ports 3000 or 8000 are already in use, modify `docker-compose.yml`:
```yaml
ports:
  - "3001:80"  # Change 3000 to 3001
```
