# JWT Authentication for MIaaS Agents

This document describes the JWT-based authentication mechanism for node agents in the MIaaS control plane.

## Overview

MIaaS uses JWT (JSON Web Tokens) to authenticate agent nodes when they communicate with the control plane. This ensures that only registered nodes can send heartbeats and receive deployment commands.

## Architecture

### Registration Flow

1. **Agent Startup**: When an agent starts, it sends a registration request to the control plane with:
   - Node name (hostname)
   - IP address
   - Capabilities (CPU, memory, GPUs, etc.)

2. **Token Issuance**: The control plane:
   - Creates or updates the node record in the database
   - Generates a JWT token specific to that node
   - Returns the node ID and JWT token

3. **Token Storage**: The agent stores the JWT token in memory and uses it for all subsequent API calls

### Authentication Flow

1. **API Request**: When making authenticated requests (e.g., heartbeat), the agent includes the JWT token in the `Authorization` header:
   ```
   Authorization: Bearer <jwt-token>
   ```

2. **Token Validation**: The control plane:
   - Extracts the token from the Authorization header
   - Verifies the token signature using the JWT secret
   - Checks token expiration
   - Validates the token type is "node_agent"
   - Extracts the node ID from the token payload

3. **Authorization**: For node-specific endpoints (e.g., `/nodes/{node_id}/heartbeat`), the control plane verifies that the authenticated node ID matches the node ID in the URL path.

## JWT Token Structure

JWT tokens contain the following claims:

```json
{
  "node_id": "550e8400-e29b-41d4-a716-446655440000",
  "node_name": "worker-01",
  "type": "node_agent",
  "iat": 1234567890,
  "exp": 1234654290
}
```

- `node_id`: Unique identifier for the node
- `node_name`: Human-readable name of the node
- `type`: Token type (always "node_agent" for agent tokens)
- `iat`: Issued at timestamp (Unix timestamp)
- `exp`: Expiration timestamp (Unix timestamp)

## Configuration

### Control Plane Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `JWT_SECRET` | Secret key for signing JWT tokens | `development-secret-change-in-production` |
| `JWT_EXPIRATION_HOURS` | Token expiration time in hours | `24` |

**⚠️ IMPORTANT**: In production, always set a strong, random `JWT_SECRET` value.

### Agent Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CONTROL_PLANE_URL` | URL of the control plane API | `http://localhost:8080` |
| `HEARTBEAT_INTERVAL` | Seconds between heartbeats | `30` |

## Security Best Practices

1. **Strong Secret**: Use a strong, randomly generated secret for `JWT_SECRET` in production
2. **HTTPS Only**: Always use HTTPS in production to prevent token interception
3. **Token Rotation**: Tokens expire after 24 hours by default. Agents automatically re-register when needed
4. **Secure Storage**: Never log or expose JWT tokens in plain text
5. **Environment Variables**: Store secrets in environment variables, never in code

## Token Lifecycle

### Token Expiration

Tokens expire after 24 hours (configurable via `JWT_EXPIRATION_HOURS`). When a token expires:

1. The agent's next heartbeat will fail with a 401 Unauthorized error
2. After 5 consecutive failed heartbeats, the agent automatically re-registers
3. Re-registration issues a new JWT token
4. The agent resumes normal operation with the new token

### Token Rotation

To rotate tokens before expiration:

1. Simply re-register the agent (same name will update the existing node)
2. The control plane will issue a new JWT token
3. Update the agent's stored token with the new value

## API Endpoints

### Registration (No Auth Required)

```http
POST /api/v1/nodes/register
Content-Type: application/json

{
  "name": "worker-01",
  "ip": "192.168.1.10",
  "capabilities": {
    "os": "linux",
    "cpu_count": 8,
    "mem_mb": 32000,
    "gpus": []
  }
}
```

Response:
```json
{
  "node_id": "550e8400-e29b-41d4-a716-446655440000",
  "node_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "control_plane_url": "http://localhost:8080"
}
```

### Heartbeat (Auth Required)

