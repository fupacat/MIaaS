"""Data models for the Control Plane."""
from datetime import datetime, timezone
from typing import Dict, List, Optional


class Node:
    """Node model representing a registered agent node."""
    
    def __init__(self, 
                 node_id: str,
                 hostname: str,
                 capabilities: Optional[List[str]] = None,
                 status: str = "active",
                 last_heartbeat: Optional[datetime] = None):
        """Initialize a Node instance.
        
        Args:
            node_id: Unique identifier for the node
            hostname: Hostname of the node
            capabilities: List of capabilities the node supports
            status: Current status of the node (active, inactive, etc.)
            last_heartbeat: Timestamp of the last heartbeat received
        """
        self.id = node_id
        self.hostname = hostname
        self.capabilities = capabilities or []
        self.status = status
        self.last_heartbeat = last_heartbeat or datetime.now(timezone.utc)
    
    def to_dict(self) -> Dict:
        """Convert node to dictionary representation.
        
        Returns:
            Dictionary representation of the node
        """
        return {
            "id": self.id,
            "hostname": self.hostname,
            "capabilities": self.capabilities,
            "status": self.status,
            "last_heartbeat": self.last_heartbeat.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Node':
        """Create a Node instance from a dictionary.
        
        Args:
            data: Dictionary containing node data
            
        Returns:
            Node instance
        """
        return cls(
            node_id=data.get("id"),
            hostname=data.get("hostname"),
            capabilities=data.get("capabilities", []),
            status=data.get("status", "active"),
            last_heartbeat=datetime.fromisoformat(data["last_heartbeat"]) 
                          if "last_heartbeat" in data 
                          else datetime.now(timezone.utc)
        )
    
    def update_heartbeat(self):
        """Update the last_heartbeat timestamp to current time."""
        self.last_heartbeat = datetime.now(timezone.utc)
