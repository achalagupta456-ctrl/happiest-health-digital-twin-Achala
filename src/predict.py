from __future__ import annotations
from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "glucotwin.joblib"

def load_model():
    if not MODEL_PATH.exists():
        from src.train import train
        train()
    return joblib.load(MODEL_PATH)

def predict(patient_state: dict) -> float:
    bundle = load_model()
    frame = pd.DataFrame([patient_state])[bundle["features"]]
    return float(bundle["model"].predict_proba(frame)[:, 1][0])
