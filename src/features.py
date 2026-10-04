from __future__ import annotations
import pandas as pd

STATIC_COLS = ["age", "bmi", "hba1c", "diabetes_years", "systolic_bp",
               "family_history", "med_adherence", "baseline_glucose"]

def build_features(patients: pd.DataFrame, dynamic: pd.DataFrame):
    d = dynamic.sort_values(["patient_id", "hour"]).copy()
    d["glucose_slope"] = d.groupby("patient_id")["glucose"].diff()
    d["glucose_mean_6h"] = d.groupby("patient_id")["glucose"].transform(lambda s: s.rolling(6, min_periods=1).mean())
    d["glucose_std_6h"] = d.groupby("patient_id")["glucose"].transform(lambda s: s.rolling(6, min_periods=2).std()).fillna(0)
    d["steps_3h"] = d.groupby("patient_id")["steps"].transform(lambda s: s.rolling(3, min_periods=1).sum())
    d["hr_mean_3h"] = d.groupby("patient_id")["heart_rate"].transform(lambda s: s.rolling(3, min_periods=1).mean())
    d["hrv_mean_3h"] = d.groupby("patient_id")["hrv"].transform(lambda s: s.rolling(3, min_periods=1).mean())
    out = d.merge(patients, on="patient_id", how="left").dropna(subset=["event_2h"]).copy()
    feature_cols = STATIC_COLS + ["glucose", "glucose_slope", "glucose_mean_6h",
        "glucose_std_6h", "steps_3h", "hr_mean_3h", "hrv_mean_3h", "sleep_hours"]
    return out, feature_cols
