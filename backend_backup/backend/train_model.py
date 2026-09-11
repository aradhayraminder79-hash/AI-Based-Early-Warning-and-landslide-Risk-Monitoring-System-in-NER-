"""
train_model.py

Trains a RandomForestClassifier to predict landslide occurrence from
five environmental features: rainfall_24h, soil_moisture, slope,
elevation, historical_events.

*** IMPORTANT — READ BEFORE DEMO/PRESENTATION ***
The training data generated below is SYNTHETIC DEMO DATA built from a
simple, hand-tuned rule (higher rainfall + soil moisture + slope +
history => higher landslide likelihood) plus random noise. It is
NOT real historical landslide/weather/terrain data and must NOT be
presented as scientifically validated. It exists purely so the model
file has something to train on for a working end-to-end demo.

For a real deployment you would replace `generate_synthetic_dataset()`
with a loader that reads actual historical landslide records (e.g. from
Bhukosh/GSI landslide inventory, state disaster management databases)
joined with rainfall (IMD), soil moisture (satellite or in-situ sensors),
and terrain (slope/elevation from a DEM such as SRTM/Cartosat).

Usage:
    python train_model.py
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

RANDOM_STATE = 42
N_SAMPLES = 2000
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "risk_model.joblib")


def generate_synthetic_dataset(n_samples: int = N_SAMPLES, random_state: int = RANDOM_STATE) -> pd.DataFrame:
    """Generate a synthetic but *plausible* dataset for demo training.

    Feature ranges are chosen to roughly match real-world terrain/weather
    conditions seen in hilly NER districts, but the labels are produced
    by a synthetic scoring rule, NOT observed ground truth.
    """
    rng = np.random.default_rng(random_state)

    rainfall_24h = rng.uniform(0, 300, n_samples)          # mm
    soil_moisture = rng.uniform(10, 100, n_samples)        # %
    slope = rng.uniform(0, 60, n_samples)                  # degrees
    elevation = rng.uniform(0, 3000, n_samples)             # meters
    historical_events = rng.integers(0, 6, n_samples)       # count

    # Synthetic risk score combining normalized features (weights are
    # illustrative, not derived from real statistical analysis).
    score = (
        0.35 * (rainfall_24h / 300)
        + 0.25 * (soil_moisture / 100)
        + 0.25 * (slope / 60)
        + 0.05 * (elevation / 3000)
        + 0.10 * (historical_events / 5)
    )

    noise = rng.normal(0, 0.05, n_samples)
    score = np.clip(score + noise, 0, 1)

    # Convert score to a binary landslide/no-landslide label using a
    # fixed threshold with noise already baked in above, so the classes
    # are mostly-but-not-perfectly separable (avoids an unrealistic 100%
    # accuracy while still giving a presentable demo score).
    landslide = (score > 0.5).astype(int)

    df = pd.DataFrame({
        "rainfall_24h": rainfall_24h,
        "soil_moisture": soil_moisture,
        "slope": slope,
        "elevation": elevation,
        "historical_events": historical_events,
        "landslide": landslide,
    })
    return df


def train_and_save_model():
    print("Generating synthetic demo dataset (NOT real field data)...")
    df = generate_synthetic_dataset()
    print(f"Dataset shape: {df.shape}")
    print(f"Class balance:\n{df['landslide'].value_counts(normalize=True)}\n")

    feature_cols = ["rainfall_24h", "soil_moisture", "slope", "elevation", "historical_events"]
    X = df[feature_cols]
    y = df["landslide"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_leaf=3,
        random_state=RANDOM_STATE,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Test Accuracy: {accuracy:.4f}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["No Landslide", "Landslide"]))

    importances = dict(zip(feature_cols, model.feature_importances_.round(3)))
    print(f"Feature Importances: {importances}\n")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({"model": model, "feature_cols": feature_cols}, MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save_model()
