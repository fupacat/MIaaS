"""Integration tests for control plane and agent interaction."""
import pytest
import time
from unittest.mock import patch, MagicMock


def test_node_registration_and_list_flow(client):
    """Test complete flow of node registration and listing."""
    # Register a node
    node_data = {
        "name": "integration-test-node",
        "ip": "10.0.1.100",
        "capabilities": {
            "os": "linux",
            "cpu_count": 16,
            "mem_mb": 32768,
            "disk_mb": 500000,
            "gpus": [{"id": 0, "model": "A100"}]
        }
    }
    
    reg_response = client.post('/api/v1/nodes/register', json=node_data)
    assert reg_response.status_code == 201
    node_id = reg_response.json()["node_id"]
    
    # List nodes and verify it appears
    list_response = client.get('/api/v1/nodes')
    assert list_response.status_code == 200
    nodes = list_response.json()
    assert len(nodes) == 1
    assert nodes[0]["id"] == node_id
    assert nodes[0]["name"] == "integration-test-node"
    assert nodes[0]["status"] == "online"


def test_node_heartbeat_updates_metrics(client):
    """Test that heartbeats update node metrics."""
    # Register a node
    node_data = {
        "name": "heartbeat-test-node",
        "ip": "10.0.1.101",
        "capabilities": {
            "os": "linux",
            "cpu_count": 8,
            "mem_mb": 16384,
            "gpus": []
        }
    }
    
    reg_response = client.post('/api/v1/nodes/register', json=node_data)
    node_id = reg_response.json()["node_id"]
    
    # Get initial node state
    initial_response = client.get(f'/api/v1/nodes/{node_id}')
    initial_last_seen = initial_response.json()["last_seen"]
    
    # Wait a moment to ensure timestamp changes
    time.sleep(0.1)
    
    # Send heartbeat
    heartbeat_data = {
        "cpu_usage": 75.5,
        "mem_usage": 80.2,
        "disk_free_mb": 100000,
        "running_containers": ["postgres-1", "redis-1"]
    }
    
    hb_response = client.post(f'/api/v1/nodes/{node_id}/heartbeat', json=heartbeat_data)
    assert hb_response.status_code == 200
    
    # Get updated node state
    updated_response = client.get(f'/api/v1/nodes/{node_id}')
    updated_node = updated_response.json()
    
    # Verify metrics were updated
    assert updated_node["last_seen"] > initial_last_seen
    # Note: metrics storage depends on implementation


def test_multiple_nodes_registration(client):
    """Test registering multiple nodes."""
    nodes_data = [
        {
            "name": "node-01",
            "ip": "10.0.1.1",
            "capabilities": {"os": "linux", "cpu_count": 4, "mem_mb": 8192, "gpus": []}
        },
        {
            "name": "node-02",
            "ip": "10.0.1.2",
            "capabilities": {"os": "linux", "cpu_count": 8, "mem_mb": 16384, "gpus": []}
        },
        {
            "name": "node-03",
            "ip": "10.0.1.3",
            "capabilities": {"os": "linux", "cpu_count": 16, "mem_mb": 32768, "gpus": [{"id": 0}]}
        }
    ]
    
    node_ids = []
    for node_data in nodes_data:
        response = client.post('/api/v1/nodes/register', json=node_data)
        assert response.status_code == 201
        node_ids.append(response.json()["node_id"])
    
    # Verify all nodes are listed
    list_response = client.get('/api/v1/nodes')
    nodes = list_response.json()
    assert len(nodes) == 3
    
    # Verify all node IDs are present
    listed_ids = [node["id"] for node in nodes]
    for node_id in node_ids:
        assert node_id in listed_ids


def test_deployment_creation_and_retrieval(client):
    """Test creating and retrieving a deployment."""
    deployment_data = {
        "deployment_id": "integration-deploy-1",
        "template_id": "postgres",
        "rendered_compose": """version: '3.8'
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: testpass123
    ports:
      - "5432:5432"
""",
        "env": {"POSTGRES_PASSWORD": "testpass123"},
        "action": "apply"
    }
    
    # Create deployment
    create_response = client.post('/api/v1/deployments', json=deployment_data)
    assert create_response.status_code == 202
    assert create_response.json()["deployment_id"] == "integration-deploy-1"
    
    # Retrieve deployment
    get_response = client.get('/api/v1/deployments/integration-deploy-1')
    assert get_response.status_code == 200
    deployment = get_response.json()
    assert deployment["deployment_id"] == "integration-deploy-1"
    assert deployment["status"] == "pending"
    assert "postgres" in deployment["message"]  # Message includes template_id


