import React from 'react'

export default function AboutSystem() {
  return (
    <div className="card" style={{ maxWidth: 720 }}>
      <div className="section-title">
        <h2>About This System</h2>
      </div>
      <p style={{ fontSize: 13.5, color: 'var(--text-secondary)', lineHeight: 1.6 }}>
        This is a college-project prototype of an AI-based landslide risk monitoring and early
        warning portal for the North Eastern Region of India. It combines rainfall, soil moisture,
        slope, elevation and historical landslide event data through a Random Forest classifier to
        estimate a landslide probability and risk level for a given zone.
      </p>
      <ul className="about-list">
        <li><strong>Backend:</strong> FastAPI + scikit-learn Random Forest model, served as a REST API.</li>
        <li><strong>Frontend:</strong> React + Vite, with an interactive Leaflet map and Recharts visualizations.</li>
        <li><strong>Data:</strong> Zone locations, weather readings and historical charts in this build are DEMO / SYNTHETIC data intended purely for demonstration.</li>
        <li><strong>Path to production:</strong> swap the demo data service for real feeds — IMD rainfall data, satellite/in-situ soil-moisture sensors, a DEM-derived slope/elevation layer, and a verified historical landslide inventory — then retrain the model on real labelled data.</li>
      </ul>
    </div>
  )
}
