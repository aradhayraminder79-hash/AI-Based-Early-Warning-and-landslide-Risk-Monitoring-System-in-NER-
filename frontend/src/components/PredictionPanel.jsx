import React, { useState } from 'react'
import RiskGauge from './RiskGauge.jsx'
import { postPredict } from '../services/api.js'

const DEFAULTS = {
  rainfall_24h: 120,
  soil_moisture: 65,
  slope: 30,
  elevation: 1200,
  historical_events: 2,
}

const FIELDS = [
  { key: 'rainfall_24h', label: 'Rainfall — 24h (mm)', min: 0, max: 500 },
  { key: 'soil_moisture', label: 'Soil Moisture (%)', min: 0, max: 100 },
  { key: 'slope', label: 'Slope (degrees)', min: 0, max: 90 },
  { key: 'elevation', label: 'Elevation (m)', min: 0, max: 5000 },
  { key: 'historical_events', label: 'Historical Landslide Events', min: 0, max: 20 },
]

export default function PredictionPanel({ onPredicted, expanded }) {
  const [form, setForm] = useState(DEFAULTS)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (key, value) => {
    setForm((f) => ({ ...f, [key]: value === '' ? '' : Number(value) }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const res = await postPredict(form)
      setResult(res)
      onPredicted && onPredicted()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card" style={expanded ? { maxWidth: 640 } : undefined}>
      <div className="section-title">
        <h2>AI Prediction Panel</h2>
        <span>Random Forest model</span>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-grid">
          {FIELDS.map((f) => (
            <div className="field" key={f.key}>
              <label htmlFor={f.key}>{f.label}</label>
              <input
                id={f.key}
                type="number"
                min={f.min}
                max={f.max}
                step="any"
                value={form[f.key]}
                onChange={(e) => handleChange(f.key, e.target.value)}
                required
              />
            </div>
          ))}
        </div>
        <button className="btn-primary" type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Landslide Risk'}
        </button>
      </form>

      {error && <div className="banner banner--error" style={{ marginTop: 14 }}>{error}</div>}

      {result && (
        <div className="prediction-result">
          <div className="gauge-wrap">
            <RiskGauge probability={result.probability} riskLevel={result.risk_level} />
            <div>
              <span className={`badge badge-${result.risk_level}`}>{result.risk_level} RISK</span>
              <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 8, lineHeight: 1.5 }}>
                {result.explanation}
              </p>
            </div>
          </div>

          <p style={{ fontSize: 13, marginTop: 14, fontWeight: 600 }}>Recommended action</p>
          <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 4 }}>{result.recommendation}</p>

          <p style={{ fontSize: 13, marginTop: 16, fontWeight: 600 }}>Contributing factors</p>
          <div style={{ marginTop: 6 }}>
            {result.factors.map((f) => (
              <div className="factor-row" key={f.name}>
                <span>{f.name}</span>
                <span>{f.value}</span>
                <span className={`badge badge-${f.impact === 'HIGH' ? 'CRITICAL' : f.impact === 'MEDIUM' ? 'MEDIUM' : 'LOW'}`}>
                  {f.impact}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
