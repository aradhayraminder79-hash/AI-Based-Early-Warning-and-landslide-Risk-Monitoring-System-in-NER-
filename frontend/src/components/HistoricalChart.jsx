import React, { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { getHistory } from '../services/api.js'

export default function HistoricalChart({ zones, selectedZoneId, onSelectZone, expanded }) {
  const [series, setSeries] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!selectedZoneId) return
    let mounted = true
    setLoading(true)
    getHistory(selectedZoneId, 14)
      .then((res) => mounted && setSeries(res.series))
      .catch((err) => mounted && setError(err.message))
      .finally(() => mounted && setLoading(false))
    return () => { mounted = false }
  }, [selectedZoneId])

  const zone = zones.find((z) => z.id === selectedZoneId)

  return (
    <div className="card">
      <div className="section-title">
        <h2>Historical Risk Chart</h2>
        <select className="zone-select" value={selectedZoneId || ''} onChange={(e) => onSelectZone(e.target.value)}>
          {zones.map((z) => (
            <option key={z.id} value={z.id}>{z.name}, {z.state}</option>
          ))}
        </select>
      </div>

      {error && <div className="banner banner--error">{error}</div>}

      <div style={{ width: '100%', height: expanded ? 380 : 240 }}>
        {!loading && series.length > 0 && (
          <ResponsiveContainer>
            <LineChart data={series}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-soft)" />
              <XAxis dataKey="date" tick={{ fontSize: 11, fill: 'var(--text-muted)' }} />
              <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: 'var(--text-muted)' }} />
              <Tooltip
                contentStyle={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)', borderRadius: 8, fontSize: 12 }}
                labelStyle={{ color: 'var(--text-secondary)' }}
              />
              <Line type="monotone" dataKey="probability" name={`Probability — ${zone?.name || ''}`} stroke="#2ec4b6" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
      <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 8 }}>
        DEMO DATA — synthetic time series generated for demonstration; not a stored prediction history.
      </p>
    </div>
  )
}
