"""In-memory storage for nodes."""
from typing import Dict, List, Optional
from .models import Node


class NodeStorage:
    """Simple in-memory storage for nodes."""
    
    def __init__(self):
        """Initialize the storage."""
        self._nodes: Dict[str, Node] = {}
    
    def add_node(self, node: Node) -> None:
        """Add or update a node in storage.
        
        Args:
            node: Node to add or update
        """
        self._nodes[node.id] = node
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by ID.
        
        Args:
            node_id: ID of the node to retrieve
            
        Returns:
            Node if found, None otherwise
        """
        return self._nodes.get(node_id)
    
    def get_all_nodes(self) -> List[Node]:
        """Get all nodes.
        
        Returns:
            List of all nodes
        """
        return list(self._nodes.values())
    
    def delete_node(self, node_id: str) -> bool:
        """Delete a node by ID.
        
        Args:
            node_id: ID of the node to delete
            
        Returns:
            True if deleted, False if not found
        """
        if node_id in self._nodes:
            del self._nodes[node_id]
            return True
        return False


# Global storage instance
storage = NodeStorage()
