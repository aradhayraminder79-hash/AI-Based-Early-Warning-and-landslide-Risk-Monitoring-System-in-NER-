import React, { useEffect, useState } from 'react'
import { getWeather } from '../services/api.js'

export default function WeatherPanel({ expanded }) {
  const [weather, setWeather] = useState([])
  const [notice, setNotice] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const loadWeather = async () => {
    try {
      setLoading(true)
      setError(null)

      const res = await getWeather()

      setWeather(res.weather || [])
      setNotice(res.data_notice || '')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadWeather()

    // Refresh live weather every 10 minutes
    const interval = setInterval(loadWeather, 10 * 60 * 1000)

    return () => clearInterval(interval)
  }, [])

  const visible = expanded ? weather : weather.slice(0, 4)

  return (
    <div className="card">
      <div className="section-title">
        <h2>Weather Panel</h2>
        <span style={{ color: '#22C55E', fontWeight: 600 }}>
          ● LIVE WEATHER
        </span>
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
          Loading live weather data...
        </p>
      )}

      {error && (
        <div className="banner banner--error">
          Weather service error: {error}
        </div>
      )}

      {!loading && !error && (
        <div className="weather-grid">
          {visible.map((w) => (
            <div className="weather-card" key={w.zone_id}>
              <h4>{w.zone_name}</h4>

              <div className="weather-row">
                <span>Temperature</span>
                <span>{w.temperature_c ?? '—'}°C</span>
              </div>

              <div className="weather-row">
                <span>Humidity</span>
                <span>{w.humidity_pct ?? '—'}%</span>
              </div>

              <div className="weather-row">
                <span>Rainfall (24h)</span>
                <span>{w.rainfall_24h_mm ?? '—'} mm</span>
              </div>

              <div className="weather-row">
                <span>Wind</span>
                <span>{w.wind_kmh ?? '—'} km/h</span>
              </div>

              <div className="weather-row">
                <span>Outlook</span>
                <span>{w.forecast ?? '—'}</span>
              </div>

              <div className="weather-row">
                <span>Source</span>
                <span>{w.source ?? '—'}</span>
              </div>

              <div
                style={{
                  marginTop: 8,
                  fontSize: 11,
                  color: 'var(--text-secondary)'
                }}
              >
                Updated: {w.updated_at ?? '—'}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
