"""Tests for Node model."""
import pytest
from datetime import datetime
from app.models import Node


def test_node_creation():
    """Test creating a Node instance."""
    node = Node(
        node_id="test-node-1",
        hostname="test-host",
        capabilities=["docker", "compose"],
        status="active"
    )
    
    assert node.id == "test-node-1"
    assert node.hostname == "test-host"
    assert node.capabilities == ["docker", "compose"]
    assert node.status == "active"
    assert isinstance(node.last_heartbeat, datetime)


def test_node_to_dict():
    """Test converting Node to dictionary."""
    node = Node(
        node_id="test-node-1",
        hostname="test-host",
        capabilities=["docker"],
        status="active"
    )
    
    node_dict = node.to_dict()
    
    assert node_dict["id"] == "test-node-1"
    assert node_dict["hostname"] == "test-host"
    assert node_dict["capabilities"] == ["docker"]
    assert node_dict["status"] == "active"
    assert "last_heartbeat" in node_dict


def test_node_from_dict():
    """Test creating Node from dictionary."""
    data = {
        "id": "test-node-1",
        "hostname": "test-host",
        "capabilities": ["docker", "compose"],
        "status": "active"
    }
    
    node = Node.from_dict(data)
    
    assert node.id == "test-node-1"
    assert node.hostname == "test-host"
    assert node.capabilities == ["docker", "compose"]
    assert node.status == "active"


def test_node_update_heartbeat():
    """Test updating node heartbeat."""
    node = Node(
        node_id="test-node-1",
        hostname="test-host"
    )
    
    original_heartbeat = node.last_heartbeat
    node.update_heartbeat()
    
    assert node.last_heartbeat >= original_heartbeat


def test_node_default_values():
    """Test Node default values."""
    node = Node(
        node_id="test-node-1",
        hostname="test-host"
    )
    
    assert node.capabilities == []
    assert node.status == "active"
    assert isinstance(node.last_heartbeat, datetime)
