"""Unit tests for agent capability detection."""
import pytest
from unittest.mock import patch, MagicMock
import platform


# Import agent module
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import agent


def test_get_capabilities_success():
    """Test successful capability detection."""
    with patch('agent.psutil.virtual_memory') as mock_mem, \
         patch('agent.psutil.disk_usage') as mock_disk, \
         patch('agent.psutil.cpu_count') as mock_cpu, \
         patch('agent.platform.system') as mock_system:
        
        # Mock psutil returns
        mock_mem.return_value = MagicMock(total=16 * 1024 * 1024 * 1024)  # 16GB
        mock_disk.return_value = MagicMock()
        mock_cpu.return_value = 8
        mock_system.return_value = "Linux"
        
        capabilities = agent.get_capabilities()
        
        assert capabilities["os"] == "linux"
        assert capabilities["cpu_count"] == 8
        assert capabilities["mem_mb"] == 16384
        assert "gpus" in capabilities
        assert isinstance(capabilities["gpus"], list)


def test_get_capabilities_with_error_returns_fallback():
    """Test capability detection returns fallback on error."""
    with patch('agent.psutil.virtual_memory', side_effect=Exception("Test error")), \
         patch('agent.platform.system', return_value="Linux"):
        
        capabilities = agent.get_capabilities()
        
        # Should return fallback values
        assert capabilities["os"] == "linux"
        assert capabilities["cpu_count"] == 1
        assert capabilities["mem_mb"] == 1024
        assert capabilities["gpus"] == []


def test_get_capabilities_windows():
    """Test capability detection on Windows."""
    with patch('agent.psutil.virtual_memory') as mock_mem, \
         patch('agent.psutil.disk_usage') as mock_disk, \
         patch('agent.psutil.cpu_count') as mock_cpu, \
         patch('agent.platform.system') as mock_system:
        
        mock_mem.return_value = MagicMock(total=8 * 1024 * 1024 * 1024)  # 8GB
        mock_disk.return_value = MagicMock()
        mock_cpu.return_value = 4
        mock_system.return_value = "Windows"
        
        capabilities = agent.get_capabilities()
        
        assert capabilities["os"] == "windows"
        assert capabilities["cpu_count"] == 4
        assert capabilities["mem_mb"] == 8192


def test_get_capabilities_darwin():
    """Test capability detection on macOS."""
    with patch('agent.psutil.virtual_memory') as mock_mem, \
         patch('agent.psutil.disk_usage') as mock_disk, \
         patch('agent.psutil.cpu_count') as mock_cpu, \
         patch('agent.platform.system') as mock_system:
        
        mock_mem.return_value = MagicMock(total=32 * 1024 * 1024 * 1024)  # 32GB
        mock_disk.return_value = MagicMock()
        mock_cpu.return_value = 12
        mock_system.return_value = "Darwin"
        
        capabilities = agent.get_capabilities()
        
        assert capabilities["os"] == "darwin"
        assert capabilities["cpu_count"] == 12
        assert capabilities["mem_mb"] == 32768


def test_get_host_ip_success():
    """Test getting host IP address successfully."""
    with patch('agent.socket.socket') as mock_socket_class:
        mock_socket = MagicMock()
        mock_socket.getsockname.return_value = ("192.168.1.100", 12345)
        mock_socket_class.return_value = mock_socket
        
        ip = agent.get_host_ip()
        
        assert ip == "192.168.1.100"
        mock_socket.connect.assert_called_once_with(("8.8.8.8", 80))
        mock_socket.close.assert_called_once()


def test_get_host_ip_fallback_on_error():
    """Test get_host_ip returns localhost on error."""
    with patch('agent.socket.socket', side_effect=Exception("Network error")):
        
        ip = agent.get_host_ip()
        
        assert ip == "127.0.0.1"


