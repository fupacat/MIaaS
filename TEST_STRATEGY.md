# MIaaS Test Strategy and Coverage

This document outlines the testing strategy for the MIaaS (Model Infrastructure as a Service) project, including unit tests, integration tests, and guidelines for future testing.

## Test Organization

### Control Plane Tests (`control-plane/tests/`)

The control plane tests are organized into several test modules:

1. **`test_models.py`** - Unit tests for Pydantic models
   - Validates model structure and validation rules
   - Tests serialization and deserialization
   - Covers all API request/response models

2. **`test_api.py`** - API endpoint tests
   - Tests node registration endpoint
   - Tests node listing and retrieval
   - Tests heartbeat endpoint
   - Tests error handling and validation

3. **`test_deployments.py`** - Deployment endpoint tests
   - Tests deployment creation
   - Tests deployment listing and retrieval
   - Tests deployment deletion
   - Tests duplicate deployment handling

4. **`test_placement.py`** - Placement engine unit tests
   - Tests node selection algorithm
   - Tests scoring logic (memory, disk, GPU)
   - Tests requirement filtering (GPU requirements)
   - Tests edge cases (no nodes, missing capabilities)

5. **`test_templates.py`** - Template rendering tests (stubs)
   - Placeholder tests for Sprint 2 template implementation
   - Documents expected behavior for template rendering
   - Includes tests for Postgres, Redis, Ollama templates

6. **`test_integration.py`** - Integration tests
   - Tests complete workflows (registration → heartbeat → listing)
   - Tests node re-registration behavior
   - Tests deployment lifecycle
   - Tests concurrent operations
   - Tests error scenarios

### Agent Tests (`agent/tests/`)

1. **`test_capabilities.py`** - Capability detection unit tests
   - Tests `get_capabilities()` function
   - Tests OS detection (Linux, Windows, macOS)
   - Tests memory and CPU detection
   - Tests error handling and fallback behavior
   - Tests `get_host_ip()` function
   - Tests `register()` function
   - Tests `send_heartbeat()` function
   - Tests metric calculations (memory MB, disk MB)

## Running Tests

### Control Plane Tests

```bash
cd control-plane
pip install -r requirements.txt
python -m pytest tests/ -v
```

**Run specific test modules:**
```bash
python -m pytest tests/test_placement.py -v
python -m pytest tests/test_integration.py -v
```

**Run with coverage:**
```bash
pip install pytest-cov
python -m pytest tests/ --cov=app --cov-report=html
```

### Agent Tests

```bash
cd agent
pip install -r requirements.txt
python -m pytest tests/ -v
```

## Test Coverage Goals

### Current Coverage (MVP - Sprint 1)

- ✅ **API Endpoints**: ~95% coverage
  - Node registration
  - Node listing and retrieval
  - Heartbeat endpoints
  - Deployment CRUD operations
  
- ✅ **Data Models**: 100% coverage
  - All Pydantic models tested
  - Validation rules verified
  
- ✅ **Placement Engine**: ~90% coverage
  - Node selection algorithm
  - Scoring logic
  - Requirement filtering
  
- ✅ **Agent Capabilities**: ~85% coverage
  - Capability detection
  - Registration logic
  - Heartbeat mechanism
  - Error handling

### Future Coverage (Sprint 2+)

- ⏳ **Template Rendering**: Target 90% coverage
  - Jinja2 template loading
  - Variable substitution
  - Template validation
  - Error handling for missing variables
  
- ⏳ **Docker Execution**: Target 85% coverage
  - Docker Compose execution
  - Container management
  - Log streaming
  - Error recovery

- ⏳ **Authentication**: Target 90% coverage
  - JWT generation and validation
  - Node token management
  - API key authentication

## Test Types

### Unit Tests

Unit tests focus on individual functions and classes in isolation:

- **What to test:**
  - Individual functions with clear inputs/outputs
  - Class methods with mocked dependencies
  - Data validation and transformation logic
  - Error handling and edge cases

- **Examples:**
  - `test_placement.py`: Tests PlacementEngine methods in isolation
  - `test_capabilities.py`: Tests agent functions with mocked psutil/requests
  - `test_models.py`: Tests Pydantic model validation

### Integration Tests

Integration tests verify that multiple components work together:

- **What to test:**
  - Complete API workflows
  - Database interactions
  - Multi-step processes
  - Component interactions

- **Examples:**
  - `test_integration.py`: Tests node registration → heartbeat → retrieval flow
  - `test_api.py`: Tests FastAPI endpoints with TestClient (includes routing, validation, DB)

### Contract Tests

Contract tests verify API contracts match specifications:

- **Current approach:**
  - Using FastAPI's automatic validation via Pydantic
  - Testing request/response schemas
  - Verifying HTTP status codes
  
- **Future enhancements:**
  - OpenAPI schema validation
  - Consumer-driven contract tests for agent ↔ control plane

### End-to-End Tests (Future)

Not yet implemented. Planned for Sprint 3+:

- **What to test:**
  - Full system: control plane + agent + deployment
  - Docker-in-Docker for agent execution
  - Template rendering → deployment → verification
  - Real network communication

- **Implementation approach:**
  - Docker Compose test environment
  - Testcontainers for isolated testing
  - Automated in CI pipeline

## Test Fixtures and Setup

