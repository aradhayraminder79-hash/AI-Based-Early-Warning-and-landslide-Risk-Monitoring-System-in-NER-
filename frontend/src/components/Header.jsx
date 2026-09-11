import React, { useEffect, useState } from 'react'

export default function Header({ apiOnline, onMenuToggle }) {
  const [now, setNow] = useState(new Date())

  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 1000)
    return () => clearInterval(t)
  }, [])

  return (
    <header className="header">
      <div className="header-left">
        <button className="header-menu-btn" onClick={onMenuToggle} aria-label="Toggle menu">☰</button>
        <div className="header-logo">EW</div>
        <div className="header-titles">
          <h1>AI Landslide Early Warning System</h1>
          <p>North Eastern Region, India</p>
        </div>
      </div>
      <div className="header-right">
        <span className="header-clock">{now.toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'medium' })}</span>
        <span className="status-pill">
          <span className={`status-dot ${apiOnline === true ? 'status-dot--online' : apiOnline === false ? 'status-dot--offline' : ''}`} />
          {apiOnline === true ? 'System Online' : apiOnline === false ? 'Backend Offline' : 'Connecting...'}
        </span>
      </div>
    </header>
  )
}