def test_register_success():
    """Test successful agent registration."""
    with patch('agent.requests.post') as mock_post, \
         patch('agent.get_capabilities', return_value={"os": "linux", "cpu_count": 4}), \
         patch('agent.get_host_ip', return_value="192.168.1.100"), \
         patch('agent.socket.gethostname', return_value="test-node"):
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "node_id": "test-node-id",
            "node_token": "test-token",
            "control_plane_url": "http://localhost:8080"
        }
        mock_post.return_value = mock_response
        
        result = agent.register()
        
        assert result["node_id"] == "test-node-id"
        assert result["node_token"] == "test-token"
        
        # Verify the request was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert "/api/v1/nodes/register" in call_args[0][0]
        
        # Verify payload structure
        payload = call_args[1]["json"]
        assert payload["name"] == "test-node"
        assert payload["ip"] == "192.168.1.100"
        assert payload["capabilities"]["os"] == "linux"


def test_register_failure():
    """Test agent registration failure."""
    with patch('agent.requests.post') as mock_post, \
         patch('agent.get_capabilities', return_value={}), \
         patch('agent.get_host_ip', return_value="127.0.0.1"), \
         patch('agent.socket.gethostname', return_value="test-node"):
        
        mock_post.side_effect = Exception("Connection error")
        
        with pytest.raises(Exception):
            agent.register()


def test_send_heartbeat_success():
    """Test successful heartbeat sending."""
    with patch('agent.requests.post') as mock_post, \
         patch('agent.psutil.cpu_percent', return_value=45.5), \
         patch('agent.psutil.virtual_memory') as mock_mem, \
         patch('agent.psutil.disk_usage') as mock_disk:
        
        mock_mem.return_value = MagicMock(percent=60.2)
        mock_disk.return_value = MagicMock(free=50000 * 1024 * 1024)  # 50000 MB
        
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ok"}
        mock_post.return_value = mock_response
        
        result = agent.send_heartbeat("test-node-id", "test-token")
        
        assert result is True
        
        # Verify heartbeat payload
        call_args = mock_post.call_args
        payload = call_args[1]["json"]
        assert payload["cpu_usage"] == 45.5
        assert payload["mem_usage"] == 60.2
        assert payload["disk_free_mb"] == 50000
        
        # Verify Authorization header is set with JWT token
        headers = call_args[1]["headers"]
        assert headers["Authorization"] == "Bearer test-token"


def test_send_heartbeat_failure():
    """Test heartbeat sending failure."""
    import requests
    
    with patch('agent.requests.post') as mock_post, \
         patch('agent.psutil.cpu_percent', return_value=0), \
         patch('agent.psutil.virtual_memory') as mock_mem, \
         patch('agent.psutil.disk_usage') as mock_disk:
        
        mock_mem.return_value = MagicMock(percent=0)
        mock_disk.return_value = MagicMock(free=0)
        # Use the correct exception type that the code catches
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")
        
        result = agent.send_heartbeat("test-node-id", "test-token")
        
        assert result is False


def test_capabilities_memory_calculation():
    """Test memory is correctly converted from bytes to MB."""
    with patch('agent.psutil.virtual_memory') as mock_mem, \
         patch('agent.psutil.disk_usage') as mock_disk, \
         patch('agent.psutil.cpu_count') as mock_cpu, \
         patch('agent.platform.system') as mock_system:
        
        # 1GB = 1024 * 1024 * 1024 bytes
        mock_mem.return_value = MagicMock(total=1024 * 1024 * 1024)
        mock_disk.return_value = MagicMock()
        mock_cpu.return_value = 2
        mock_system.return_value = "Linux"
        
        capabilities = agent.get_capabilities()
        
        # Should be 1024 MB
        assert capabilities["mem_mb"] == 1024


def test_heartbeat_disk_calculation():
    """Test disk space is correctly converted from bytes to MB."""
    with patch('agent.requests.post') as mock_post, \
         patch('agent.psutil.cpu_percent', return_value=0), \
         patch('agent.psutil.virtual_memory') as mock_mem, \
         patch('agent.psutil.disk_usage') as mock_disk:
        
        mock_mem.return_value = MagicMock(percent=0)
        # 2GB free = 2 * 1024 * 1024 * 1024 bytes
        mock_disk.return_value = MagicMock(free=2 * 1024 * 1024 * 1024)
        
        mock_response = MagicMock()
        mock_post.return_value = mock_response
        
        agent.send_heartbeat("test-node-id", "test-token")
        
        # Should be 2048 MB
        call_args = mock_post.call_args
        payload = call_args[1]["json"]
        assert payload["disk_free_mb"] == 2048
