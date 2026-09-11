"""
Prototype Landslide Risk Model Trainer
---------------------------------------
Creates a synthetic dataset for the college prototype.
This is NOT a real-world historical landslide dataset.
"""

from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42
N_SAMPLES = 5000

FEATURES = [
    "rainfall_24h",
    "soil_moisture",
    "slope",
    "elevation",
    "historical_events",
]


def create_synthetic_dataset(n_samples=5000):
    rng = np.random.default_rng(RANDOM_STATE)

    rainfall = rng.uniform(0, 300, n_samples)
    soil = rng.uniform(20, 95, n_samples)
    slope = rng.uniform(5, 50, n_samples)
    elevation = rng.uniform(0, 3000, n_samples)
    historical = rng.integers(0, 9, n_samples)

    rain_risk = np.clip(rainfall / 250, 0, 1)
    soil_risk = np.clip((soil - 20) / 75, 0, 1)
    slope_risk = np.clip((slope - 5) / 45, 0, 1)
    history_risk = np.clip(historical / 8, 0, 1)
    elevation_risk = np.clip(elevation / 3000, 0, 1)

    risk_score = (
        0.50 * rain_risk
        + 0.20 * soil_risk
        + 0.20 * slope_risk
        + 0.08 * history_risk
        + 0.02 * elevation_risk
    )

    risk_score += rng.normal(0, 0.08, n_samples)

    threshold = np.quantile(risk_score, 0.62)
    landslide = (risk_score >= threshold).astype(int)

    return pd.DataFrame({
        "rainfall_24h": np.round(rainfall, 2),
        "soil_moisture": np.round(soil, 2),
        "slope": np.round(slope, 2),
        "elevation": np.round(elevation, 2),
        "historical_events": historical,
        "landslide": landslide,
    })


def main():
    print("=" * 60)
    print("AI Landslide Risk Model Training")
    print("=" * 60)

    df = create_synthetic_dataset(N_SAMPLES)

    print(f"\nTraining samples: {len(df)}")
    print(f"Landslide samples: {df['landslide'].sum()}")
    print(f"Non-landslide samples: {(df['landslide'] == 0).sum()}")

    X = df[FEATURES]
    y = df["landslide"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=4,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    print("\nTraining Random Forest...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, predictions)
    auc = roc_auc_score(y_test, probabilities)

    print("\n" + "=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)

    print(f"Accuracy : {accuracy:.3f}")
    print(f"ROC-AUC  : {auc:.3f}")

    print("\nClassification report:")
    print(classification_report(y_test, predictions))

    print("\nFeature importance:")

    for feature, importance in sorted(
        zip(FEATURES, model.feature_importances_),
        key=lambda x: x[1],
        reverse=True,
    ):
        print(f"  {feature:20s} {importance:.3f}")

    model_path = (
        Path(__file__).resolve().parent
        / "model"
        / "risk_model.joblib"
    )

    model_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        {
            "model": model,
            "features": FEATURES,
            "feature_cols": FEATURES,
            "model_version": "prototype-v2",
            "training_samples": N_SAMPLES,
            "training_type": "synthetic_prototype",
        },
        model_path,
    )

    dataset_path = (
        Path(__file__).resolve().parent
        / "model"
        / "training_dataset.csv"
    )

    df.to_csv(dataset_path, index=False)

    print("\n" + "=" * 60)
    print("FILES CREATED")
    print("=" * 60)

    print(f"Model   : {model_path}")
    print(f"Dataset : {dataset_path}")

    print("\nWARNING:")
    print("This is a synthetic prototype model.")
    print("Replace the training dataset with verified historical")
    print("landslide observations before real-world deployment.")


if __name__ == "__main__":
    main()
