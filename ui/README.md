# MIaaS UI

React-based user interface for the MIaaS control plane.

## Features

- Display registered nodes in a card-based layout
- Real-time node status and capabilities
- Refresh button to reload node list
- Responsive design with modern dark theme
- Error handling and loading states

## Tech Stack

- React 18
- Vite (build tool)
- Modern CSS with flexbox/grid
- Fetch API for backend communication

## Development

### Install dependencies
```bash
npm install
```

### Run development server
```bash
npm run dev
```

The UI will be available at http://localhost:5173

### Environment Configuration

Create a `.env` file to configure the API endpoint:
```bash
VITE_API_BASE_URL=http://localhost:8000
```

### Build for production
```bash
npm run build
```

The production build will be in the `dist/` directory.

## Docker

### Build image
```bash
docker build -t miaas-ui .
```

### Run container
```bash
docker run -p 3000:80 miaas-ui
```

## Components

### App.jsx
Main application component that:
- Fetches nodes from the control-plane API
- Manages loading and error states
- Provides refresh functionality

### NodeList.jsx
Displays a grid of node cards or empty state message.

### NodeCard.jsx
Individual node card showing:
- Node name with status indicator
- Node ID (truncated)
- IP address
- Status (online/offline)
- Last seen timestamp
- Capabilities (CPU, memory, GPU, etc.)

## Integration with Control Plane

The UI communicates with the control-plane via REST API:
- `GET /api/v1/nodes` - Fetch all registered nodes

When running with docker-compose, nginx proxies API requests to the control-plane service.
