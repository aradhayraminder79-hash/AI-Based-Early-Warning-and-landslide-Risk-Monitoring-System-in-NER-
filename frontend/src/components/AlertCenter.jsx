import React, { useEffect, useState } from 'react'
import { getAlerts } from '../services/api.js'

const DOT_COLOR = {
  LOW: 'var(--teal)',
  MEDIUM: 'var(--amber)',
  HIGH: 'var(--orange)',
  CRITICAL: 'var(--red)',
}

export default function AlertCenter({ expanded }) {
  const [alerts, setAlerts] = useState([])
  const [notice, setNotice] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const loadAlerts = async () => {
    try {
      setLoading(true)
      setError(null)

      const res = await getAlerts()

      console.log('Alert API response:', res)

      const alertList = Array.isArray(res?.alerts)
        ? res.alerts
        : Array.isArray(res)
          ? res
          : []

      setAlerts(alertList)
      setNotice(res?.data_notice || '')
    } catch (err) {
      console.error('Alert loading error:', err)
      setError(err?.message || 'Unable to load alerts')
      setAlerts([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadAlerts()

    const interval = setInterval(loadAlerts, 60 * 1000)

    return () => clearInterval(interval)
  }, [])

  const visible = expanded ? alerts : alerts.slice(0, 5)

  return (
    <div className="card">
      <div className="section-title">
        <h2>Alert Center</h2>
        <span>{alerts.length} active</span>
      </div>

      {notice && (
        <div
          className="banner banner--notice"
          style={{ marginBottom: 12 }}
        >
          {notice}
        </div>
      )}

      {loading && (
        <p style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
          Loading alerts...
        </p>
      )}

      {error && (
        <div className="banner banner--error">
          Alert service error: {error}
        </div>
      )}

      {!loading && !error && visible.map((a, index) => {
        const severity = String(a.severity || 'LOW').toUpperCase()

        return (
          <div
            className="alert-item"
            key={a.id || `${a.zone_id || 'alert'}-${index}`}
          >
            <span
              className="alert-dot"
              style={{
                background: DOT_COLOR[severity] || 'var(--teal)',
              }}
            />

            <div>
              <div className="alert-message">
                <span
                  className={`badge badge-${severity}`}
                  style={{ marginRight: 8 }}
                >
                  {severity}
                </span>

                {a.message || 'Risk alert detected.'}
              </div>

              <div className="alert-meta">
                {a.zone_name || 'Unknown zone'}
                {a.state ? `, ${a.state}` : ''}
                {' · '}

                {a.timestamp
                  ? new Date(a.timestamp).toLocaleString('en-IN', {
                      dateStyle: 'medium',
                      timeStyle: 'short',
                    })
                  : 'Time unavailable'}
              </div>
            </div>
          </div>
        )
      })}

      {!loading && !error && alerts.length === 0 && (
        <p style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
          No alerts at this time.
        </p>
      )}
    </div>
  )
}
