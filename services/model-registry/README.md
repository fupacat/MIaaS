# Model Registry Service

The Model Registry manages ML model storage, versioning, and metadata.

## Responsibilities

- Store trained ML models
- Manage model versions and metadata
- Track model lifecycle (active, deprecated, archived)
- Provide model discovery API
- Serve models to Inference Engine
- Maintain model schemas and documentation

## API Endpoints

- `GET /models` - List all models
- `GET /models/{model_id}` - Get model details
- `POST /models` - Register new model
- `PUT /models/{model_id}` - Update model metadata
- `DELETE /models/{model_id}` - Archive model

## Development

Service implementation coming soon. See [protocol.md](../../docs/protocol.md) for API specifications.
