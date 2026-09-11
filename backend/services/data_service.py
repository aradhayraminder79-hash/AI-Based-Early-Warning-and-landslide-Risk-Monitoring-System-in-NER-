"""
Data service for the AI Landslide Early Warning System.

Weather:
    Live Open-Meteo weather/rainfall data.

Other risk factors:
    Soil moisture, slope, elevation and historical events remain
    prototype/demo values until real datasets or sensors are connected.
"""

from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

import requests


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

DEMO_DATA_NOTICE = (
    "Weather: LIVE Open-Meteo data. "
    "Soil moisture, terrain and historical landslide datasets remain prototype/demo data."
)


# ---------------------------------------------------------------------
# Monitored zones
# ---------------------------------------------------------------------

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


# ---------------------------------------------------------------------
# Weather helpers
# ---------------------------------------------------------------------

def weather_description(code):
    """Convert WMO weather code into a readable description."""
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Freezing rain",
        67: "Heavy freezing rain",
        71: "Light snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Light rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail",
    }

    return descriptions.get(int(code), "Unknown")


def fetch_weather_for_zone(z):
    """Fetch current weather and previous 24 hours of precipitation."""

    params = {
        "latitude": z["lat"],
        "longitude": z["lon"],
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "wind_speed_10m,"
            "weather_code"
        ),
        "hourly": "precipitation",
        "past_hours": 24,
        "forecast_hours": 1,
        "timezone": "auto",
    }

    try:
        response = requests.get(
            OPEN_METEO_URL,
            params=params,
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

        current = data.get("current", {})
        hourly = data.get("hourly", {})

        rainfall_values = hourly.get("precipitation", [])

        rainfall_24h = round(
            sum(
                float(v)
                for v in rainfall_values
                if v is not None
            ),
            1,
        )

        return {
            "zone_id": z["id"],
            "zone_name": z["name"],
            "temperature_c": round(
                float(current.get("temperature_2m", 0)), 1
            ),
            "humidity_pct": round(
                float(current.get("relative_humidity_2m", 0))
            ),
            "rainfall_24h_mm": rainfall_24h,
            "wind_kmh": round(
                float(current.get("wind_speed_10m", 0)), 1
            ),
            "forecast": weather_description(
                current.get("weather_code", 0)
            ),
            "updated_at": current.get("time"),
            "source": "Open-Meteo",
            "live": True,
        }

    except Exception as exc:
        print(
            f"Weather request failed for {z['name']}: {exc}"
        )

        return {
            "zone_id": z["id"],
            "zone_name": z["name"],
            "temperature_c": None,
            "humidity_pct": None,
            "rainfall_24h_mm": z["rainfall_24h"],
            "wind_kmh": None,
            "forecast": "Weather service unavailable",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "source": "Fallback",
            "live": False,
            "error": str(exc),
        }

def get_demo_weather(zone_id: str = None):
    """
    Kept with the old function name so the existing frontend/backend
    architecture continues working.

    Despite the legacy name, weather data is now fetched from Open-Meteo.
    """

    zones = (
        ZONES
        if zone_id is None
        else [z for z in ZONES if z["id"] == zone_id]
    )

    if not zones:
        return []

    weather = []

    # Fetch multiple zones concurrently so /weather and /zones stay fast.
    with ThreadPoolExecutor(max_workers=min(6, len(zones))) as executor:
        futures = {
            executor.submit(fetch_weather_for_zone, z): z
            for z in zones
        }

        for future in as_completed(futures):
            weather.append(future.result())

    # Preserve original zone order.
    order = {z["id"]: i for i, z in enumerate(zones)}
    weather.sort(key=lambda item: order[item["zone_id"]])

    return weather


# ---------------------------------------------------------------------
# IMPORTANT:
# Live rainfall is now injected into the ML input.
# ---------------------------------------------------------------------

def get_zones_raw():
    """
    Return zone data with current Open-Meteo rainfall.

    Soil moisture, slope, elevation and historical events remain the
    existing prototype values.
    """

    zones = [dict(z) for z in ZONES]

    live_weather = get_demo_weather()

    weather_by_zone = {
        w["zone_id"]: w
        for w in live_weather
    }

    for zone in zones:
        weather = weather_by_zone.get(zone["id"])

        if weather and weather.get("live"):
            # THIS is the important connection:
            # Open-Meteo rainfall -> ML rainfall_24h feature.
            zone["rainfall_24h"] = weather["rainfall_24h_mm"]
            zone["weather_live"] = True
            zone["weather_source"] = "Open-Meteo"
        else:
            # Safe fallback if the weather API is temporarily unavailable.
            zone["weather_live"] = False
            zone["weather_source"] = "Fallback"

    return zones


# ---------------------------------------------------------------------
# Historical chart data
# ---------------------------------------------------------------------

def get_historical_series(zone_id: str, days: int = 14):
    """
    Synthetic historical risk series for the chart.

    Real deployment should replace this with stored prediction history.
    """

    now = datetime.utcnow()
    series = []

    base = random.uniform(20, 55)

    for i in range(days, 0, -1):
        date = now - timedelta(days=i)

        drift = random.uniform(-8, 8)
        base = max(5, min(95, base + drift))

        series.append({
            "date": date.strftime("%Y-%m-%d"),
            "probability": round(base, 1),
        })

    return series



