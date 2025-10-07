"""Tests for deployment endpoints."""


def test_create_deployment(client):
    """Test creating a new deployment."""
    deployment_data = {
        "deployment_id": "deploy-123",
        "template_id": "postgres",
        "rendered_compose": "version: '3.8'\nservices:\n  postgres:\n    image: postgres:16",
        "env": {"POSTGRES_PASSWORD": "secret123"},
        "action": "apply"
    }
    
    response = client.post('/api/v1/deployments', json=deployment_data)
    
    assert response.status_code == 202
    data = response.json()
    assert data['deployment_id'] == 'deploy-123'
    assert data['status'] == 'accepted'


def test_create_duplicate_deployment(client):
    """Test creating a deployment with duplicate ID."""
    deployment_data = {
        "deployment_id": "deploy-123",
        "template_id": "postgres",
        "rendered_compose": "version: '3.8'\nservices:\n  postgres:\n    image: postgres:16",
        "env": {},
        "action": "apply"
    }
    
    # Create first deployment
    client.post('/api/v1/deployments', json=deployment_data)
    
    # Try to create duplicate
    response = client.post('/api/v1/deployments', json=deployment_data)
    
    assert response.status_code == 400


def test_list_deployments_empty(client):
    """Test listing deployments when none exist."""
    response = client.get('/api/v1/deployments')
    
    assert response.status_code == 200
    assert response.json() == []


def test_list_deployments(client):
    """Test listing deployments."""
    # Create two deployments
    deployment1 = {
        "deployment_id": "deploy-1",
        "template_id": "postgres",
        "rendered_compose": "version: '3.8'",
        "env": {},
        "action": "apply"
    }
    deployment2 = {
        "deployment_id": "deploy-2",
        "template_id": "redis",
        "rendered_compose": "version: '3.8'",
        "env": {},
        "action": "apply"
    }
    
    client.post('/api/v1/deployments', json=deployment1)
    client.post('/api/v1/deployments', json=deployment2)
    
    response = client.get('/api/v1/deployments')
    
    assert response.status_code == 200
    deployments = response.json()
    assert len(deployments) == 2


def test_get_deployment(client):
    """Test getting a specific deployment."""
    deployment_data = {
        "deployment_id": "deploy-123",
        "template_id": "postgres",
        "rendered_compose": "version: '3.8'",
        "env": {},
        "action": "apply"
    }
    
    client.post('/api/v1/deployments', json=deployment_data)
    
    response = client.get('/api/v1/deployments/deploy-123')
    
    assert response.status_code == 200
    data = response.json()
    assert data['deployment_id'] == 'deploy-123'


def test_get_deployment_not_found(client):
    """Test getting a non-existent deployment."""
    response = client.get('/api/v1/deployments/non-existent')
    
    assert response.status_code == 404


def test_delete_deployment(client):
    """Test deleting a deployment."""
    deployment_data = {
        "deployment_id": "deploy-123",
        "template_id": "postgres",
        "rendered_compose": "version: '3.8'",
        "env": {},
        "action": "apply"
    }
    
    client.post('/api/v1/deployments', json=deployment_data)
    
    response = client.delete('/api/v1/deployments/deploy-123')
    
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'deleting'


def test_delete_deployment_not_found(client):
    """Test deleting a non-existent deployment."""
    response = client.delete('/api/v1/deployments/non-existent')
    
    assert response.status_code == 404
