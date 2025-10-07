"""FastAPI application entry point for MIaaS Control Plane.

This module initializes the FastAPI application, sets up middleware,
includes API routers, and provides health check endpoints.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import nodes, deployments
from app.db import init_db

app = FastAPI(
    title="MIaaS Control Plane",
    version="0.1.0",
    description="Model Infrastructure as a Service - Control Plane API",
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(nodes.router, prefix="/api/v1")
app.include_router(deployments.router, prefix="/api/v1")


@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/")
def root():
    """Root endpoint with API information.
    
    Returns:
        Basic API information and version
    """
    return {
        "message": "MIaaS Control Plane API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint.
    
    Returns:
        Health status of the control plane
    """
    return {"status": "healthy"}