```http
POST /api/v1/nodes/{node_id}/heartbeat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "cpu_usage": 45.5,
  "mem_usage": 60.2,
  "disk_free_mb": 100000,
  "running_containers": []
}
```

Response:
```json
{
  "status": "ok",
  "timestamp": 1234567890.123
}
```

## Error Handling

### 401 Unauthorized

Occurs when:
- No Authorization header is provided
- Token is invalid or malformed
- Token has expired
- Token signature verification fails

Response:
```json
{
  "detail": "Invalid or expired token"
}
```

**Agent Action**: Re-register to obtain a new token

### 403 Forbidden

Occurs when:
- Token is valid but the authenticated node ID doesn't match the requested node ID

Response:
```json
{
  "detail": "Cannot send heartbeat for a different node"
}
```

**Agent Action**: This indicates a configuration error. Check that the agent is using the correct node ID.

## Implementation Examples

### Python Agent (Using requests)

```python
import requests

# Registration
registration_response = requests.post(
    "http://control-plane:8080/api/v1/nodes/register",
    json={
        "name": "worker-01",
        "ip": "192.168.1.10",
        "capabilities": {...}
    }
)
node_id = registration_response.json()["node_id"]
token = registration_response.json()["node_token"]

# Heartbeat with authentication
heartbeat_response = requests.post(
    f"http://control-plane:8080/api/v1/nodes/{node_id}/heartbeat",
    json={
        "cpu_usage": 45.5,
        "mem_usage": 60.2,
        "disk_free_mb": 100000,
        "running_containers": []
    },
    headers={"Authorization": f"Bearer {token}"}
)
```

### curl Examples

Registration:
```bash
curl -X POST http://localhost:8080/api/v1/nodes/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "worker-01",
    "ip": "192.168.1.10",
    "capabilities": {
      "os": "linux",
      "cpu_count": 8,
      "mem_mb": 32000,
      "gpus": []
    }
  }'
```

Heartbeat:
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
NODE_ID="550e8400-e29b-41d4-a716-446655440000"

curl -X POST http://localhost:8080/api/v1/nodes/$NODE_ID/heartbeat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cpu_usage": 45.5,
    "mem_usage": 60.2,
    "disk_free_mb": 100000,
    "running_containers": []
  }'
```

## Testing

The control plane includes comprehensive tests for JWT authentication:

```bash
cd control-plane
pytest tests/test_auth.py -v
```

Test coverage includes:
- Token creation and verification
- Expired token handling
- Invalid token handling
- Registration with JWT issuance
- Authenticated heartbeat
- Authorization checks (node ID matching)

## Troubleshooting

### Agent cannot authenticate

1. **Check token format**: Ensure the Authorization header uses "Bearer" scheme
2. **Verify token**: Use jwt.io to decode and inspect the token payload
3. **Check expiration**: Verify the token hasn't expired (check `exp` claim)
4. **Secret mismatch**: Ensure control plane and agent are using the same JWT secret

### Heartbeat returns 403

This means the authenticated node ID doesn't match the URL node ID. Check that:
1. The agent is using the correct node ID from registration
2. The token was issued for the correct node
3. The agent isn't trying to impersonate another node

### Token expired too quickly

Adjust the `JWT_EXPIRATION_HOURS` environment variable on the control plane to increase token lifetime.

## Future Enhancements

Potential improvements for the authentication system:

1. **Token Refresh**: Implement a refresh token mechanism to extend sessions without full re-registration
2. **Role-Based Access**: Add roles/scopes to tokens for fine-grained permissions
3. **Token Revocation**: Implement a token blacklist for immediate revocation
4. **Public Key Cryptography**: Move from HMAC (HS256) to RSA (RS256) for better key management
5. **OAuth2 Integration**: Support OAuth2 flows for user authentication
6. **Mutual TLS**: Add mTLS as an alternative authentication method

## References

- [JWT.io](https://jwt.io/) - JWT debugger and documentation
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [MIaaS Architecture](../MIaaS.md) - Full system architecture document
