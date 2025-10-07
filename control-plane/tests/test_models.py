"""Tests for Pydantic models."""
import pytest
from pydantic import ValidationError
from app.models import (
    CapabilitiesModel,
    NodeRegisterRequest,
    NodeResponse,
    HeartbeatRequest,
    DeploymentRequest,
)


def test_capabilities_model():
    """Test CapabilitiesModel validation."""
    caps = CapabilitiesModel(
        os="linux",
        cpu_count=8,
        mem_mb=16000,
        gpus=[]
    )
    
    assert caps.os == "linux"
    assert caps.cpu_count == 8
    assert caps.mem_mb == 16000
    assert caps.gpus == []


def test_capabilities_model_missing_required():
    """Test CapabilitiesModel with missing required fields."""
    with pytest.raises(ValidationError):
        CapabilitiesModel(
            os="linux",
            cpu_count=8
            # Missing mem_mb
        )


def test_node_register_request():
    """Test NodeRegisterRequest validation."""
    request = NodeRegisterRequest(
        name="worker-01",
        ip="192.168.1.10",
        capabilities=CapabilitiesModel(
            os="linux",
            cpu_count=8,
            mem_mb=16000,
            gpus=[]
        )
    )
    
    assert request.name == "worker-01"
    assert request.ip == "192.168.1.10"
    assert request.capabilities.os == "linux"


def test_node_response():
    """Test NodeResponse model."""
    response = NodeResponse(
        id="node-123",
        name="worker-01",
        ip="192.168.1.10",
        capabilities={"os": "linux", "cpu_count": 8},
        last_seen=1234567890.0,
        status="online"
    )
    
    assert response.id == "node-123"
    assert response.name == "worker-01"
    assert response.status == "online"


def test_heartbeat_request():
    """Test HeartbeatRequest with default values."""
    heartbeat = HeartbeatRequest()
    
    assert heartbeat.cpu_usage == 0.0
    assert heartbeat.mem_usage == 0.0
    assert heartbeat.disk_free_mb == 0
    assert heartbeat.running_containers == []


def test_heartbeat_request_with_values():
    """Test HeartbeatRequest with provided values."""
    heartbeat = HeartbeatRequest(
        cpu_usage=45.5,
        mem_usage=60.2,
        disk_free_mb=50000,
        running_containers=["postgres", "redis"]
    )
    
    assert heartbeat.cpu_usage == 45.5
    assert heartbeat.mem_usage == 60.2
    assert heartbeat.disk_free_mb == 50000
    assert len(heartbeat.running_containers) == 2


def test_deployment_request():
    """Test DeploymentRequest validation."""
    deployment = DeploymentRequest(
        deployment_id="deploy-123",
        template_id="postgres",
        rendered_compose="version: '3.8'\nservices:...",
        env={"POSTGRES_PASSWORD": "secret"},
        action="apply"
    )
    
    assert deployment.deployment_id == "deploy-123"
    assert deployment.template_id == "postgres"
    assert deployment.action == "apply"
    assert deployment.env["POSTGRES_PASSWORD"] == "secret"


def test_deployment_request_missing_fields():
    """Test DeploymentRequest with missing required fields."""
    with pytest.raises(ValidationError):
        DeploymentRequest(
            deployment_id="deploy-123",
            template_id="postgres"
            # Missing required fields
        )
