# Inference Engine Service

The Inference Engine executes ML model inference workloads.

## Responsibilities

- Pull inference requests from message queue
- Load models from Model Registry
- Execute model inference with provided input data
- Support multiple ML frameworks (TensorFlow, PyTorch, ONNX)
- Return inference results
- Scale horizontally based on demand

## Supported Frameworks

- TensorFlow 2.x
- PyTorch 1.x
- ONNX Runtime
- Scikit-learn

## Development

Service implementation coming soon. See [protocol.md](../../docs/protocol.md) for API specifications.
