import { useState, useEffect } from 'react'
import './App.css'
import NodeList from './components/NodeList'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function App() {
  const [nodes, setNodes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchNodes()
  }, [])

  const fetchNodes = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await fetch(`${API_BASE_URL}/api/v1/nodes`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      setNodes(data)
    } catch (err) {
      setError(err.message)
      console.error('Error fetching nodes:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>MIaaS Control Plane</h1>
        <p className="subtitle">Model Infrastructure as a Service</p>
      </header>
      
      <main className="app-main">
        <div className="nodes-section">
          <div className="section-header">
            <h2>Nodes</h2>
            <button onClick={fetchNodes} className="refresh-btn">
              ↻ Refresh
            </button>
          </div>
          
          {loading && <div className="loading">Loading nodes...</div>}
          
          {error && (
            <div className="error">
              <p>Error: {error}</p>
              <p className="hint">Make sure the control-plane is running at {API_BASE_URL}</p>
            </div>
          )}
          
          {!loading && !error && <NodeList nodes={nodes} />}
        </div>
      </main>
    </div>
  )
}

export default App
