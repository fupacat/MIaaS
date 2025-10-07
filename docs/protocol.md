# MIaaS Protocol Specification

## Overview

This document defines the protocol and API specifications for Model Inference as a Service (MIaaS).

## Architecture

MIaaS follows a microservices architecture with the following core components:

- **Control Plane**: Orchestrates inference requests and manages service lifecycle
- **Inference Engine**: Executes model inference workloads
- **Model Registry**: Stores and versions ML models

## API Endpoints

### Control Plane API

#### Health Check
```
GET /health
Response: 200 OK
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Submit Inference Request
```
POST /inference
Request:
{
  "model_id": "string",
  "input_data": "object",
  "parameters": "object (optional)"
}

Response: 202 Accepted
{
  "request_id": "string",
  "status": "queued"
}
```

#### Get Inference Result
```
GET /inference/{request_id}
Response: 200 OK
{
  "request_id": "string",
  "status": "completed|processing|failed",
  "result": "object",
  "timestamp": "string"
}
```

### Model Registry API

#### List Models
```
GET /models
Response: 200 OK
{
  "models": [
    {
      "id": "string",
      "name": "string",
      "version": "string",
      "status": "active|deprecated"
    }
  ]
}
```

#### Get Model Details
```
GET /models/{model_id}
Response: 200 OK
{
  "id": "string",
  "name": "string",
  "version": "string",
  "framework": "string",
  "input_schema": "object",
  "output_schema": "object"
}
```

## Communication Protocols

### Inter-Service Communication
- Services communicate via REST APIs over HTTP
- All requests must include authentication headers
- Response format: JSON

### Message Queue
- Inference requests are queued using a message broker
- Supports asynchronous processing
- Guarantees at-least-once delivery

## Error Handling

Standard HTTP status codes:
- `200 OK`: Successful request
- `202 Accepted`: Request accepted for processing
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error response format:
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object (optional)"
  }
}
```

## Security

- All API endpoints require authentication
- Use API keys or OAuth2 tokens
- TLS/HTTPS required for all communications
- Rate limiting: 1000 requests per minute per client

## Versioning

- API version included in URL path: `/v1/endpoint`
- Backward compatibility maintained for at least 2 major versions
