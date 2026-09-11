import React from 'react'

const LEVELS = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']

export default function SummaryCards({ zones, loading }) {
  const counts = LEVELS.reduce((acc, level) => {
    acc[level] = zones.filter((z) => z.risk_level === level).length
    return acc
  }, {})

  const cards = [
    { label: 'Total Monitored Zones', value: zones.length, chipClass: '' },
    { label: 'Low Risk Zones', value: counts.LOW, chipClass: 'badge-LOW', level: 'LOW' },
    { label: 'Medium Risk Zones', value: counts.MEDIUM, chipClass: 'badge-MEDIUM', level: 'MEDIUM' },
    { label: 'High Risk Zones', value: counts.HIGH, chipClass: 'badge-HIGH', level: 'HIGH' },
    { label: 'Critical Zones', value: counts.CRITICAL, chipClass: 'badge-CRITICAL', level: 'CRITICAL' },
  ]

  return (
    <div>
      <div className="section-title">
        <h2>Overall Risk Summary</h2>
        <span>Live across all monitored zones</span>
      </div>
      <div className="summary-grid">
        {cards.map((c) => (
          <div className="summary-card" key={c.label}>
            {loading ? (
              <div className="skeleton" style={{ height: 26, width: 40 }} />
            ) : (
              <span className="value">{c.value}</span>
            )}
            <span className="label">{c.label}</span>
            {c.level && <span className={`chip badge ${c.chipClass}`}>{c.level}</span>}
          </div>
        ))}
      </div>
    </div>
  )
}
