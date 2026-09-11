"""
FastAPI backend for the AI Landslide Early Warning System.

Run with:
    uvicorn app:app --reload --port 8000

Requires a trained model at backend/model/risk_model.joblib — run
`python train_model.py` first.
"""

import os
from datetime import datetime

import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from services.data_service import (
    get_zones_raw, get_demo_weather, get_historical_series, DEMO_DATA_NOTICE,
)
from services.alert_service import build_alerts
from utils.risk_utils import classify_risk, get_recommendation, get_risk_explanation, build_factors

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "risk_model.joblib")

app = FastAPI(
    title="AI Landslide Early Warning System API",
    description="Backend API for AI-based landslide risk monitoring in the North Eastern Region, India. "
                 "Location, weather and historical data served by this API is DEMO DATA for a college project.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------
_model_bundle = None
_model_load_error = None

def load_model():
    global _model_bundle, _model_load_error
    try:
        _model_bundle = joblib.load(MODEL_PATH)
        _model_load_error = None
    except Exception as exc:  # noqa: BLE001
        _model_bundle = None
        _model_load_error = str(exc)

load_model()


# ---------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------
class PredictRequest(BaseModel):
    rainfall_24h: float = Field(..., ge=0, le=1000, description="Rainfall in last 24h (mm)")
    soil_moisture: float = Field(..., ge=0, le=100, description="Soil moisture (%)")
    slope: float = Field(..., ge=0, le=90, description="Slope angle (degrees)")
    elevation: float = Field(..., ge=0, le=9000, description="Elevation (meters)")
    historical_events: int = Field(..., ge=0, le=50, description="Historical landslide event count")


class PredictResponse(BaseModel):
    probability: float
    risk_level: str
    recommendation: str
    explanation: str
    factors: list


# ---------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------
def run_prediction(rainfall_24h, soil_moisture, slope, elevation, historical_events):
    if _model_bundle is None:
        raise HTTPException(
            status_code=503,
            detail=f"ML model not loaded. Run train_model.py first. ({_model_load_error})",
        )
    model = _model_bundle["model"]
    feature_cols = _model_bundle["feature_cols"]
    import pandas as pd
    X = pd.DataFrame([{
        "rainfall_24h": rainfall_24h,
        "soil_moisture": soil_moisture,
        "slope": slope,
        "elevation": elevation,
        "historical_events": historical_events,
    }])[feature_cols]
    proba = model.predict_proba(X)[0][1] * 100
    risk_level = classify_risk(proba)
    return round(proba, 1), risk_level


# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "service": "AI Landslide Early Warning System API",
        "status": "online",
        "model_loaded": _model_bundle is not None,
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "ok" if _model_bundle is not None else "degraded",
        "model_loaded": _model_bundle is not None,
        "model_error": _model_load_error,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/zones")
def zones():
    """Return all monitored zones with a live risk prediction attached to each."""
    raw_zones = get_zones_raw()
    result = []
    for z in raw_zones:
        if _model_bundle is not None:
            proba, risk_level = run_prediction(
                z["rainfall_24h"], z["soil_moisture"], z["slope"], z["elevation"], z["historical_events"]
            )
        else:
            proba, risk_level = 0.0, "LOW"
        result.append({**z, "probability": proba, "risk_level": risk_level})
    return {"data_notice": DEMO_DATA_NOTICE, "zones": result}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    proba, risk_level = run_prediction(
        req.rainfall_24h, req.soil_moisture, req.slope, req.elevation, req.historical_events
    )
    return PredictResponse(
        probability=proba,
        risk_level=risk_level,
        recommendation=get_recommendation(risk_level),
        explanation=get_risk_explanation(risk_level, proba),
        factors=build_factors(req.rainfall_24h, req.soil_moisture, req.slope, req.elevation, req.historical_events),
    )


@app.get("/alerts")
def alerts():
    raw_zones = get_zones_raw()
    zone_predictions = []
    for z in raw_zones:
        if _model_bundle is not None:
            proba, risk_level = run_prediction(
                z["rainfall_24h"], z["soil_moisture"], z["slope"], z["elevation"], z["historical_events"]
            )
        else:
            proba, risk_level = 0.0, "LOW"
        zone_predictions.append({"zone": z, "probability": proba, "risk_level": risk_level})
    return {"data_notice": DEMO_DATA_NOTICE, "alerts": build_alerts(zone_predictions)}


@app.get("/weather")
def weather(zone_id: str = None):
    return {"data_notice": DEMO_DATA_NOTICE, "weather": get_demo_weather(zone_id)}


@app.get("/history/{zone_id}")
def history(zone_id: str, days: int = 14):
    raw_zones = get_zones_raw()
    if not any(z["id"] == zone_id for z in raw_zones):
        raise HTTPException(status_code=404, detail="Zone not found")
    return {"data_notice": DEMO_DATA_NOTICE, "zone_id": zone_id, "series": get_historical_series(zone_id, days)}
