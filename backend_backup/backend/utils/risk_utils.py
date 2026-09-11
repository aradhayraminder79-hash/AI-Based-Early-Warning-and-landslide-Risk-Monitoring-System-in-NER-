"""
Utility functions for converting a raw ML probability into a
human-readable risk level, explanation text and recommended action.

These thresholds are used consistently across the whole backend
(prediction endpoint, alert engine, zone summaries) so the frontend
never has to re-derive risk levels itself.
"""

from typing import List, Dict


# Risk thresholds (probability is expressed as 0-100)
RISK_THRESHOLDS = [
    (0, 30, "LOW"),
    (31, 60, "MEDIUM"),
    (61, 80, "HIGH"),
    (81, 100, "CRITICAL"),
]


def classify_risk(probability: float) -> str:
    """Map a probability (0-100) to a risk level string."""
    probability = max(0.0, min(100.0, probability))
    for low, high, label in RISK_THRESHOLDS:
        if low <= probability <= high:
            return label
    return "CRITICAL"


def get_recommendation(risk_level: str) -> str:
    recommendations = {
        "LOW": "No immediate threat detected. Continue routine monitoring of the zone.",
        "MEDIUM": "Increased monitoring recommended. Field teams should inspect drainage and slope conditions.",
        "HIGH": "Prepare warning notices and monitor the zone closely over the next 24-48 hours.",
        "CRITICAL": "Immediate attention required. Consider evacuation advisories and alert local disaster management authorities.",
    }
    return recommendations.get(risk_level, "Monitor the zone as per standard protocol.")


def get_risk_explanation(risk_level: str, probability: float) -> str:
    explanations = {
        "LOW": f"Predicted landslide probability is {probability:.1f}%, which falls within the safe operating range based on current rainfall, soil moisture and terrain inputs.",
        "MEDIUM": f"Predicted landslide probability is {probability:.1f}%. Environmental conditions are trending upward and warrant closer observation.",
        "HIGH": f"Predicted landslide probability is {probability:.1f}%. Multiple risk factors (rainfall, soil saturation, slope) are compounding in this zone.",
        "CRITICAL": f"Predicted landslide probability is {probability:.1f}%. Conditions closely resemble historical pre-landslide patterns for this terrain profile.",
    }
    return explanations.get(risk_level, "")


def build_factors(rainfall_24h: float, soil_moisture: float, slope: float,
                   elevation: float, historical_events: int) -> List[Dict]:
    """Return a breakdown of contributing factors with simple qualitative flags.
    This is a rule-of-thumb explanation layer on top of the ML model, not a
    substitute for the model's own feature importances.
    """
    factors = []

    factors.append({
        "name": "Rainfall (24h)",
        "value": f"{rainfall_24h} mm",
        "impact": "HIGH" if rainfall_24h > 150 else "MEDIUM" if rainfall_24h > 80 else "LOW",
    })
    factors.append({
        "name": "Soil Moisture",
        "value": f"{soil_moisture}%",
        "impact": "HIGH" if soil_moisture > 70 else "MEDIUM" if soil_moisture > 45 else "LOW",
    })
    factors.append({
        "name": "Slope",
        "value": f"{slope}\u00b0",
        "impact": "HIGH" if slope > 35 else "MEDIUM" if slope > 20 else "LOW",
    })
    factors.append({
        "name": "Elevation",
        "value": f"{elevation} m",
        "impact": "MEDIUM" if elevation > 1200 else "LOW",
    })
    factors.append({
        "name": "Historical Events",
        "value": str(historical_events),
        "impact": "HIGH" if historical_events >= 3 else "MEDIUM" if historical_events >= 1 else "LOW",
    })

    return factors
