"""Node management API endpoints.

This module provides REST API endpoints for node registration, listing,
status updates, and heartbeat management.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import uuid
import time

from app.models import (
    NodeRegisterRequest,
    NodeRegisterResponse,
    NodeResponse,
    HeartbeatRequest,
    HeartbeatResponse,
)
from app.db import get_db, NodeDB
from app.auth import create_node_token, require_node_auth

router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.post("/register", response_model=NodeRegisterResponse, status_code=201)
def register_node(
    request: NodeRegisterRequest,
    db: Session = Depends(get_db),
) -> NodeRegisterResponse:
    """Register a new node or update an existing node.
    
    This endpoint allows agent nodes to register with the control plane,
    providing their capabilities and connection information. If a node with
    the same name already exists, it will be updated.
    
    Args:
        request: Node registration request with name, ip, and capabilities
        db: Database session
        
    Returns:
        NodeRegisterResponse with assigned node_id, token, and control plane URL
        
    Example:
        POST /api/v1/nodes/register
        {
            "name": "worker-01",
            "ip": "192.168.1.10",
            "capabilities": {
                "os": "linux",
                "cpu_count": 8,
                "mem_mb": 32000,
                "gpus": []
            }
        }
    """
    # Check if node with same name exists
    existing_node = db.query(NodeDB).filter(NodeDB.name == request.name).first()
    
    if existing_node:
        # Update existing node
        existing_node.ip = request.ip
        existing_node.capabilities = request.capabilities.model_dump()
        existing_node.last_seen = time.time()
        existing_node.status = "online"
        db.commit()
        node_id = existing_node.id
    else:
        # Create new node
        node_id = str(uuid.uuid4())
        node = NodeDB(
            id=node_id,
            name=request.name,
            ip=request.ip,
            capabilities=request.capabilities.model_dump(),
            last_seen=time.time(),
            status="online",
        )
        db.add(node)
        db.commit()
    
    # Generate JWT token for the node
    jwt_token = create_node_token(node_id, request.name)
    
    return NodeRegisterResponse(
        node_id=node_id,
        node_token=jwt_token,
        control_plane_url="http://localhost:8080",
    )


@router.get("", response_model=List[NodeResponse])
def list_nodes(db: Session = Depends(get_db)) -> List[NodeResponse]:
    """List all registered nodes.
    
    Returns a list of all nodes registered with the control plane,
    including their current status and capabilities.
    
    Args:
        db: Database session
        
    Returns:
        List of NodeResponse objects
        
    Example:
        GET /api/v1/nodes
    """
    nodes = db.query(NodeDB).all()
    return [
        NodeResponse(
            id=node.id,
            name=node.name,
            ip=node.ip,
            capabilities=node.capabilities,
            last_seen=node.last_seen,
            status=node.status,
        )
        for node in nodes
    ]


@router.get("/{node_id}", response_model=NodeResponse)
def get_node(node_id: str, db: Session = Depends(get_db)) -> NodeResponse:
    """Get a specific node by ID.
    
    Args:
        node_id: ID of the node to retrieve
        db: Database session
        
    Returns:
        NodeResponse with node details
        
    Raises:
        HTTPException: 404 if node not found
        
    Example:
        GET /api/v1/nodes/{node_id}
    """
    node = db.query(NodeDB).filter(NodeDB.id == node_id).first()
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    return NodeResponse(
        id=node.id,
        name=node.name,
        ip=node.ip,
        capabilities=node.capabilities,
        last_seen=node.last_seen,
        status=node.status,
    )


@router.post("/{node_id}/heartbeat", response_model=HeartbeatResponse)
def heartbeat(
    node_id: str,
    request: HeartbeatRequest,
    db: Session = Depends(get_db),
    authenticated_node_id: str = Depends(require_node_auth),
) -> HeartbeatResponse:
    """Update node heartbeat and metrics.
    
    This endpoint receives periodic heartbeat updates from agent nodes,
    updating their status and resource metrics.
    
    Args:
        node_id: ID of the node sending heartbeat
        request: Heartbeat data with resource metrics
        db: Database session
        
    Returns:
        HeartbeatResponse with status confirmation
        
    Raises:
        HTTPException: 404 if node not found
        
    Example:
        POST /api/v1/nodes/{node_id}/heartbeat
        {
            "cpu_usage": 45.5,
            "mem_usage": 60.2,
            "disk_free_mb": 50000,
            "running_containers": ["postgres", "redis"]
        }
    """
    # Verify the authenticated node matches the request
    if authenticated_node_id != node_id:
        raise HTTPException(
            status_code=403,
            detail="Cannot send heartbeat for a different node"
        )
    
    node = db.query(NodeDB).filter(NodeDB.id == node_id).first()
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # Update node status
    node.last_seen = time.time()
    node.status = "online"
    
    # Store metrics in capabilities (for MVP)
    if not isinstance(node.capabilities, dict):
        node.capabilities = {}
    node.capabilities["metrics"] = request.model_dump()
    
    db.commit()
    
    return HeartbeatResponse(
        status="ok",
        timestamp=time.time(),
    )
