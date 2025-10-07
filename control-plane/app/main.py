from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import time

app = FastAPI(title="MIaaS Control Plane", version="0.1.0")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for MVP
nodes = {}


class RegisterReq(BaseModel):
    name: str
    ip: str
    capabilities: dict


@app.post("/api/v1/nodes/register")
def register_node(body: RegisterReq):
    node_id = str(uuid.uuid4())
    nodes[node_id] = {
        "id": node_id,
        "name": body.name,
        "ip": body.ip,
        "capabilities": body.capabilities,
        "last_seen": time.time(),
        "status": "online",
    }
    return {"node_id": node_id, "node_token": f"node-token-{node_id}"}


@app.get("/api/v1/nodes")
def list_nodes():
    return list(nodes.values())


@app.get("/")
def root():
    return {"message": "MIaaS Control Plane API", "version": "0.1.0"}
