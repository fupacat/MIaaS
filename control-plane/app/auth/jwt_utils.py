"""JWT token utilities for node authentication.

This module provides functions to create and verify JWT tokens for node agents.
Tokens are node-specific with configurable TTL and support rotation.
"""
import os
import jwt
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

# JWT configuration - can be overridden via environment variables
JWT_SECRET = os.environ.get("JWT_SECRET", "development-secret-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = int(os.environ.get("JWT_EXPIRATION_HOURS", "24"))


def create_node_token(node_id: str, node_name: str) -> str:
    """Create a JWT token for a node agent.
    
    The token includes the node ID, node name, issued time, and expiration time.
    Tokens are signed with the JWT_SECRET and use HS256 algorithm.
    
    Args:
        node_id: Unique identifier for the node
        node_name: Human-readable name of the node
        
    Returns:
        JWT token string
        
    Example:
        >>> token = create_node_token("node-123", "worker-01")
        >>> print(token)
        eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """
    now = datetime.utcnow()
    expiration = now + timedelta(hours=JWT_EXPIRATION_HOURS)
    
    payload = {
        "node_id": node_id,
        "node_name": node_name,
        "iat": int(now.timestamp()),
        "exp": int(expiration.timestamp()),
        "type": "node_agent",
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_node_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode a node JWT token.
    
    Validates the token signature and expiration time. Returns the decoded
    payload if valid, or None if invalid/expired.
    
    Args:
        token: JWT token string to verify
        
    Returns:
        Dictionary with token payload if valid, None otherwise
        
    Example:
        >>> payload = verify_node_token(token)
        >>> if payload:
        ...     print(f"Node: {payload['node_id']}")
    """
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )
        
        # Verify this is a node agent token
        if payload.get("type") != "node_agent":
            return None
            
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Invalid token
        return None


def get_current_node(token: str) -> Optional[str]:
    """Extract node ID from a JWT token.
    
    Convenience function to get just the node_id from a token.
    
    Args:
        token: JWT token string
        
    Returns:
        Node ID if token is valid, None otherwise
        
    Example:
        >>> node_id = get_current_node(token)
        >>> if node_id:
        ...     print(f"Authenticated as node: {node_id}")
    """
    payload = verify_node_token(token)
    if payload:
        return payload.get("node_id")
    return None
