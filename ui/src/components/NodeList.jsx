import NodeCard from './NodeCard'
import './NodeList.css'

function NodeList({ nodes }) {
  if (nodes.length === 0) {
    return (
      <div className="empty-state">
        <p>No nodes registered yet.</p>
        <p className="hint">Register a node to see it appear here.</p>
      </div>
    )
  }

  return (
    <div className="node-list">
      {nodes.map((node) => (
        <NodeCard key={node.id} node={node} />
      ))}
    </div>
  )
}

export default NodeList
