const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

async function handleResponse(res) {
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`API error ${res.status}: ${text}`)
  }
  return res.json()
}

export async function getHealth() {
  const res = await fetch(`${API_BASE}/health`)
  return handleResponse(res)
}

export async function getZones() {
  const res = await fetch(`${API_BASE}/zones`)
  return handleResponse(res)
}

export async function postPredict(payload) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  return handleResponse(res)
}

export async function getAlerts() {
  const res = await fetch(`${API_BASE}/alerts`)
  return handleResponse(res)
}

export async function getWeather(zoneId) {
  const url = zoneId ? `${API_BASE}/weather?zone_id=${zoneId}` : `${API_BASE}/weather`
  const res = await fetch(url)
  return handleResponse(res)
}

export async function getHistory(zoneId, days = 14) {
  const res = await fetch(`${API_BASE}/history/${zoneId}?days=${days}`)
  return handleResponse(res)
}

export { API_BASE }
