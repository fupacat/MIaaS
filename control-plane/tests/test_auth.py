"""Tests for JWT authentication."""
import pytest
import jwt
import time
from app.auth import create_node_token, verify_node_token, get_current_node
from app.auth.jwt_utils import JWT_SECRET, JWT_ALGORITHM


def test_create_node_token():
    """Test JWT token creation."""
    node_id = "test-node-123"
    node_name = "test-worker"
    
    token = create_node_token(node_id, node_name)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Decode without verification to check payload
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    assert payload["node_id"] == node_id
    assert payload["node_name"] == node_name
    assert payload["type"] == "node_agent"
    assert "iat" in payload
    assert "exp" in payload


def test_verify_valid_token():
    """Test verification of a valid token."""
    node_id = "test-node-456"
    node_name = "test-worker-2"
    
    token = create_node_token(node_id, node_name)
    payload = verify_node_token(token)
    
    assert payload is not None
    assert payload["node_id"] == node_id
    assert payload["node_name"] == node_name
    assert payload["type"] == "node_agent"


def test_verify_invalid_token():
    """Test verification of an invalid token."""
    invalid_token = "invalid.token.string"
    
    payload = verify_node_token(invalid_token)
    
    assert payload is None


def test_verify_expired_token():
    """Test verification of an expired token."""
    node_id = "test-node-789"
    node_name = "test-worker-3"
    
    # Create a token that's already expired
    now = time.time()
    expired_payload = {
        "node_id": node_id,
        "node_name": node_name,
        "iat": int(now - 3600),
        "exp": int(now - 1800),  # Expired 30 minutes ago
        "type": "node_agent",
    }
    
    expired_token = jwt.encode(expired_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    payload = verify_node_token(expired_token)
    
    assert payload is None


def test_verify_wrong_token_type():
    """Test verification of a token with wrong type."""
    # Create a token with wrong type
    wrong_type_payload = {
        "node_id": "test-node",
        "node_name": "test",
        "iat": int(time.time()),
        "exp": int(time.time() + 3600),
        "type": "user",  # Wrong type
    }
    
    token = jwt.encode(wrong_type_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    payload = verify_node_token(token)
    
    assert payload is None


def test_get_current_node():
    """Test extracting node ID from token."""
    node_id = "test-node-101"
    node_name = "test-worker-4"
    
    token = create_node_token(node_id, node_name)
    extracted_node_id = get_current_node(token)
    
    assert extracted_node_id == node_id


def test_get_current_node_invalid_token():
    """Test extracting node ID from invalid token."""
    invalid_token = "invalid.token"
    
    node_id = get_current_node(invalid_token)
    
    assert node_id is None


def test_register_node_returns_jwt(client):
    """Test that node registration returns a JWT token."""
    node_data = {
        "name": "worker-jwt-test",
        "ip": "192.168.1.50",
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
    assert 'node_token' in data
    
    # Verify it's a valid JWT
    token = data['node_token']
    payload = verify_node_token(token)
    
    assert payload is not None
    assert payload['node_id'] == data['node_id']
    assert payload['node_name'] == node_data['name']


def test_heartbeat_requires_auth(client):
    """Test that heartbeat endpoint requires authentication."""
    # Register a node first
    node_data = {
        "name": "worker-auth-test",
        "ip": "192.168.1.60",
        "capabilities": {
            "os": "linux",
            "cpu_count": 4,
            "mem_mb": 16000,
            "gpus": []
        }
    }
    
    reg_response = client.post('/api/v1/nodes/register', json=node_data)
    node_id = reg_response.json()['node_id']
    
    # Try to send heartbeat without token
    heartbeat_data = {
        "cpu_usage": 50.0,
        "mem_usage": 60.0,
        "disk_free_mb": 100000,
        "running_containers": []
    }
    
    response = client.post(f'/api/v1/nodes/{node_id}/heartbeat', json=heartbeat_data)
    
    assert response.status_code == 401


def test_heartbeat_with_valid_token(client):
    """Test heartbeat with valid JWT token."""
    # Register a node
    node_data = {
        "name": "worker-valid-token",
        "ip": "192.168.1.70",
        "capabilities": {
            "os": "linux",
            "cpu_count": 8,
            "mem_mb": 32000,
            "gpus": []
        }
    }
    
    reg_response = client.post('/api/v1/nodes/register', json=node_data)
    node_id = reg_response.json()['node_id']
    token = reg_response.json()['node_token']
    
    # Send heartbeat with token
    heartbeat_data = {
        "cpu_usage": 50.0,
        "mem_usage": 60.0,
        "disk_free_mb": 100000,
        "running_containers": []
    }
    
    response = client.post(
        f'/api/v1/nodes/{node_id}/heartbeat',
        json=heartbeat_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_heartbeat_with_invalid_token(client):
    """Test heartbeat with invalid JWT token."""
    # Register a node
    node_data = {
        "name": "worker-invalid-token",
        "ip": "192.168.1.80",
        "capabilities": {
            "os": "linux",
            "cpu_count": 4,
            "mem_mb": 16000,
            "gpus": []
        }
    }
    
    reg_response = client.post('/api/v1/nodes/register', json=node_data)
    node_id = reg_response.json()['node_id']
    
    # Send heartbeat with invalid token
    heartbeat_data = {
        "cpu_usage": 50.0,
        "mem_usage": 60.0,
        "disk_free_mb": 100000,
        "running_containers": []
    }
    
    response = client.post(
        f'/api/v1/nodes/{node_id}/heartbeat',
        json=heartbeat_data,
        headers={"Authorization": "Bearer invalid.token.string"}
    )
    
    assert response.status_code == 401


def test_heartbeat_with_mismatched_node_id(client):
    """Test heartbeat when token node_id doesn't match URL node_id."""
    # Register two nodes
    node1_data = {
        "name": "worker-node-1",
        "ip": "192.168.1.90",
        "capabilities": {
            "os": "linux",
            "cpu_count": 4,
            "mem_mb": 16000,
            "gpus": []
        }
    }
    
    node2_data = {
        "name": "worker-node-2",
        "ip": "192.168.1.91",
        "capabilities": {
            "os": "linux",
            "cpu_count": 4,
            "mem_mb": 16000,
            "gpus": []
        }
    }
    
    reg1_response = client.post('/api/v1/nodes/register', json=node1_data)
    node1_id = reg1_response.json()['node_id']
    
    reg2_response = client.post('/api/v1/nodes/register', json=node2_data)
    node2_id = reg2_response.json()['node_id']
    node2_token = reg2_response.json()['node_token']
    
    # Try to send heartbeat for node1 using node2's token
    heartbeat_data = {
        "cpu_usage": 50.0,
        "mem_usage": 60.0,
        "disk_free_mb": 100000,
        "running_containers": []
    }
    
    response = client.post(
        f'/api/v1/nodes/{node1_id}/heartbeat',
        json=heartbeat_data,
        headers={"Authorization": f"Bearer {node2_token}"}
    )
    
    assert response.status_code == 403
    assert "different node" in response.json()['detail'].lower()
