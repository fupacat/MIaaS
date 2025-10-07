#!/bin/bash
# Script to seed test data into the control-plane

API_URL="${API_URL:-http://localhost:8000}"

echo "Seeding test data to $API_URL..."

# Register test node 1
curl -X POST "$API_URL/api/v1/nodes/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-node-1",
    "ip": "192.168.1.100",
    "capabilities": {
      "cpu": "8 cores",
      "memory": "16GB",
      "gpu": "NVIDIA RTX 3090",
      "docker": true
    }
  }'

echo ""

# Register test node 2
curl -X POST "$API_URL/api/v1/nodes/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-node-2",
    "ip": "192.168.1.101",
    "capabilities": {
      "cpu": "16 cores",
      "memory": "32GB",
      "gpu": "NVIDIA A100",
      "docker": true,
      "k8s": true
    }
  }'

echo ""

# Register test node 3
curl -X POST "$API_URL/api/v1/nodes/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "gpu-worker-1",
    "ip": "192.168.1.102",
    "capabilities": {
      "cpu": "24 cores",
      "memory": "64GB",
      "gpu": "NVIDIA H100",
      "docker": true,
      "k8s": true
    }
  }'

echo ""
echo "Test data seeded successfully!"
