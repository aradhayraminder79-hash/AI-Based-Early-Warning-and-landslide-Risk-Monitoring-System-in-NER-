import React from 'react'

const METRICS = [
  { key: 'rainfall_24h', label: 'Rainfall (24h)', unit: 'mm', max: 300, color: 'var(--teal)' },
  { key: 'soil_moisture', label: 'Soil Moisture', unit: '%', max: 100, color: 'var(--amber)' },
  { key: 'slope', label: 'Slope', unit: '°', max: 60, color: 'var(--orange)' },
  { key: 'elevation', label: 'Elevation', unit: 'm', max: 3000, color: 'var(--teal)' },
  { key: 'historical_events', label: 'Historical Events', unit: '', max: 6, color: 'var(--red)' },
]

export default function EnvironmentalConditions({ zone, zones, onSelectZone, expanded }) {
  return (
    <div className="card">
      <div className="section-title">
        <h2>Environmental Conditions</h2>
        <select className="zone-select" value={zone?.id || ''} onChange={(e) => onSelectZone(e.target.value)}>
          {zones.map((z) => (
            <option key={z.id} value={z.id}>{z.name}, {z.state}</option>
          ))}
        </select>
      </div>

      {!zone ? (
        <p style={{ fontSize: 13, color: 'var(--text-secondary)' }}>No zone data available yet.</p>
      ) : (
        <>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 6 }}>
            <span className={`badge badge-${zone.risk_level}`}>{zone.risk_level}</span>
            <span style={{ fontSize: 12.5, color: 'var(--text-secondary)' }}>
              Probability: {zone.probability}%
            </span>
          </div>

          <div className="env-metric-grid" style={expanded ? { gridTemplateColumns: 'repeat(3, 1fr)' } : undefined}>
            {METRICS.map((m) => {
              const value = zone[m.key]
              const pct = Math.min(100, (value / m.max) * 100)
              return (
                <div className="env-metric" key={m.key}>
                  <div className="env-label">{m.label}</div>
                  <div className="env-value">{value}{m.unit}</div>
                  <div className="bar-track">
                    <div className="bar-fill" style={{ width: `${pct}%`, background: m.color }} />
                  </div>
                </div>
              )
            })}
          </div>
        </>
      )}
    </div>
  )
}
