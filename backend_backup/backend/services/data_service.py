"""
Demo data service.

IMPORTANT: All location, weather and historical data returned from this
module is DEMO / SYNTHETIC data generated for the purpose of a college
project demonstration. None of it is sourced from a live sensor network,
live satellite feed, or live weather API. See README.md for notes on
wiring up real data sources (IMD weather API, Bhuvan/ISRO landslide
susceptibility layers, IoT soil-moisture sensors, etc.).
"""

from datetime import datetime, timedelta
import random

DEMO_DATA_NOTICE = "DEMO DATA — for demonstration purposes only. Not live sensor/satellite data."

# Sample monitored locations across the North Eastern Region of India.
# Coordinates are approximate town/village centers used for demo mapping.
ZONES = [
    {"id": "z1", "name": "Sohra (Cherrapunji)", "state": "Meghalaya", "lat": 25.2702, "lon": 91.7323,
     "rainfall_24h": 182, "soil_moisture": 78, "slope": 38, "elevation": 1484, "historical_events": 4},
    {"id": "z2", "name": "Mawsynram", "state": "Meghalaya", "lat": 25.2989, "lon": 91.5822,
     "rainfall_24h": 165, "soil_moisture": 74, "slope": 33, "elevation": 1400, "historical_events": 3},
    {"id": "z3", "name": "Gangtok", "state": "Sikkim", "lat": 27.3389, "lon": 88.6065,
     "rainfall_24h": 96, "soil_moisture": 58, "slope": 29, "elevation": 1650, "historical_events": 2},
    {"id": "z4", "name": "Mangan", "state": "Sikkim", "lat": 27.5117, "lon": 88.5311,
     "rainfall_24h": 110, "soil_moisture": 62, "slope": 41, "elevation": 1900, "historical_events": 3},
    {"id": "z5", "name": "Itanagar", "state": "Arunachal Pradesh", "lat": 27.0844, "lon": 93.6053,
     "rainfall_24h": 58, "soil_moisture": 40, "slope": 18, "elevation": 350, "historical_events": 0},
    {"id": "z6", "name": "Bomdila", "state": "Arunachal Pradesh", "lat": 27.2649, "lon": 92.4159,
     "rainfall_24h": 88, "soil_moisture": 50, "slope": 27, "elevation": 2415, "historical_events": 1},
    {"id": "z7", "name": "Aizawl", "state": "Mizoram", "lat": 23.7271, "lon": 92.7176,
     "rainfall_24h": 142, "soil_moisture": 70, "slope": 36, "elevation": 1132, "historical_events": 3},
    {"id": "z8", "name": "Lunglei", "state": "Mizoram", "lat": 22.8878, "lon": 92.7320,
     "rainfall_24h": 75, "soil_moisture": 48, "slope": 24, "elevation": 1100, "historical_events": 1},
    {"id": "z9", "name": "Kohima", "state": "Nagaland", "lat": 25.6751, "lon": 94.1086,
     "rainfall_24h": 64, "soil_moisture": 44, "slope": 22, "elevation": 1444, "historical_events": 1},
    {"id": "z10", "name": "Imphal", "state": "Manipur", "lat": 24.8170, "lon": 93.9368,
     "rainfall_24h": 40, "soil_moisture": 33, "slope": 12, "elevation": 786, "historical_events": 0},
    {"id": "z11", "name": "Agartala", "state": "Tripura", "lat": 23.8315, "lon": 91.2868,
     "rainfall_24h": 35, "soil_moisture": 30, "slope": 9, "elevation": 46, "historical_events": 0},
    {"id": "z12", "name": "Haflong", "state": "Assam", "lat": 25.1667, "lon": 93.0167,
     "rainfall_24h": 128, "soil_moisture": 66, "slope": 31, "elevation": 680, "historical_events": 2},
]


def get_zones_raw():
    """Return the raw demo zone data (without ML predictions attached)."""
    return ZONES


def get_demo_weather(zone_id: str = None):
    """Return demo weather data. Clearly marked as demo, architected so a
    real weather API (e.g. IMD, OpenWeatherMap) can be swapped in later by
    replacing the body of this function.
    """
    zones = ZONES if zone_id is None else [z for z in ZONES if z["id"] == zone_id]
    now = datetime.utcnow()
    weather = []
    for z in zones:
        weather.append({
            "zone_id": z["id"],
            "zone_name": z["name"],
            "temperature_c": round(random.uniform(14, 26), 1),
            "humidity_pct": round(random.uniform(55, 95), 1),
            "rainfall_24h_mm": z["rainfall_24h"],
            "wind_kmh": round(random.uniform(5, 25), 1),
            "forecast": random.choice(["Heavy rain expected", "Intermittent showers", "Partly cloudy", "Clear skies"]),
            "updated_at": now.isoformat() + "Z",
            "source": "DEMO",
        })
    return weather


def get_historical_series(zone_id: str, days: int = 14):
    """Return a synthetic time series of risk probability for charting.
    Real deployment would replace this with a query against a stored
    prediction history table (e.g. in Postgres/SQLite)."""
    now = datetime.utcnow()
    series = []
    base = random.uniform(20, 55)
    for i in range(days, 0, -1):
        date = now - timedelta(days=i)
        drift = random.uniform(-8, 8)
        base = max(5, min(95, base + drift))
        series.append({"date": date.strftime("%Y-%m-%d"), "probability": round(base, 1)})
    return series
