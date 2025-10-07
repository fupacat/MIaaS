"""API endpoints for the Control Plane."""
from flask import Flask, request, jsonify
from .models import Node
from .storage import storage


app = Flask(__name__)


@app.route('/api/v1/nodes/register', methods=['POST'])
def register_node():
    """Register a new node or update an existing one.
    
    Expected JSON payload:
    {
        "id": "node-123",
        "hostname": "worker-01",
        "capabilities": ["docker", "compose"],
        "status": "active"
    }
    
    Returns:
        JSON response with registration status
    """
    try:
        data = request.get_json(silent=True)
        
        # Validate required fields
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if "id" not in data:
            return jsonify({"error": "Missing required field: id"}), 400
        
        if "hostname" not in data:
            return jsonify({"error": "Missing required field: hostname"}), 400
        
        # Create or update node
        node = Node.from_dict(data)
        storage.add_node(node)
        
        return jsonify({
            "message": "Node registered successfully",
            "node": node.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/nodes', methods=['GET'])
def list_nodes():
    """List all registered nodes.
    
    Returns:
        JSON response with list of all nodes
    """
    try:
        nodes = storage.get_all_nodes()
        return jsonify({
            "nodes": [node.to_dict() for node in nodes],
            "count": len(nodes)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/nodes/<node_id>', methods=['GET'])
def get_node(node_id):
    """Get a specific node by ID.
    
    Args:
        node_id: ID of the node to retrieve
        
    Returns:
        JSON response with node details
    """
    try:
        node = storage.get_node(node_id)
        
        if not node:
            return jsonify({"error": "Node not found"}), 404
        
        return jsonify(node.to_dict()), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint.
    
    Returns:
        JSON response with health status
    """
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
