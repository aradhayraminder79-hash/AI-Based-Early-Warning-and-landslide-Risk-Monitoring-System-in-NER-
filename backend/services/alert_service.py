"""
Data-driven landslide alert engine.

Alerts are generated from the latest ML prediction for each monitored zone.
They are NOT official government emergency warnings.
"""

from datetime import datetime, timezone


ALERT_MESSAGES = {
    "CRITICAL": "Current model assessment: CRITICAL landslide risk detected in {zone}. Immediate monitoring and evacuation readiness recommended.",
    "HIGH": "Current model assessment: HIGH landslide risk detected in {zone}. Prepare warning notices and monitor closely.",
    "MEDIUM": "Current model assessment: MEDIUM landslide risk detected in {zone}. Increased monitoring is recommended.",
    "LOW": "Current model assessment: LOW landslide risk in {zone}. Routine monitoring continues.",
}


def build_alert(zone: dict, probability: float, risk_level: str, index: int = 0) -> dict:
    now = datetime.now(timezone.utc)

    return {
        "id": f"alert-{zone['id']}-{index}",
        "zone_id": zone["id"],
        "zone_name": zone["name"],
        "state": zone["state"],
        "severity": risk_level,
        "probability": round(float(probability), 1),
        "message": ALERT_MESSAGES[risk_level].format(zone=zone["name"]),
        "timestamp": now.isoformat().replace("+00:00", "Z"),
        "source": "AI risk assessment",
        "official_warning": False,
    }


def build_alerts(zone_predictions: list) -> list:
    """
    Build alerts from the latest ML predictions.

    These are system-generated risk assessments, not official
    government emergency warnings.
    """

    severity_order = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
    }

    alerts = [
        build_alert(
            zp["zone"],
            zp["probability"],
            zp["risk_level"],
            i
        )
        for i, zp in enumerate(zone_predictions)
    ]

    alerts.sort(
        key=lambda a: (
            severity_order.get(a["severity"], 4),
            -a["probability"],
        )
    )

    return alerts
