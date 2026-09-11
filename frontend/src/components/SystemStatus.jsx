import React from 'react'

export default function SystemStatus({ apiOnline }) {
  const items = [
    { name: 'AI Model', status: apiOnline ? 'Operational' : 'Unknown', ok: apiOnline },
    { name: 'Backend API', status: apiOnline ? 'Operational' : 'Offline', ok: apiOnline },
    { name: 'Database', status: 'Not configured (demo)', ok: null },
    { name: 'Weather Data', status: 'Demo data source', ok: null },
    { name: 'Map Service', status: 'OpenStreetMap / CARTO', ok: true },
  ]

  return (
    <div className="card">
      <div className="section-title">
        <h2>System Status</h2>
        <span>Component health</span>
      </div>
      <div className="status-grid">
        {items.map((i) => (
          <div className="status-row" key={i.name}>
            <span>{i.name}</span>
            <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <span
                className="status-dot"
                style={{
                  background: i.ok === true ? 'var(--teal)' : i.ok === false ? 'var(--red)' : 'var(--amber)',
                }}
              />
              {i.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
