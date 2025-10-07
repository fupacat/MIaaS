import requests
import time
import socket
import platform
import psutil
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

CONTROL_PLANE = os.environ.get("CONTROL_PLANE_URL", "http://localhost:8080")
HEARTBEAT_INTERVAL = int(os.environ.get("HEARTBEAT_INTERVAL", "30"))

def get_capabilities():
    """Detect and return node capabilities"""
    try:
        mem_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        
        capabilities = {
            "os": platform.system().lower(),
            "cpu_count": psutil.cpu_count(logical=True),
            "mem_mb": mem_info.total // (1024 * 1024),
            "gpus": []  # GPU detection can be added later
        }
        
        logger.info(f"Detected capabilities: {capabilities}")
        return capabilities
    except Exception as e:
        logger.error(f"Error detecting capabilities: {e}")
        # Return minimal capabilities as fallback
        return {
            "os": platform.system().lower(),
            "cpu_count": 1,
            "mem_mb": 1024,
            "gpus": []
        }

def get_host_ip():
    """Get the host IP address"""
    try:
        # Try to get IP by connecting to an external address (doesn't actually send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def register():
    """Register this agent with the control plane"""
    try:
        payload = {
            "name": socket.gethostname(),
            "ip": get_host_ip(),
            "capabilities": get_capabilities()
        }
        
        logger.info(f"Registering with control plane at {CONTROL_PLANE}")
        response = requests.post(
            f"{CONTROL_PLANE}/api/v1/nodes/register",
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Registration successful. Node ID: {data['node_id']}")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to register with control plane: {e}")
        raise

def send_heartbeat(node_id):
    """Send heartbeat with current metrics to control plane"""
    try:
        # Collect current metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        mem_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        
        payload = {
            "cpu_usage": cpu_percent,
            "mem_usage": mem_info.percent,
            "disk_free_mb": disk_info.free // (1024 * 1024),
            "running_containers": []  # Can be enhanced to detect Docker containers
        }
        
        response = requests.post(
            f"{CONTROL_PLANE}/api/v1/nodes/{node_id}/heartbeat",
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        
        logger.debug(f"Heartbeat sent successfully")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send heartbeat: {e}")
        return False

def main():
    """Main agent loop"""
    logger.info("Agent starting...")
    
    # Register with control plane
    try:
        registration_info = register()
        node_id = registration_info["node_id"]
        node_token = registration_info["node_token"]
        logger.info(f"Agent registered successfully with node_id: {node_id}")
    except Exception as e:
        logger.error(f"Failed to register agent: {e}")
        logger.error("Exiting...")
        return
    
    # Main heartbeat loop
    logger.info(f"Starting heartbeat loop (interval: {HEARTBEAT_INTERVAL}s)")
    consecutive_failures = 0
    max_failures = 5
    
    while True:
        try:
            time.sleep(HEARTBEAT_INTERVAL)
            
            if send_heartbeat(node_id):
                consecutive_failures = 0
            else:
                consecutive_failures += 1
                if consecutive_failures >= max_failures:
                    logger.error(f"Failed to send heartbeat {max_failures} times. Attempting re-registration...")
                    try:
                        registration_info = register()
                        node_id = registration_info["node_id"]
                        consecutive_failures = 0
                    except Exception as e:
                        logger.error(f"Re-registration failed: {e}")
                        
        except KeyboardInterrupt:
            logger.info("Agent shutting down...")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            time.sleep(5)  # Brief pause before retrying

if __name__ == "__main__":
    main()
