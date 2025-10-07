"""Pydantic models for API requests and responses."""
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class CapabilitiesModel(BaseModel):
    """Node capabilities model."""
    os: str = Field(..., description="Operating system")
    cpu_count: int = Field(..., description="Number of CPU cores")
    mem_mb: int = Field(..., description="Total memory in MB")
    disk_mb: Optional[int] = Field(None, description="Total disk space in MB")
    gpus: List[Dict] = Field(default_factory=list, description="List of available GPUs")
    docker: Optional[Dict] = Field(None, description="Docker information")
    k8s: Optional[Dict] = Field(None, description="Kubernetes information")


class NodeRegisterRequest(BaseModel):
    """Request model for node registration."""
    name: str = Field(..., description="Node name")
    ip: str = Field(..., description="Node IP address")
    capabilities: CapabilitiesModel = Field(..., description="Node capabilities")


class NodeResponse(BaseModel):
    """Response model for node information."""
    id: str = Field(..., description="Node ID")
    name: str = Field(..., description="Node name")
    ip: str = Field(..., description="Node IP address")
    capabilities: Dict = Field(..., description="Node capabilities")
    last_seen: float = Field(..., description="Last seen timestamp")
    status: str = Field(..., description="Node status")


class NodeRegisterResponse(BaseModel):
    """Response model for node registration."""
    node_id: str = Field(..., description="Assigned node ID")
    node_token: str = Field(..., description="Node authentication token")
    control_plane_url: str = Field(..., description="Control plane URL")


class HeartbeatRequest(BaseModel):
    """Request model for node heartbeat."""
    cpu_usage: float = Field(0.0, description="CPU usage percentage")
    mem_usage: float = Field(0.0, description="Memory usage percentage")
    disk_free_mb: int = Field(0, description="Free disk space in MB")
    running_containers: List[str] = Field(default_factory=list, description="List of running containers")


class HeartbeatResponse(BaseModel):
    """Response model for heartbeat."""
    status: str = Field(..., description="Response status")
    timestamp: float = Field(..., description="Server timestamp")


class DeploymentRequest(BaseModel):
    """Request model for deployment."""
    deployment_id: str = Field(..., description="Deployment ID")
    template_id: str = Field(..., description="Template ID")
    rendered_compose: str = Field(..., description="Rendered docker-compose YAML")
    env: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    action: str = Field(..., description="Action to perform: apply or remove")


class DeploymentResponse(BaseModel):
    """Response model for deployment."""
    deployment_id: str = Field(..., description="Deployment ID")
    status: str = Field(..., description="Deployment status")
    message: str = Field(..., description="Status message")
