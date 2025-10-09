#!/usr/bin/env python3
"""Seed test data into the control-plane database.

This script populates the database with sample nodes for testing and development.
Can be run standalone or imported for use in tests.
"""
import sys
import time
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import NodeDB


def seed_test_nodes(db: Session):
    """Seed test nodes into the database.
    
    Args:
        db: Database session
        
    Returns:
        List of created node IDs
    """
    test_nodes = [
        {
            "id": "test-node-1",
            "name": "test-node-1",
            "ip": "192.168.1.100",
            "capabilities": {
                "os": "linux",
                "cpu_count": 8,
                "mem_mb": 16000,
                "disk_mb": 500000,
                "gpus": [{"id": 0, "model": "NVIDIA RTX 3090", "mem_mb": 24000}],
                "docker": {"version": "24.0.0", "available": True}
            },
            "last_seen": time.time(),
            "status": "online"
        },
        {
            "id": "test-node-2",
            "name": "test-node-2",
            "ip": "192.168.1.101",
            "capabilities": {
                "os": "linux",
                "cpu_count": 16,
                "mem_mb": 32000,
                "disk_mb": 1000000,
                "gpus": [{"id": 0, "model": "NVIDIA A100", "mem_mb": 80000}],
                "docker": {"version": "24.0.0", "available": True},
                "k8s": {"version": "1.28.0", "available": True}
            },
            "last_seen": time.time(),
            "status": "online"
        },
        {
            "id": "gpu-worker-1",
            "name": "gpu-worker-1",
            "ip": "192.168.1.102",
            "capabilities": {
                "os": "linux",
                "cpu_count": 24,
                "mem_mb": 64000,
                "disk_mb": 2000000,
                "gpus": [{"id": 0, "model": "NVIDIA H100", "mem_mb": 80000}],
                "docker": {"version": "24.0.0", "available": True},
                "k8s": {"version": "1.28.0", "available": True}
            },
            "last_seen": time.time(),
            "status": "online"
        }
    ]
    
    created_ids = []
    for node_data in test_nodes:
        # Check if node already exists
        existing_node = db.query(NodeDB).filter(NodeDB.id == node_data["id"]).first()
        if existing_node:
            print(f"Node {node_data['id']} already exists, updating...")
            for key, value in node_data.items():
                setattr(existing_node, key, value)
        else:
            print(f"Creating node {node_data['id']}...")
            node = NodeDB(**node_data)
            db.add(node)
        
        created_ids.append(node_data["id"])
    
    db.commit()
    print(f"Successfully seeded {len(created_ids)} nodes")
    return created_ids


def clear_test_data(db: Session):
    """Clear all test data from the database.
    
    Args:
        db: Database session
    """
    print("Clearing test data...")
    db.query(NodeDB).delete()
    db.commit()
    print("Test data cleared")


def main():
    """Main function to seed test data."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Seed test data into control-plane database")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing test data before seeding"
    )
    args = parser.parse_args()
    
    db = SessionLocal()
    try:
        if args.clear:
            clear_test_data(db)
        
        node_ids = seed_test_nodes(db)
        print(f"\nSeeded nodes: {', '.join(node_ids)}")
        print("\nYou can now query the API:")
        print("  curl http://localhost:8000/api/v1/nodes")
        return 0
    except Exception as e:
        print(f"Error seeding data: {e}", file=sys.stderr)
        db.rollback()
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
