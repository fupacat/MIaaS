# Control Plane Tests

This directory contains automated tests for the MIaaS control plane.

## Test Files

### `test_models.py`
**Type:** Unit Tests  
**Coverage:** Pydantic data models

Tests validation, serialization, and model structure for:
- `CapabilitiesModel` - Node capability information
- `NodeRegisterRequest` - Node registration payload
- `NodeResponse` - Node information response
- `HeartbeatRequest` - Node heartbeat data
- `DeploymentRequest` - Deployment configuration

### `test_api.py`
**Type:** Integration Tests  
**Coverage:** Node management API endpoints

Tests FastAPI endpoints for:
- Health check (`/health`)
- Root endpoint (`/`)
- Node registration (`POST /api/v1/nodes/register`)
- Node listing (`GET /api/v1/nodes`)
- Node retrieval (`GET /api/v1/nodes/{id}`)
- Node heartbeat (`POST /api/v1/nodes/{id}/heartbeat`)
- Error handling (404s, validation errors)

### `test_deployments.py`
**Type:** Integration Tests  
**Coverage:** Deployment management API endpoints

Tests FastAPI endpoints for:
- Deployment creation (`POST /api/v1/deployments`)
- Deployment listing (`GET /api/v1/deployments`)
- Deployment retrieval (`GET /api/v1/deployments/{id}`)
- Deployment deletion (`DELETE /api/v1/deployments/{id}`)
- Duplicate deployment handling

### `test_placement.py`
**Type:** Unit Tests  
**Coverage:** Placement engine logic

Tests node selection algorithm:
- Node scoring (memory, disk, GPU weights)
- Requirement filtering (GPU requirements)
- Best node selection from multiple candidates
- Edge cases (no nodes, missing capabilities)
- Multiple GPU handling

### `test_integration.py`
**Type:** Integration Tests  
**Coverage:** End-to-end workflows

Tests complete workflows:
- Node registration → listing → retrieval
- Node heartbeat → metrics update
- Multiple node registration
- Deployment creation → retrieval → deletion
- Node re-registration (update existing)
- Concurrent heartbeats
- Error scenarios (missing nodes, etc.)

### `test_templates.py`
**Type:** Unit Tests (Stubs)  
**Coverage:** Template rendering (future Sprint 2 feature)

Placeholder tests for template rendering:
- Jinja2 template loading
- Variable substitution
- Template validation
- Service-specific templates (Postgres, Redis, Ollama)

All tests are currently skipped with descriptive TODOs for implementation.

## Running Tests

### Run all tests
```bash
pytest tests/ -v
```

### Run specific test file
```bash
pytest tests/test_placement.py -v
pytest tests/test_integration.py -v
```

### Run tests with coverage
```bash
pytest tests/ --cov=app --cov-report=html
# Open htmlcov/index.html to view coverage report
```

### Run tests matching a pattern
```bash
pytest tests/ -k "placement" -v
pytest tests/ -k "heartbeat" -v
```

## Test Configuration

### `conftest.py`
Contains pytest fixtures and configuration:
- `client` - FastAPI TestClient with test database
- `setup_database` - Clears database between tests
- Database override - Uses in-memory SQLite for isolation

### Test Database
- Uses SQLite in-memory database (`:memory:`)
- Automatically cleared between tests
- Fast and isolated (no side effects)

## Writing New Tests

When adding new features, follow these patterns:

### Unit Test Example
```python
def test_new_function():
    """Test description."""
    # Arrange
    input_data = {...}
    
    # Act
    result = my_function(input_data)
    
    # Assert
    assert result == expected
```

### API Test Example
```python
def test_new_endpoint(client):
    """Test description."""
    response = client.post('/api/v1/endpoint', json={...})
    assert response.status_code == 200
    assert response.json()['field'] == 'value'
```

### Integration Test Example
```python
def test_complete_workflow(client):
    """Test description."""
    # Step 1: Setup
    reg_response = client.post('/api/v1/nodes/register', json={...})
    node_id = reg_response.json()['node_id']
    
    # Step 2: Execute action
    action_response = client.post(f'/api/v1/nodes/{node_id}/action')
    
    # Step 3: Verify result
    verify_response = client.get(f'/api/v1/nodes/{node_id}')
    assert verify_response.json()['status'] == 'expected'
```

## Test Guidelines

1. **Test names:** Use descriptive names starting with `test_`
2. **Docstrings:** Every test should have a brief description
3. **Arrange-Act-Assert:** Follow the AAA pattern
4. **Isolation:** Tests should not depend on other tests
5. **Assertions:** Use clear, specific assertions
6. **Mocking:** Mock external dependencies (HTTP, DB, etc.)

## Continuous Integration

Tests are automatically run on:
- Every push to main/master branches
- Every pull request
- Via `.github/workflows/ci.yml`

CI requirements:
- All tests must pass
- No decrease in test coverage

## Related Documentation

- [Test Strategy](../../TEST_STRATEGY.md) - Comprehensive testing documentation
- [Testing Guide](../../TESTING.md) - Manual testing guide
- [Architecture](../../MIaaS.md) - System architecture
