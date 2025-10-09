#!/bin/bash
# Script to seed test data into the control-plane

API_URL="${API_URL:-http://localhost:8000}"

echo "Seeding test data to $API_URL..."

# Register test node 1
echo "Registering test-node-1..."
curl -X POST "$API_URL/api/v1/nodes/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-node-1",
    "ip": "192.168.1.100",
    "capabilities": {
      "os": "linux",
      "cpu_count": 8,
      "mem_mb": 16000,
      "disk_mb": 500000,
      "gpus": [{"id": 0, "model": "NVIDIA RTX 3090", "mem_mb": 24000}],
      "docker": {"version": "24.0.0", "available": true}
    }
  }'

echo ""

# Register test node 2
echo "Registering test-node-2..."
curl -X POST "$API_URL/api/v1/nodes/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-node-2",
    "ip": "192.168.1.101",
    "capabilities": {
      "os": "linux",
      "cpu_count": 16,
      "mem_mb": 32000,
      "disk_mb": 1000000,
      "gpus": [{"id": 0, "model": "NVIDIA A100", "mem_mb": 80000}],
      "docker": {"version": "24.0.0", "available": true},
      "k8s": {"version": "1.28.0", "available": true}
    }
  }'

echo ""

# Register test node 3
echo "Registering gpu-worker-1..."
curl -X POST "$API_URL/api/v1/nodes/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "gpu-worker-1",
    "ip": "192.168.1.102",
    "capabilities": {
      "os": "linux",
      "cpu_count": 24,
      "mem_mb": 64000,
      "disk_mb": 2000000,
      "gpus": [{"id": 0, "model": "NVIDIA H100", "mem_mb": 80000}],
      "docker": {"version": "24.0.0", "available": true},
      "k8s": {"version": "1.28.0", "available": true}
    }
  }'

echo ""
echo "Test data seeded successfully!"
