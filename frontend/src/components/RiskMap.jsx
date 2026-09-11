import React from 'react'
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet'

const RISK_COLORS = {
  LOW: '#2ec4b6',
  MEDIUM: '#f4a300',
  HIGH: '#ff6b35',
  CRITICAL: '#e63946',
}

function FlyToZone({ zone }) {
  const map = useMap()
  React.useEffect(() => {
    if (zone) map.flyTo([zone.lat, zone.lon], 7, { duration: 0.6 })
  }, [zone, map])
  return null
}

export default function RiskMap({ zones, selectedZoneId, onSelectZone, expanded }) {
  const center = zones.length > 0 ? [25.5, 92.5] : [26, 93]
  const selectedZone = zones.find((z) => z.id === selectedZoneId)

  return (
    <div className="card">
      <div className="section-title">
        <h2>Interactive Risk Map</h2>
        <span>Sample monitored locations â€” North Eastern Region</span>
      </div>
      <div className={`map-container ${expanded ? 'map-container--expanded' : ''}`}>
        <MapContainer center={center} zoom={6} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
          />
          {zones.map((z) => (
            <CircleMarker
              key={z.id}
              center={[z.lat, z.lon]}
              radius={z.id === selectedZoneId ? 12 : 9}
              pathOptions={{
                color: RISK_COLORS[z.risk_level] || '#2ec4b6',
                fillColor: RISK_COLORS[z.risk_level] || '#2ec4b6',
                fillOpacity: 0.75,
                weight: z.id === selectedZoneId ? 3 : 1,
              }}
              eventHandlers={{ click: () => onSelectZone(z.id) }}
            >
              <Popup>
                <div className="popup-title">{z.name}, {z.state}</div>
                <div className="popup-row">Risk level: {z.risk_level} ({z.probability}%)</div>
                <div className="popup-row">Rainfall (24h): {z.rainfall_24h} mm</div>
                <div className="popup-row">Soil moisture: {z.soil_moisture}%</div>
                <div className="popup-row">Lat/Lon: {z.lat.toFixed(3)}, {z.lon.toFixed(3)}</div>
              </Popup>
            </CircleMarker>
          ))}
          <FlyToZone zone={selectedZone} />
        </MapContainer>
      </div>
      <div style={{ display: 'flex', gap: 16, marginTop: 12, flexWrap: 'wrap' }}>
        {Object.entries(RISK_COLORS).map(([level, color]) => (
          <span key={level} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12, color: 'var(--text-secondary)' }}>
            <span style={{ width: 9, height: 9, borderRadius: '50%', background: color, display: 'inline-block' }} />
            {level}
          </span>
        ))}
      </div>
    </div>
  )
}

