# MIaaS UI

React-based web interface for managing and monitoring the MIaaS cluster. Provides real-time visualization of registered nodes, their capabilities, and status.

## Features

- **Node Visualization**: Display all registered nodes in a responsive card-based layout
- **Real-Time Status**: Shows online/offline status with visual indicators
- **Capability Display**: CPU, memory, disk space, and GPU information
- **Auto-Refresh**: Reload button to fetch latest node data
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern Dark Theme**: Clean, professional interface with good contrast
- **Error Handling**: Graceful error states and loading indicators
- **Empty State**: Helpful message when no nodes are registered

## Tech Stack

- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and dev server
- **CSS3**: Flexbox/grid layouts with custom styling
- **Fetch API**: RESTful communication with control plane

## Screenshots

### Node List View
The main view shows all registered nodes with their details:
- Node name with status indicator (🟢 online / 🔴 offline)
- Unique node ID (truncated for readability)
- IP address
- Last seen timestamp
- System capabilities (CPU, RAM, GPU, disk)

### Empty State
When no nodes are registered, displays helpful message to get started.

## Development

### Prerequisites
- Node.js 18+ and npm
- Control plane running on port 8080 (or configured endpoint)

### Install Dependencies
```bash
cd ui
npm install
```

### Run Development Server
```bash
npm run dev
```

The UI will be available at http://localhost:5173

Development server features:
- Hot module replacement (HMR)
- Fast refresh
- Error overlay
- Auto-reload on file changes

### Environment Configuration

Create a `.env` file to configure the API endpoint:

```bash
# .env
VITE_API_BASE_URL=http://localhost:8080
```

**Note:** Vite requires the `VITE_` prefix for environment variables.

### Build for Production
```bash
npm run build
```

The production build will be in the `dist/` directory. This creates:
- Minified JavaScript bundles
- Optimized CSS
- Asset hashing for cache busting
- HTML with injected script/style tags

### Preview Production Build
```bash
npm run preview
```

### Linting
```bash
npm run lint
```

## Docker Deployment

### Build Image
```bash
docker build -t miaas-ui .
```

The Dockerfile uses a multi-stage build:
1. **Build stage**: Compiles React app with Vite
2. **Runtime stage**: Serves static files with nginx

### Run Container
```bash
# Run standalone
docker run -p 3000:80 miaas-ui

# Access at http://localhost:3000
```

### Docker Compose
The UI can be included in docker-compose.yml:

```yaml
ui:
  build: ./ui
  ports:
    - "3000:80"
  depends_on:
    - control-plane
  environment:
    - API_BASE_URL=http://control-plane:8080
```

## Components

### App.jsx
Main application component with the following responsibilities:

**State Management:**
- `nodes`: Array of node objects from API
- `loading`: Boolean for loading state
- `error`: Error message string

**Functions:**
- `fetchNodes()`: Fetches nodes from `/api/v1/nodes` endpoint
- Called on component mount via `useEffect`
- Can be triggered manually with refresh button

**Layout:**
- Header with title and refresh button
- Error display when API fails
- Loading indicator during fetch
- NodeList component with fetched nodes

### NodeList.jsx
Container component for displaying nodes:

**Props:**
- `nodes`: Array of node objects

**Behavior:**
- Shows empty state message if no nodes
- Renders grid layout of NodeCard components
- Responsive grid: 3 columns desktop, 2 tablet, 1 mobile

**Styling:**
- CSS Grid with gap between cards
- Centered empty state message
- Responsive breakpoints

### NodeCard.jsx
Individual node card component:

**Props:**
- `node`: Object with id, name, ip, status, last_seen, capabilities

**Display Elements:**
- Status indicator: 🟢 (online) or 🔴 (offline)
- Node name and truncated ID
- IP address
- Last seen timestamp (formatted)
- Capability badges:
  - CPU cores
  - Memory (GB)
  - GPU count (if available)
  - Disk space (GB)

**Styling:**
- Card with border and shadow
- Dark theme with gray tones
- Hover effect for interactivity
- Badge system for capabilities

## API Integration

The UI communicates with the control plane via RESTful API:

### Endpoints Used

```javascript
// Fetch all nodes
GET /api/v1/nodes

// Response format:
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "worker-01",
    "ip": "192.168.1.10",
    "status": "online",
    "last_seen": 1704067200.123,
    "capabilities": {
      "os": "linux",
      "cpu_count": 8,
      "mem_mb": 16000,
      "disk_mb": 500000,
      "gpus": []
    }
  }
]
```

### Error Handling

The UI handles various error scenarios:
- Network errors (control plane unreachable)
- HTTP errors (4xx, 5xx responses)
- Empty response (no nodes registered)
- Malformed JSON responses

### CORS Configuration

When running locally, ensure control plane allows CORS:

```python
# control-plane/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Proxy Setup (Docker)

When running with docker-compose, nginx proxies API requests:

```nginx
location /api/ {
    proxy_pass http://control-plane:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## Future Enhancements

Planned features for the UI:

- ✅ Node list and status display (MVP complete)
- ⬜ Deployment creation interface
- ⬜ Template selection and configuration
- ⬜ Real-time log streaming
- ⬜ Node detail modal with metrics graphs
- ⬜ Deployment status tracking
- ⬜ Service catalog with install buttons
- ⬜ User authentication and RBAC
- ⬜ Dark/light theme toggle

## Troubleshooting

### UI Shows "No nodes registered"

**Solutions:**
- Verify control plane is running: `curl http://localhost:8080/api/v1/nodes`
- Check agent is running and registered
- Look at browser console for API errors

### CORS Errors in Browser

**Error:** `Access to fetch at 'http://localhost:8080' from origin 'http://localhost:5173' has been blocked`

**Solution:** Ensure control plane has CORS middleware configured to allow localhost:5173

### UI Not Loading

**Solutions:**
- Check dev server is running: `npm run dev`
- Verify port 5173 is not in use
- Clear browser cache and reload
- Check browser console for JavaScript errors

## Related Documentation

- [Control Plane README](../control-plane/README.md) - API endpoints
- [Quick Start Guide](../QUICKSTART.md) - Getting started
- [Onboarding Guide](../docs/onboarding.md) - Development workflow
