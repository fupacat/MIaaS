"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.db.models import NodeDB, DeploymentDB  # Import to register models


# Use in-memory database with shared connection for tests
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables once
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Clear tables before each test."""
    # Clear all data between tests
    db = TestingSessionLocal()
    try:
        # Delete all records from tables
        db.query(DeploymentDB).delete()
        db.query(NodeDB).delete()
        db.commit()
    finally:
        db.close()
    yield


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)