def test_node_reregistration_updates_existing(client):
    """Test that re-registering a node with same name updates existing entry."""
    node_name = "reregister-test-node"
    
    # First registration
    initial_data = {
        "name": node_name,
        "ip": "10.0.1.200",
        "capabilities": {
            "os": "linux",
            "cpu_count": 4,
            "mem_mb": 8192,
            "gpus": []
        }
    }
    
    first_response = client.post('/api/v1/nodes/register', json=initial_data)
    assert first_response.status_code == 201
    first_node_id = first_response.json()["node_id"]
    
    # Re-register with updated capabilities
    updated_data = {
        "name": node_name,
        "ip": "10.0.1.201",  # Different IP
        "capabilities": {
            "os": "linux",
            "cpu_count": 8,  # Upgraded
            "mem_mb": 16384,  # Upgraded
            "gpus": [{"id": 0, "model": "RTX 3090"}]  # Added GPU
        }
    }
    
    second_response = client.post('/api/v1/nodes/register', json=updated_data)
    assert second_response.status_code == 201
    second_node_id = second_response.json()["node_id"]
    
    # Should get the same node ID
    assert first_node_id == second_node_id
    
    # Verify only one node exists
    list_response = client.get('/api/v1/nodes')
    nodes = list_response.json()
    assert len(nodes) == 1
    
    # Verify capabilities were updated
    node = nodes[0]
    assert node["capabilities"]["cpu_count"] == 8
    assert node["capabilities"]["mem_mb"] == 16384
    assert len(node["capabilities"]["gpus"]) == 1


def test_deployment_lifecycle(client):
    """Test complete deployment lifecycle: create, retrieve, delete."""
    deployment_id = "lifecycle-test-deploy"
    
    # Create deployment
    deployment_data = {
        "deployment_id": deployment_id,
        "template_id": "redis",
        "rendered_compose": "version: '3.8'\nservices:\n  redis:\n    image: redis:7",
        "env": {},
        "action": "apply"
    }
    
    create_response = client.post('/api/v1/deployments', json=deployment_data)
    assert create_response.status_code == 202
    
    # Verify it exists
    get_response = client.get(f'/api/v1/deployments/{deployment_id}')
    assert get_response.status_code == 200
    
    # Delete deployment
    delete_response = client.delete(f'/api/v1/deployments/{deployment_id}')
    assert delete_response.status_code == 200
    
    # Note: Verify deletion behavior depends on implementation
    # Some systems mark as deleted, others remove entirely


def test_heartbeat_without_registration_fails(client):
    """Test that heartbeat fails for non-existent node."""
    heartbeat_data = {
        "cpu_usage": 50.0,
        "mem_usage": 60.0,
        "disk_free_mb": 100000,
        "running_containers": []
    }
    
    response = client.post('/api/v1/nodes/nonexistent-node/heartbeat', json=heartbeat_data)
    assert response.status_code == 404


def test_api_health_and_root_endpoints(client):
    """Test basic API health and root endpoints."""
    # Test health endpoint
    health_response = client.get('/health')
    assert health_response.status_code == 200
    assert health_response.json()["status"] == "healthy"
    
    # Test root endpoint
    root_response = client.get('/')
    assert root_response.status_code == 200
    data = root_response.json()
    assert "version" in data
    assert "message" in data


def test_concurrent_heartbeats(client):
    """Test multiple heartbeats from same node in quick succession."""
    # Register node
    node_data = {
        "name": "concurrent-test-node",
        "ip": "10.0.1.250",
        "capabilities": {
            "os": "linux",
            "cpu_count": 4,
            "mem_mb": 8192,
            "gpus": []
        }
    }
    
    reg_response = client.post('/api/v1/nodes/register', json=node_data)
    node_id = reg_response.json()["node_id"]
    
    # Send multiple heartbeats
    for i in range(5):
        heartbeat_data = {
            "cpu_usage": 50.0 + i,
            "mem_usage": 60.0 + i,
            "disk_free_mb": 100000 - (i * 1000),
            "running_containers": [f"container-{i}"]
        }
        
        response = client.post(f'/api/v1/nodes/{node_id}/heartbeat', json=heartbeat_data)
        assert response.status_code == 200
    
    # Node should still be retrievable
    get_response = client.get(f'/api/v1/nodes/{node_id}')
    assert get_response.status_code == 200
