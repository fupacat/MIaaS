from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import time

app = FastAPI(title="MIaaS Control Plane")

# In-memory storage for MVP
nodes = {}

class Capabilities(BaseModel):
    os: str
    cpu_count: int
    mem_mb: int
    gpus: list = []

class RegisterRequest(BaseModel):
    name: str
    ip: str
    capabilities: Capabilities

class HeartbeatRequest(BaseModel):
    cpu_usage: float = 0.0
    mem_usage: float = 0.0
    disk_free_mb: int = 0
    running_containers: list = []

@app.get("/")
def read_root():
    return {"service": "MIaaS Control Plane", "version": "0.1.0"}

@app.post("/api/v1/nodes/register")
def register_node(body: RegisterRequest):
    node_id = str(uuid.uuid4())
    nodes[node_id] = {
        "id": node_id,
        "name": body.name,
        "ip": body.ip,
        "capabilities": body.capabilities.dict(),
        "last_seen": time.time(),
        "status": "online"
    }
    return {
        "node_id": node_id,
        "node_token": f"node-token-{node_id}",
        "control_plane_url": "http://localhost:8080"
    }

@app.get("/api/v1/nodes")
def list_nodes():
    return list(nodes.values())

@app.post("/api/v1/nodes/{node_id}/heartbeat")
def heartbeat(node_id: str, body: HeartbeatRequest):
    if node_id not in nodes:
        raise HTTPException(status_code=404, detail="Node not found")
    
    nodes[node_id]["last_seen"] = time.time()
    nodes[node_id]["status"] = "online"
    nodes[node_id]["metrics"] = body.dict()
    
    return {"status": "ok", "timestamp": time.time()}
