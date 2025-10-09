"""Unit tests for placement engine."""
import pytest
from app.orchestrator.placement import PlacementEngine


def test_placement_engine_initialization():
    """Test PlacementEngine initializes with correct weights."""
    engine = PlacementEngine()
    
    assert engine.weight_memory == 1.0
    assert engine.weight_disk == 0.5
    assert engine.weight_gpu == 2.0


def test_select_node_with_no_nodes():
    """Test select_node returns None when no nodes available."""
    engine = PlacementEngine()
    nodes = []
    requirements = {}
    
    result = engine.select_node(nodes, requirements)
    
    assert result is None


def test_select_node_single_node():
    """Test select_node with a single suitable node."""
    engine = PlacementEngine()
    nodes = [
        {
            "id": "node-1",
            "name": "worker-01",
            "capabilities": {
                "os": "linux",
                "cpu_count": 8,
                "mem_mb": 16000,
                "disk_mb": 100000,
                "gpus": []
            }
        }
    ]
    requirements = {}
    
    result = engine.select_node(nodes, requirements)
    
    assert result == "node-1"


def test_select_node_multiple_nodes_selects_best():
    """Test select_node selects node with highest score."""
    engine = PlacementEngine()
    nodes = [
        {
            "id": "node-1",
            "capabilities": {
                "mem_mb": 8000,
                "disk_mb": 50000,
                "gpus": []
            }
        },
        {
            "id": "node-2",
            "capabilities": {
                "mem_mb": 16000,  # Higher memory
                "disk_mb": 100000,  # Higher disk
                "gpus": []
            }
        },
        {
            "id": "node-3",
            "capabilities": {
                "mem_mb": 4000,
                "disk_mb": 25000,
                "gpus": []
            }
        }
    ]
    requirements = {}
    
    result = engine.select_node(nodes, requirements)
    
    # node-2 should be selected due to higher resources
    assert result == "node-2"


def test_select_node_with_gpu_requirement():
    """Test select_node filters by GPU requirement."""
    engine = PlacementEngine()
    nodes = [
        {
            "id": "node-1",
            "capabilities": {
                "mem_mb": 16000,
                "disk_mb": 100000,
                "gpus": []
            }
        },
        {
            "id": "node-2",
            "capabilities": {
                "mem_mb": 16000,
                "disk_mb": 100000,
                "gpus": [{"id": 0, "model": "RTX 3090"}]
            }
        }
    ]
    requirements = {"tags": ["gpu"]}
    
    result = engine.select_node(nodes, requirements)
    
    # node-2 should be selected as it has GPU
    assert result == "node-2"


def test_select_node_with_gpu_requirement_no_suitable_node():
    """Test select_node returns None when GPU required but none available."""
    engine = PlacementEngine()
    nodes = [
        {
            "id": "node-1",
            "capabilities": {
                "mem_mb": 16000,
                "disk_mb": 100000,
                "gpus": []
            }
        }
    ]
    requirements = {"tags": ["gpu"]}
    
    result = engine.select_node(nodes, requirements)
    
    assert result is None


def test_meets_requirements_no_tags():
    """Test _meets_requirements with no specific requirements."""
    engine = PlacementEngine()
    node = {
        "id": "node-1",
        "capabilities": {
            "mem_mb": 8000,
            "gpus": []
        }
    }
    requirements = {}
    
    result = engine._meets_requirements(node, requirements)
    
    assert result is True


def test_meets_requirements_gpu_available():
    """Test _meets_requirements when GPU is required and available."""
    engine = PlacementEngine()
    node = {
        "id": "node-1",
        "capabilities": {
            "mem_mb": 8000,
            "gpus": [{"id": 0, "model": "RTX 3090"}]
        }
    }
    requirements = {"tags": ["gpu"]}
    
    result = engine._meets_requirements(node, requirements)
    
    assert result is True


def test_meets_requirements_gpu_not_available():
    """Test _meets_requirements when GPU is required but not available."""
    engine = PlacementEngine()
    node = {
        "id": "node-1",
        "capabilities": {
            "mem_mb": 8000,
            "gpus": []
        }
    }
    requirements = {"tags": ["gpu"]}
    
    result = engine._meets_requirements(node, requirements)
    
    assert result is False


def test_score_node_basic():
    """Test _score_node calculates correct score."""
    engine = PlacementEngine()
    node = {
        "id": "node-1",
        "capabilities": {
            "mem_mb": 10000,
            "disk_mb": 20000,
            "gpus": []
        }
    }
    requirements = {}
    
    score = engine._score_node(node, requirements)
    
    # score = 10000 * 1.0 + 20000 * 0.5 + 0 = 20000
    expected_score = 10000 * 1.0 + 20000 * 0.5
    assert score == expected_score


def test_score_node_with_gpu():
    """Test _score_node includes GPU bonus."""
    engine = PlacementEngine()
    node = {
        "id": "node-1",
        "capabilities": {
            "mem_mb": 10000,
            "disk_mb": 20000,
            "gpus": [{"id": 0, "model": "RTX 3090"}]
        }
    }
    requirements = {}
    
    score = engine._score_node(node, requirements)
    
    # score = 10000 * 1.0 + 20000 * 0.5 + 1 * 2.0 = 20002
    expected_score = 10000 * 1.0 + 20000 * 0.5 + 1 * 2.0
    assert score == expected_score


def test_score_node_with_multiple_gpus():
    """Test _score_node calculates GPU bonus for multiple GPUs."""
    engine = PlacementEngine()
    node = {
        "id": "node-1",
        "capabilities": {
            "mem_mb": 10000,
            "disk_mb": 20000,
            "gpus": [
                {"id": 0, "model": "RTX 3090"},
                {"id": 1, "model": "RTX 3090"}
            ]
        }
    }
    requirements = {}
    
    score = engine._score_node(node, requirements)
    
    # score = 10000 * 1.0 + 20000 * 0.5 + 2 * 2.0 = 20004
    expected_score = 10000 * 1.0 + 20000 * 0.5 + 2 * 2.0
    assert score == expected_score


def test_score_node_missing_capabilities():
    """Test _score_node handles missing capability fields."""
    engine = PlacementEngine()
    node = {
        "id": "node-1",
        "capabilities": {}
    }
    requirements = {}
    
    score = engine._score_node(node, requirements)
    
    # With no capabilities, score should be 0
    assert score == 0.0


def test_select_node_gpu_bonus_affects_selection():
    """Test that GPU bonus affects node selection."""
    engine = PlacementEngine()
    nodes = [
        {
            "id": "node-1",
            "capabilities": {
                "mem_mb": 20000,  # Higher memory
                "disk_mb": 100000,
                "gpus": []
            }
        },
        {
            "id": "node-2",
            "capabilities": {
                "mem_mb": 16000,
                "disk_mb": 100000,
                "gpus": [{"id": 0, "model": "RTX 3090"}]
            }
        }
    ]
    requirements = {}
    
    result = engine.select_node(nodes, requirements)
    
    # Calculate expected scores:
    # node-1: 20000 * 1.0 + 100000 * 0.5 = 70000
    # node-2: 16000 * 1.0 + 100000 * 0.5 + 1 * 2.0 = 66002
    # node-1 should be selected with higher score
    assert result == "node-1"
