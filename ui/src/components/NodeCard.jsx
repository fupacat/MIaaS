import './NodeCard.css'

function NodeCard({ node }) {
  const formatLastSeen = (timestamp) => {
    if (!timestamp) return 'Never'
    const date = new Date(timestamp * 1000)
    return date.toLocaleString()
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'online':
        return '#4ade80'
      case 'offline':
        return '#ef4444'
      default:
        return '#fbbf24'
    }
  }

  return (
    <div className="node-card">
      <div className="node-header">
        <div className="node-status" style={{ backgroundColor: getStatusColor(node.status) }}></div>
        <h3 className="node-name">{node.name}</h3>
      </div>
      
      <div className="node-details">
        <div className="detail-row">
          <span className="label">ID:</span>
          <span className="value">{node.id.substring(0, 8)}...</span>
        </div>
        
        <div className="detail-row">
          <span className="label">IP:</span>
          <span className="value">{node.ip}</span>
        </div>
        
        <div className="detail-row">
          <span className="label">Status:</span>
          <span className="value">{node.status}</span>
        </div>
        
        <div className="detail-row">
          <span className="label">Last Seen:</span>
          <span className="value">{formatLastSeen(node.last_seen)}</span>
        </div>

        {node.capabilities && (
          <div className="capabilities">
            <span className="label">Capabilities:</span>
            <div className="capabilities-list">
              {Object.entries(node.capabilities).map(([key, value]) => (
                <span key={key} className="capability-tag">
                  {key}: {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default NodeCard
