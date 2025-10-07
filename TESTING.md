# Testing Guide

This document describes how to test the MIaaS UI skeleton implementation.

## Prerequisites

- Python 3.11+
- Node.js 20+
- npm or yarn

## Local Development Testing

### 1. Test Control Plane

Start the control plane:
```bash
cd control-plane
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

In another terminal, test the API:
```bash
# Health check
curl http://localhost:8000/
# Expected: {"message":"MIaaS Control Plane API","version":"0.1.0"}

# List nodes (initially empty)
curl http://localhost:8000/api/v1/nodes
# Expected: []

# Register a test node
curl -X POST http://localhost:8000/api/v1/nodes/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-node-1",
    "ip": "192.168.1.100",
    "capabilities": {
      "cpu": "8 cores",
      "memory": "16GB",
      "gpu": "NVIDIA RTX 3090",
      "docker": true
    }
  }'

# List nodes again
curl http://localhost:8000/api/v1/nodes
# Expected: Array with one node
```

Or use the seed script:
```bash
cd control-plane
./seed_data.sh
```

### 2. Test UI

With the control plane still running, start the UI:
```bash
cd ui
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

**Expected Results:**
- Purple gradient header with "MIaaS Control Plane" title
- "Nodes" section with refresh button
- Node cards displaying:
  - Green status indicator for online nodes
  - Node name as heading
  - Truncated ID
  - IP address
  - Status (online)
  - Last seen timestamp
  - Capabilities as colored tags

**Test Actions:**
1. Click the "Refresh" button - should reload node list
2. Register new nodes via API - click refresh to see them appear
3. Check browser console for errors (should be none)

### 3. Test UI Build

Build the production UI:
```bash
cd ui
npm run build
```

**Expected:**
- Build completes successfully
- `dist/` directory created with:
  - `index.html`
  - `assets/` directory with JS and CSS files

## Integration Testing

### Test with Docker Compose (if Docker is available)

```bash
cd ops
docker compose up --build
```

**Expected:**
- Both services start successfully
- Control plane accessible at http://localhost:8000
- UI accessible at http://localhost:3000
- API calls from UI routed through nginx proxy

## Manual Test Checklist

Control Plane:
- [ ] Server starts without errors
- [ ] Health endpoint returns correct response
- [ ] Empty node list returns `[]`
- [ ] Node registration succeeds and returns ID + token
- [ ] Registered nodes appear in list
- [ ] CORS headers present in responses

UI:
- [ ] Development server starts without errors
- [ ] Page loads without console errors
- [ ] Header displays correctly
- [ ] Empty state shows when no nodes registered
- [ ] Node cards display after registration
- [ ] All node information visible and formatted correctly
- [ ] Refresh button works
- [ ] Loading state shows during fetch
- [ ] Error state shows if API unreachable

Build:
- [ ] Control plane imports successfully
- [ ] UI production build completes
- [ ] No TypeScript/ESLint errors (if applicable)

## Known Issues

- Docker builds may fail in CI environments with SSL certificate issues
  - This is an environment issue, not a code issue
  - Local builds and runs work correctly
- Node list uses in-memory storage and resets on control plane restart
  - This is expected for the MVP

## Testing Future Features

When implementing additional features, test:

### Node Agent (Sprint 2)
- Agent registration with capabilities
- Heartbeat mechanism
- Capability reporting accuracy

### Templates (Sprint 2)
- Template rendering
- Deployment to nodes
- Status reporting

### Authentication (Sprint 3)
- JWT token generation
- Node token validation
- User session management
