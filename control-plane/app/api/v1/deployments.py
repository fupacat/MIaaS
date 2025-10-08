"""Deployment management API endpoints.

This module provides REST API endpoints for managing deployments,
including creating, listing, and deleting deployments.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.models import DeploymentRequest, DeploymentResponse
from app.db import get_db, DeploymentDB, NodeDB

router = APIRouter(prefix="/deployments", tags=["deployments"])


@router.post("", response_model=DeploymentResponse, status_code=202)
def create_deployment(
    request: DeploymentRequest,
    db: Session = Depends(get_db),
) -> DeploymentResponse:
    """Create a new deployment.
    
    This endpoint creates a deployment request that will be sent to the
    specified node agent for execution. The deployment is stored in the
    database with a pending status.
    
    Args:
        request: Deployment request with template and configuration
        db: Database session
        
    Returns:
        DeploymentResponse with deployment status
        
    Raises:
        HTTPException: 400 if deployment data is invalid
        
    Example:
        POST /api/v1/deployments
        {
            "deployment_id": "deploy-123",
            "template_id": "postgres",
            "rendered_compose": "version: '3.8'\\nservices:...",
            "env": {"POSTGRES_PASSWORD": "secret"},
            "action": "apply"
        }
    """
    # Validate deployment_id is unique
    existing = db.query(DeploymentDB).filter(
        DeploymentDB.id == request.deployment_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Deployment with ID {request.deployment_id} already exists"
        )
    
    # For MVP, we'll accept any deployment without node assignment
    # In production, this would use the orchestrator to select a node
    deployment = DeploymentDB(
        id=request.deployment_id,
        node_id="unassigned",  # Stub: would use orchestrator
        template_id=request.template_id,
        rendered_compose=request.rendered_compose,
        env=request.env,
        status="pending",
        action=request.action,
    )
    
    db.add(deployment)
    db.commit()
    
    return DeploymentResponse(
        deployment_id=deployment.id,
        status="accepted",
        message="Deployment request accepted and queued for processing",
    )


@router.get("", response_model=List[DeploymentResponse])
def list_deployments(db: Session = Depends(get_db)) -> List[DeploymentResponse]:
    """List all deployments.
    
    Returns a list of all deployments with their current status.
    
    Args:
        db: Database session
        
    Returns:
        List of DeploymentResponse objects
        
    Example:
        GET /api/v1/deployments
    """
    deployments = db.query(DeploymentDB).all()
    return [
        DeploymentResponse(
            deployment_id=d.id,
            status=d.status,
            message=f"Deployment on node {d.node_id}",
        )
        for d in deployments
    ]


@router.get("/{deployment_id}", response_model=DeploymentResponse)
def get_deployment(
    deployment_id: str,
    db: Session = Depends(get_db),
) -> DeploymentResponse:
    """Get a specific deployment by ID.
    
    Args:
        deployment_id: ID of the deployment to retrieve
        db: Database session
        
    Returns:
        DeploymentResponse with deployment details
        
    Raises:
        HTTPException: 404 if deployment not found
        
    Example:
        GET /api/v1/deployments/{deployment_id}
    """
    deployment = db.query(DeploymentDB).filter(
        DeploymentDB.id == deployment_id
    ).first()
    
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    return DeploymentResponse(
        deployment_id=deployment.id,
        status=deployment.status,
        message=f"Deployment '{deployment.template_id}' on node {deployment.node_id}",
    )


@router.delete("/{deployment_id}", response_model=DeploymentResponse)
def delete_deployment(
    deployment_id: str,
    db: Session = Depends(get_db),
) -> DeploymentResponse:
    """Delete a deployment.
    
    This endpoint marks a deployment for deletion. The agent will
    tear down the associated resources.
    
    Args:
        deployment_id: ID of the deployment to delete
        db: Database session
        
    Returns:
        DeploymentResponse with deletion status
        
    Raises:
        HTTPException: 404 if deployment not found
        
    Example:
        DELETE /api/v1/deployments/{deployment_id}
    """
    deployment = db.query(DeploymentDB).filter(
        DeploymentDB.id == deployment_id
    ).first()
    
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    # Mark for deletion instead of removing immediately
    deployment.status = "deleting"
    deployment.action = "remove"
    db.commit()
    
    return DeploymentResponse(
        deployment_id=deployment.id,
        status="deleting",
        message="Deployment marked for deletion",
    )
