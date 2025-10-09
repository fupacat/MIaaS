"""Tests for seed_data.py script."""
import pytest
from sqlalchemy.orm import Session

from app.db.models import NodeDB
from seed_data import seed_test_nodes, clear_test_data


def test_seed_test_nodes(setup_database):
    """Test that seed_test_nodes creates nodes correctly."""
    from tests.conftest import TestingSessionLocal
    
    db = TestingSessionLocal()
    try:
        # Seed the nodes
        node_ids = seed_test_nodes(db)
        
        # Verify correct number of nodes
        assert len(node_ids) == 3
        assert "test-node-1" in node_ids
        assert "test-node-2" in node_ids
        assert "gpu-worker-1" in node_ids
        
        # Verify nodes exist in database
        nodes = db.query(NodeDB).all()
        assert len(nodes) == 3
        
        # Verify node details
        node1 = db.query(NodeDB).filter(NodeDB.id == "test-node-1").first()
        assert node1 is not None
        assert node1.name == "test-node-1"
        assert node1.ip == "192.168.1.100"
        assert node1.status == "online"
        assert node1.capabilities["os"] == "linux"
        assert node1.capabilities["cpu_count"] == 8
        assert len(node1.capabilities["gpus"]) == 1
        assert node1.capabilities["gpus"][0]["model"] == "NVIDIA RTX 3090"
        
        # Verify node with K8s capabilities
        node2 = db.query(NodeDB).filter(NodeDB.id == "test-node-2").first()
        assert node2 is not None
        assert node2.capabilities["k8s"]["version"] == "1.28.0"
    finally:
        db.close()


def test_seed_test_nodes_idempotent(setup_database):
    """Test that seeding is idempotent (can be run multiple times)."""
    from tests.conftest import TestingSessionLocal
    
    db = TestingSessionLocal()
    try:
        # Seed once
        seed_test_nodes(db)
        nodes_count_1 = db.query(NodeDB).count()
        
        # Seed again
        seed_test_nodes(db)
        nodes_count_2 = db.query(NodeDB).count()
        
        # Should still have same number of nodes
        assert nodes_count_1 == nodes_count_2 == 3
        
        # Verify no duplicates
        node_ids = [node.id for node in db.query(NodeDB).all()]
        assert len(node_ids) == len(set(node_ids))  # All unique
    finally:
        db.close()


def test_clear_test_data(setup_database):
    """Test that clear_test_data removes all nodes."""
    from tests.conftest import TestingSessionLocal
    
    db = TestingSessionLocal()
    try:
        # Seed some nodes
        seed_test_nodes(db)
        assert db.query(NodeDB).count() == 3
        
        # Clear data
        clear_test_data(db)
        
        # Verify all nodes removed
        assert db.query(NodeDB).count() == 0
    finally:
        db.close()


def test_seeded_node_capabilities_schema(setup_database):
    """Test that seeded nodes have proper capabilities schema."""
    from tests.conftest import TestingSessionLocal
    
    db = TestingSessionLocal()
    try:
        seed_test_nodes(db)
        
        # Check all nodes have required capability fields
        nodes = db.query(NodeDB).all()
        for node in nodes:
            caps = node.capabilities
            
            # Required fields
            assert "os" in caps
            assert "cpu_count" in caps
            assert "mem_mb" in caps
            assert "disk_mb" in caps
            assert "gpus" in caps
            assert "docker" in caps
            
            # Verify types
            assert isinstance(caps["os"], str)
            assert isinstance(caps["cpu_count"], int)
            assert isinstance(caps["mem_mb"], int)
            assert isinstance(caps["disk_mb"], int)
            assert isinstance(caps["gpus"], list)
            assert isinstance(caps["docker"], dict)
            
            # Docker should have required fields
            assert "version" in caps["docker"]
            assert "available" in caps["docker"]
    finally:
        db.close()
