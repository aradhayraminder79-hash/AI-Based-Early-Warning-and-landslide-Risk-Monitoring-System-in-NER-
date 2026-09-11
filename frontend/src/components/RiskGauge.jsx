import React from 'react'

const RISK_COLORS = {
  LOW: 'var(--teal)',
  MEDIUM: 'var(--amber)',
  HIGH: 'var(--orange)',
  CRITICAL: 'var(--red)',
}

export default function RiskGauge({ probability, riskLevel, size = 108 }) {
  const radius = (size - 12) / 2
  const circumference = 2 * Math.PI * radius
  const pct = Math.max(0, Math.min(100, probability)) / 100
  const offset = circumference * (1 - pct)
  const color = RISK_COLORS[riskLevel] || 'var(--teal)'

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke="var(--border-soft)"
        strokeWidth="10"
      />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke={color}
        strokeWidth="10"
        strokeLinecap="round"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
        style={{ transition: 'stroke-dashoffset 0.6s ease' }}
      />
      <text
        x="50%"
        y="50%"
        textAnchor="middle"
        dominantBaseline="central"
        fill="var(--text-primary)"
        fontFamily="var(--font-display)"
        fontSize={size * 0.22}
        fontWeight="700"
      >
        {Math.round(probability)}%
      </text>
    </svg>
  )
}