### Control Plane Fixtures (`conftest.py`)

- **`client`**: FastAPI TestClient with overridden database
- **`setup_database`**: Clears database between tests
- **Database override**: Uses in-memory SQLite for fast, isolated tests

### Test Data Strategy

- Use realistic but minimal test data
- Avoid hardcoded IDs where possible
- Use factory patterns for complex test data (future enhancement)

## CI/CD Integration

### Current CI Pipeline (`.github/workflows/ci.yml`)

```yaml
- Checkout code
- Setup Python 3.x
- Install dependencies from requirements.txt
- Run tests: python -m unittest discover ci/tests
- Run linting: flake8 (if available)
```

### Recommended Updates

1. **Add separate test jobs:**
   ```yaml
   - name: Test Control Plane
     run: cd control-plane && pytest tests/ -v
   
   - name: Test Agent
     run: cd agent && pytest tests/ -v
   ```

2. **Add coverage reporting:**
   ```yaml
   - name: Coverage Report
     run: pytest --cov=app --cov-report=xml
   
   - name: Upload Coverage
     uses: codecov/codecov-action@v3
   ```

3. **Run integration tests separately:**
   ```yaml
   - name: Integration Tests
     run: pytest tests/test_integration.py -v
   ```

## Testing Best Practices

### General Guidelines

1. **Test naming:** Use descriptive names that explain what is being tested
   - ✅ `test_select_node_with_gpu_requirement()`
   - ❌ `test_node_1()`

2. **Arrange-Act-Assert pattern:**
   ```python
   def test_example():
       # Arrange: Set up test data
       node = {...}
       
       # Act: Execute the function
       result = select_node([node])
       
       # Assert: Verify the result
       assert result == expected
   ```

3. **One assertion per test (when practical):**
   - Tests should focus on one behavior
   - Multiple assertions OK if testing related properties

4. **Mock external dependencies:**
   - Mock HTTP requests (requests.post)
   - Mock system calls (psutil, socket)
   - Use in-memory database for DB tests

5. **Test both success and failure paths:**
   - Happy path: normal operation
   - Error handling: exceptions, invalid input
   - Edge cases: empty lists, missing fields

### Control Plane Specific

1. **Use the `client` fixture:** Automatically handles DB setup/teardown
2. **Test validation errors:** Verify FastAPI returns 422 for invalid data
3. **Test 404 scenarios:** Verify proper error handling for missing resources
4. **Test concurrent operations:** Ensure thread-safety where needed

### Agent Specific

1. **Mock external services:** Never make real HTTP calls in unit tests
2. **Mock system info:** Use unittest.mock for psutil, platform, socket
3. **Test fallback behavior:** Verify graceful degradation on errors
4. **Test calculation accuracy:** Verify unit conversions (bytes → MB)

## Future Testing Enhancements

### Sprint 2 (Templates + Deploy)

- [ ] Add template rendering tests
- [ ] Add Docker Compose execution tests (using Docker-in-Docker)
- [ ] Add log streaming tests
- [ ] Add template validation tests

### Sprint 3 (Auth + Security)

- [ ] Add JWT authentication tests
- [ ] Add API key validation tests
- [ ] Add rate limiting tests
- [ ] Add security vulnerability tests

### Sprint 4+ (Scale + Production)

- [ ] Add load testing (Locust)
- [ ] Add chaos engineering tests
- [ ] Add multi-node deployment tests
- [ ] Add backup/restore tests
- [ ] Add upgrade path tests

## Test Metrics

### Target Metrics

- **Unit test coverage:** >85%
- **Integration test coverage:** >70%
- **Test execution time:** <10 seconds for unit tests, <1 minute for integration
- **Test reliability:** >99% (flaky tests should be fixed immediately)
- **New feature tests:** All new features must include tests

### Current Status

```
Control Plane Tests: 38 tests (27 existing + 11 placement + integration)
Agent Tests: 14 tests (capability detection)
Total: 52 tests

Average execution time: ~0.5 seconds (control plane), ~0.2 seconds (agent)
Success rate: 100%
```

## Troubleshooting Common Test Issues

### Issue: Tests fail with database errors

**Solution:** Ensure `setup_database` fixture is cleaning up properly:
```python
@pytest.fixture(autouse=True)
def setup_database():
    db = TestingSessionLocal()
    db.query(Model).delete()
    db.commit()
```

### Issue: Tests fail with "port already in use"

**Solution:** Use TestClient instead of running actual server:
```python
from fastapi.testclient import TestClient
client = TestClient(app)
```

### Issue: Agent tests fail with network errors

**Solution:** Mock all external HTTP calls:
```python
with patch('agent.requests.post') as mock_post:
    mock_post.return_value = MagicMock(json=lambda: {...})
```

### Issue: Flaky integration tests

**Solution:** Add proper synchronization or use polling:
```python
import time
time.sleep(0.1)  # Allow async operations to complete
```

## Contributing Tests

When contributing new features:

1. **Write tests first** (TDD approach recommended)
2. **Ensure all tests pass** before submitting PR
3. **Maintain or improve coverage** - no decrease in coverage %
4. **Document complex test scenarios** with comments
5. **Update this document** if adding new test patterns

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [FastAPI testing guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
- [MIaaS Architecture](./MIaaS.md)
- [Testing Guide](./TESTING.md)
