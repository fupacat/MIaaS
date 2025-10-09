# Agent Tests

This directory contains automated tests for the MIaaS agent.

## Test Files

### `test_capabilities.py`
**Type:** Unit Tests  
**Coverage:** Agent capability detection and communication

Tests core agent functionality:

#### Capability Detection
- `test_get_capabilities_success` - Successful capability detection
- `test_get_capabilities_with_error_returns_fallback` - Fallback on errors
- `test_get_capabilities_windows` - Windows OS detection
- `test_get_capabilities_darwin` - macOS detection
- `test_capabilities_memory_calculation` - Memory conversion (bytes → MB)

#### Network Discovery
- `test_get_host_ip_success` - IP address detection
- `test_get_host_ip_fallback_on_error` - Fallback to localhost

#### Registration
- `test_register_success` - Successful agent registration
- `test_register_failure` - Registration error handling

#### Heartbeat
- `test_send_heartbeat_success` - Successful heartbeat
- `test_send_heartbeat_failure` - Heartbeat error handling
- `test_heartbeat_disk_calculation` - Disk space calculation

## Running Tests

### Run all agent tests
```bash
cd agent
pytest tests/ -v
```

### Run with coverage
```bash
pytest tests/ --cov=agent --cov-report=html
```

### Run specific tests
```bash
pytest tests/test_capabilities.py::test_get_capabilities_success -v
pytest tests/ -k "heartbeat" -v
```

## Test Patterns

### Mocking External Dependencies

The agent tests extensively mock external dependencies to ensure:
- Tests don't require network access
- Tests don't depend on system state
- Tests run quickly and reliably

Example:
```python
with patch('agent.psutil.virtual_memory') as mock_mem, \
     patch('agent.requests.post') as mock_post:
    mock_mem.return_value = MagicMock(total=16*1024*1024*1024)
    mock_post.return_value = MagicMock(status_code=200)
    
    result = agent.get_capabilities()
    assert result['mem_mb'] == 16384
```

### Testing Error Handling

All functions that can fail are tested for graceful degradation:
```python
def test_function_with_error():
    with patch('agent.external_call', side_effect=Exception("error")):
        result = agent.function_that_calls_external()
        assert result is False  # or fallback value
```

## Mocked Dependencies

The following are mocked in tests:

### System Information (`psutil`)
- `psutil.virtual_memory()` - Memory information
- `psutil.cpu_count()` - CPU count
- `psutil.cpu_percent()` - CPU usage
- `psutil.disk_usage()` - Disk information

### Network (`socket`)
- `socket.socket()` - Network socket creation
- `socket.gethostname()` - Hostname retrieval

### HTTP Requests (`requests`)
- `requests.post()` - HTTP POST requests

### Platform
- `platform.system()` - OS detection

## Test Data

### Realistic Test Values
Tests use realistic values to catch common errors:
- Memory: 8GB, 16GB, 32GB
- CPUs: 4, 8, 12, 16 cores
- Disk: 50GB, 100GB, 500GB free
- GPUs: Empty list, single GPU, multiple GPUs

### Edge Cases
- Zero values (CPU usage = 0%)
- Missing capabilities
- Network failures
- System errors

## Writing New Tests

### Unit Test Template
```python
def test_new_feature():
    """Test description of what is being tested."""
    with patch('agent.dependency') as mock_dep:
        # Arrange
        mock_dep.return_value = test_value
        
        # Act
        result = agent.new_function()
        
        # Assert
        assert result == expected_value
        mock_dep.assert_called_once()
```

### Error Handling Template
```python
def test_new_feature_error_handling():
    """Test that errors are handled gracefully."""
    with patch('agent.dependency', side_effect=Exception("error")):
        result = agent.new_function()
        assert result is False  # or appropriate fallback
```

## Test Guidelines

1. **Mock all external calls** - Don't make real HTTP requests or system calls
2. **Test both success and failure** - Every function should have both happy path and error tests
3. **Use realistic test data** - Make test values look like real system values
4. **Test calculations** - Verify unit conversions (bytes→MB, etc.)
5. **Test edge cases** - Empty values, missing fields, timeouts

## Integration with Control Plane

While these are unit tests, they verify the agent's ability to:
- Send correctly formatted registration requests
- Include all required capability fields
- Send heartbeats with metrics
- Handle control plane errors gracefully

See `control-plane/tests/test_integration.py` for full agent ↔ control plane integration tests.

## Continuous Integration

Agent tests run in CI alongside control plane tests:
```yaml
- name: Test Agent
  run: cd agent && pytest tests/ -v
```

## Future Tests

Planned tests for Sprint 2+:
- Docker Compose execution
- Container management
- Log streaming
- Deployment status reporting
- Template execution

## Related Documentation

- [Test Strategy](../../TEST_STRATEGY.md) - Complete testing documentation
- [Agent Implementation](../agent.py) - Agent source code
- [Architecture](../../MIaaS.md) - System architecture
