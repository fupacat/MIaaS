"""Tests for FastAPI endpoints."""


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    assert 'version' in response.json()


def test_register_node(client):
    """Test node registration endpoint."""
    node_data = {
        "name": "worker-01",
        "ip": "192.168.1.10",
        "capabilities": {
            "os": "linux",
            "cpu_count": 8,
            "mem_mb": 32000,
            "gpus": []
        }
    }
    
    response = client.post('/api/v1/nodes/register', json=node_data)
    
    assert response.status_code == 201
    data = response.json()
    assert 'node_id' in data
    assert 'node_token' in data
    assert data['control_plane_url'] == 'http://localhost:8080'


def test_register_node_missing_fields(client):
    """Test node registration with missing fields."""
    node_data = {
        "name": "worker-01"
    }
    
    response = client.post('/api/v1/nodes/register', json=node_data)
    
    assert response.status_code == 422  # FastAPI validation error


def test_list_nodes_empty(client):
    """Test listing nodes when none are registered."""
    response = client.get('/api/v1/nodes')
    
    assert response.status_code == 200
    assert response.json() == []


def test_list_nodes(client):
    """Test listing registered nodes."""
    # Register two nodes
    node1 = {
        "name": "worker-01",
        "ip": "192.168.1.10",
        "capabilities": {
            "os": "linux",
            "cpu_count": 8,
            "mem_mb": 16000,
            "gpus": []
        }
    }
    node2 = {
        "name": "worker-02",
        "ip": "192.168.1.11",
        "capabilities": {
            "os": "linux",
            "cpu_count": 4,
            "mem_mb": 8000,
            "gpus": []
        }
    }
    
    client.post('/api/v1/nodes/register', json=node1)
    client.post('/api/v1/nodes/register', json=node2)
    
    response = client.get('/api/v1/nodes')
    
    assert response.status_code == 200
    nodes = response.json()
    assert len(nodes) == 2


def test_get_node(client):
    """Test getting a specific node."""
    node_data = {
        "name": "worker-01",
        "ip": "192.168.1.10",
        "capabilities": {
            "os": "linux",
            "cpu_count": 8,
            "mem_mb": 16000,
            "gpus": []
        }
    }
    
    reg_response = client.post('/api/v1/nodes/register', json=node_data)
    node_id = reg_response.json()['node_id']
    
    response = client.get(f'/api/v1/nodes/{node_id}')
    
    assert response.status_code == 200
    node = response.json()
    assert node['id'] == node_id
    assert node['name'] == 'worker-01'


def test_get_node_not_found(client):
    """Test getting a non-existent node."""
    response = client.get('/api/v1/nodes/non-existent')
    
    assert response.status_code == 404


def test_update_existing_node(client):
    """Test updating an existing node by re-registering."""
    node_data = {
        "name": "worker-01",
        "ip": "192.168.1.10",
        "capabilities": {
            "os": "linux",
            "cpu_count": 8,
            "mem_mb": 16000,
            "gpus": []
        }
    }
    
    # Register node
    reg_response = client.post('/api/v1/nodes/register', json=node_data)
    node_id = reg_response.json()['node_id']
    
    # Update node with same name
    updated_data = {
        "name": "worker-01",
        "ip": "192.168.1.20",
        "capabilities": {
            "os": "linux",
            "cpu_count": 16,
            "mem_mb": 32000,
            "gpus": [{"id": 0, "model": "RTX 3090"}]
        }
    }
    
    response = client.post('/api/v1/nodes/register', json=updated_data)
    
    assert response.status_code == 201
    # Should return same node_id since we're updating by name
    assert response.json()['node_id'] == node_id
    
    # Verify only one node exists
    list_response = client.get('/api/v1/nodes')
    assert len(list_response.json()) == 1


def test_heartbeat(client):
    """Test node heartbeat endpoint."""
    # Register a node first
    node_data = {
        "name": "worker-01",
        "ip": "192.168.1.10",
        "capabilities": {
            "os": "linux",
            "cpu_count": 8,
            "mem_mb": 16000,
            "gpus": []
        }
    }
    
    reg_response = client.post('/api/v1/nodes/register', json=node_data)
    node_id = reg_response.json()['node_id']
    
    # Send heartbeat
    heartbeat_data = {
        "cpu_usage": 45.5,
        "mem_usage": 60.2,
        "disk_free_mb": 50000,
        "running_containers": ["postgres", "redis"]
    }
    
    response = client.post(f'/api/v1/nodes/{node_id}/heartbeat', json=heartbeat_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'ok'
    assert 'timestamp' in data


def test_heartbeat_not_found(client):
    """Test heartbeat for non-existent node."""
    heartbeat_data = {
        "cpu_usage": 45.5,
        "mem_usage": 60.2,
        "disk_free_mb": 50000,
        "running_containers": []
    }
    
    response = client.post('/api/v1/nodes/non-existent/heartbeat', json=heartbeat_data)
    
    assert response.status_code == 404
