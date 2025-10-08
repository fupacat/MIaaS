"""
FastAPI Control Plane Entry Point

This module imports the FastAPI application from app.main and makes it
available for uvicorn to run. This allows running the server with:

    uvicorn main:app --reload --host 0.0.0.0 --port 8080

Or from the project root:

    uvicorn control-plane.main:app --reload --host 0.0.0.0 --port 8080
"""
from app.main import app

# Export the app for uvicorn
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
