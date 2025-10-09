"""FastAPI dependencies for authentication.

This module provides dependency injection functions for protecting API endpoints
that require node authentication.
"""
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from .jwt_utils import verify_node_token

security = HTTPBearer(auto_error=False)


def require_node_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> str:
    """Require valid node authentication for an endpoint.
    
    This dependency extracts and validates the JWT token from the Authorization
    header. Returns the node_id if valid, or raises HTTPException if not.
    
    Args:
        credentials: HTTP Bearer credentials from the Authorization header
        
    Returns:
        Node ID from the validated token
        
    Raises:
        HTTPException: 401 if token is missing, invalid, or expired
        
    Example:
        @app.get("/protected")
        def protected_endpoint(node_id: str = Depends(require_node_auth)):
            return {"message": f"Authenticated as {node_id}"}
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    payload = verify_node_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload["node_id"]
