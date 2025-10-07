"""Tests for API endpoints."""
import pytest
from app.api import app
from app.storage import storage


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Clear storage before each test
        storage._nodes.clear()
        yield client


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'


def test_register_node(client):
    """Test node registration endpoint."""
    node_data = {
        "id": "node-1",
        "hostname": "worker-01",
        "capabilities": ["docker", "compose"],
        "status": "active"
    }
    
    response = client.post('/api/v1/nodes/register', json=node_data)
    
    assert response.status_code == 201
    assert response.json['message'] == 'Node registered successfully'
    assert response.json['node']['id'] == 'node-1'
    assert response.json['node']['hostname'] == 'worker-01'
    assert response.json['node']['capabilities'] == ["docker", "compose"]


def test_register_node_missing_id(client):
    """Test node registration without ID."""
    node_data = {
        "hostname": "worker-01"
    }
    
    response = client.post('/api/v1/nodes/register', json=node_data)
    
    assert response.status_code == 400
    assert 'id' in response.json['error']


def test_register_node_missing_hostname(client):
    """Test node registration without hostname."""
    node_data = {
        "id": "node-1"
    }
    
    response = client.post('/api/v1/nodes/register', json=node_data)
    
    assert response.status_code == 400
    assert 'hostname' in response.json['error']


def test_register_node_no_data(client):
    """Test node registration without data."""
    response = client.post('/api/v1/nodes/register')
    
    assert response.status_code == 400


def test_list_nodes_empty(client):
    """Test listing nodes when none are registered."""
    response = client.get('/api/v1/nodes')
    
    assert response.status_code == 200
    assert response.json['nodes'] == []
    assert response.json['count'] == 0


def test_list_nodes(client):
    """Test listing registered nodes."""
    # Register two nodes
    node1 = {
        "id": "node-1",
        "hostname": "worker-01",
        "capabilities": ["docker"]
    }
    node2 = {
        "id": "node-2",
        "hostname": "worker-02",
        "capabilities": ["compose"]
    }
    
    client.post('/api/v1/nodes/register', json=node1)
    client.post('/api/v1/nodes/register', json=node2)
    
    response = client.get('/api/v1/nodes')
    
    assert response.status_code == 200
    assert response.json['count'] == 2
    assert len(response.json['nodes']) == 2


def test_get_node(client):
    """Test getting a specific node."""
    node_data = {
        "id": "node-1",
        "hostname": "worker-01",
        "capabilities": ["docker"]
    }
    
    client.post('/api/v1/nodes/register', json=node_data)
    
    response = client.get('/api/v1/nodes/node-1')
    
    assert response.status_code == 200
    assert response.json['id'] == 'node-1'
    assert response.json['hostname'] == 'worker-01'


def test_get_node_not_found(client):
    """Test getting a non-existent node."""
    response = client.get('/api/v1/nodes/non-existent')
    
    assert response.status_code == 404
    assert 'not found' in response.json['error'].lower()


def test_update_existing_node(client):
    """Test updating an existing node."""
    node_data = {
        "id": "node-1",
        "hostname": "worker-01",
        "capabilities": ["docker"]
    }
    
    # Register node
    client.post('/api/v1/nodes/register', json=node_data)
    
    # Update node
    updated_data = {
        "id": "node-1",
        "hostname": "worker-01-updated",
        "capabilities": ["docker", "compose"]
    }
    
    response = client.post('/api/v1/nodes/register', json=updated_data)
    
    assert response.status_code == 201
    assert response.json['node']['hostname'] == 'worker-01-updated'
    assert len(response.json['node']['capabilities']) == 2
    
    # Verify only one node exists
    list_response = client.get('/api/v1/nodes')
    assert list_response.json['count'] == 1
