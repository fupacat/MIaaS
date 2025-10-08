"""SQLAlchemy database models."""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, JSON
from .database import Base


class NodeDB(Base):
    """Database model for nodes."""
    
    __tablename__ = "nodes"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    capabilities = Column(JSON, nullable=False)
    last_seen = Column(Float, nullable=False)
    status = Column(String, default="online")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DeploymentDB(Base):
    """Database model for deployments."""
    
    __tablename__ = "deployments"
    
    id = Column(String, primary_key=True, index=True)
    node_id = Column(String, nullable=False, index=True)
    template_id = Column(String, nullable=False)
    rendered_compose = Column(Text, nullable=False)
    env = Column(JSON, default={})
    status = Column(String, default="pending")
    action = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
