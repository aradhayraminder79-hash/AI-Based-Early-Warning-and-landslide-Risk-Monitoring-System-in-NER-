import React, { useEffect, useState, useCallback } from 'react'

import Header from './components/Header.jsx'
import Sidebar from './components/Sidebar.jsx'
import DashboardOverview from './components/DashboardOverview.jsx'
import SummaryCards from './components/SummaryCards.jsx'
import PredictionPanel from './components/PredictionPanel.jsx'
import EnvironmentalConditions from './components/EnvironmentalConditions.jsx'
import RiskMap from './components/RiskMap.jsx'
import AlertCenter from './components/AlertCenter.jsx'
import WeatherPanel from './components/WeatherPanel.jsx'
import HistoricalChart from './components/HistoricalChart.jsx'
import SystemStatus from './components/SystemStatus.jsx'
import AboutSystem from './components/AboutSystem.jsx'

import { getZones, getHealth, getAlerts } from './services/api.js'

import './App.css'

const SECTIONS = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'monitoring', label: 'Risk Monitoring' },
  { id: 'map', label: 'Risk Map' },
  { id: 'alerts', label: 'Alerts' },
  { id: 'weather', label: 'Weather' },
  { id: 'history', label: 'Historical Data' },
  { id: 'predict', label: 'AI Prediction' },
  { id: 'about', label: 'About System' },
]

export default function App() {
  const [activeSection, setActiveSection] = useState('dashboard')

  const [zones, setZones] = useState([])
  const [alerts, setAlerts] = useState([])
  const [health, setHealth] = useState(null)

  const [selectedZoneId, setSelectedZoneId] = useState(null)
  const [apiOnline, setApiOnline] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const loadData = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const healthRes = await getHealth()
      setHealth(healthRes)
      setApiOnline(true)

      const zonesRes = await getZones()
      const zoneList = Array.isArray(zonesRes?.zones)
        ? zonesRes.zones
        : []

      setZones(zoneList)

      if (zoneList.length > 0) {
        setSelectedZoneId((current) => current || zoneList[0].id)
      }

      try {
        const alertsRes = await getAlerts()

        const alertList = Array.isArray(alertsRes?.alerts)
          ? alertsRes.alerts
          : Array.isArray(alertsRes)
            ? alertsRes
            : []

        setAlerts(alertList)
      } catch (alertError) {
        console.error('Alert loading error:', alertError)
        setAlerts([])
      }

    } catch (err) {
      console.error('Dashboard loading error:', err)
      setApiOnline(false)
      setError(err?.message || 'Unable to connect to backend')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadData()

    const interval = setInterval(loadData, 60000)

    return () => clearInterval(interval)
  }, [loadData])

  const selectedZone =
    zones.find((z) => z.id === selectedZoneId) || null

  return (
    <div className="app-shell">

      <Header
        apiOnline={apiOnline}
        onMenuToggle={() => setSidebarOpen((s) => !s)}
      />

      <div className="app-body">

        <Sidebar
          sections={SECTIONS}
          active={activeSection}
          onSelect={(id) => {
            setActiveSection(id)
            setSidebarOpen(false)
          }}
          open={sidebarOpen}
        />

        <main className="app-main">

          {error && (
            <div className="banner banner--error">
              Could not reach the backend API. Make sure the FastAPI
              server is running on port 8000. Details: {error}
            </div>
          )}

          {activeSection === 'dashboard' && (
            <>
              <DashboardOverview
                zones={zones}
                alerts={alerts}
                health={health}
              />

              <div className="grid-2" style={{ marginTop: 18 }}>
                <PredictionPanel onPredicted={loadData} />

                <EnvironmentalConditions
                  zone={selectedZone}
                  zones={zones}
                  onSelectZone={setSelectedZoneId}
                />
              </div>

              <RiskMap
                zones={zones}
                selectedZoneId={selectedZoneId}
                onSelectZone={setSelectedZoneId}
              />

              <div className="grid-2">

                <AlertCenter />

                <WeatherPanel zones={zones} />

              </div>

              <HistoricalChart
                zones={zones}
                selectedZoneId={selectedZoneId}
                onSelectZone={setSelectedZoneId}
              />

              <SystemStatus apiOnline={apiOnline} />
            </>
          )}

          {activeSection === 'monitoring' && (
            <>
              <SummaryCards
                zones={zones}
                loading={loading}
              />

              <EnvironmentalConditions
                zone={selectedZone}
                zones={zones}
                onSelectZone={setSelectedZoneId}
                expanded
              />
            </>
          )}

          {activeSection === 'map' && (
            <RiskMap
              zones={zones}
              selectedZoneId={selectedZoneId}
              onSelectZone={setSelectedZoneId}
              expanded
            />
          )}

          {activeSection === 'alerts' && (
            <AlertCenter expanded />
          )}

          {activeSection === 'weather' && (
            <WeatherPanel
              zones={zones}
              expanded
            />
          )}

          {activeSection === 'history' && (
            <HistoricalChart
              zones={zones}
              selectedZoneId={selectedZoneId}
              onSelectZone={setSelectedZoneId}
              expanded
            />
          )}

          {activeSection === 'predict' && (
            <PredictionPanel
              onPredicted={loadData}
              expanded
            />
          )}

          {activeSection === 'about' && (
            <AboutSystem />
          )}

        </main>
      </div>
    </div>
  )
}
