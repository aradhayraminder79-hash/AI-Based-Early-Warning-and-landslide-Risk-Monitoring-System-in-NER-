"""
Alert engine.

Given a zone's predicted risk, generate a structured alert. In a real
deployment this would be triggered by a scheduled prediction job and
persisted to a database / pushed via SMS or push notifications. Here it
is computed on-demand from the current demo zone data for the /alerts
endpoint.
"""

from datetime import datetime, timedelta
import random

ALERT_MESSAGES = {
    "CRITICAL": "Heavy rainfall and soil saturation detected in {zone}. Immediate monitoring and evacuation readiness required.",
    "HIGH": "Landslide probability has increased in {zone}. Prepare warning notices and monitor closely.",
    "MEDIUM": "Environmental conditions in {zone} require increased monitoring over the next 24 hours.",
    "LOW": "No immediate threat detected in {zone}. Routine monitoring continues.",
}


def build_alert(zone: dict, probability: float, risk_level: str, index: int = 0) -> dict:
    now = datetime.utcnow() - timedelta(minutes=random.randint(1, 240))
    return {
        "id": f"alert-{zone['id']}-{index}",
        "zone_id": zone["id"],
        "zone_name": zone["name"],
        "state": zone["state"],
        "severity": risk_level,
        "probability": probability,
        "message": ALERT_MESSAGES[risk_level].format(zone=zone["name"]),
        "timestamp": now.isoformat() + "Z",
    }


def build_alerts(zone_predictions: list) -> list:
    """zone_predictions: list of dicts with keys zone (raw zone dict),
    probability, risk_level. Returns alerts sorted by severity (CRITICAL first),
    then most recent."""
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    alerts = [
        build_alert(zp["zone"], zp["probability"], zp["risk_level"], i)
        for i, zp in enumerate(zone_predictions)
    ]
    alerts.sort(key=lambda a: severity_order.get(a["severity"], 4))
    return alerts
