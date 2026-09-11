import React from 'react'

const ICONS = {
  dashboard: '◱',
  monitoring: '◈',
  map: '⬢',
  alerts: '⚠',
  weather: '☁',
  history: '≣',
  predict: '✦',
  about: 'ⓘ',
}

export default function Sidebar({ sections, active, onSelect, open }) {
  return (
    <nav className={`sidebar ${open ? 'sidebar--open' : ''}`}>
      {sections.map((s) => (
        <button
          key={s.id}
          className={`sidebar-item ${active === s.id ? 'sidebar-item--active' : ''}`}
          onClick={() => onSelect(s.id)}
        >
          <span className="sidebar-icon">{ICONS[s.id]}</span>
          {s.label}
        </button>
      ))}
    </nav>
  )
}
