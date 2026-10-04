from __future__ import annotations
import numpy as np
import pandas as pd

def generate_dataset(n_patients: int = 800, hours_per_patient: int = 168, seed: int = 42):
    rng = np.random.default_rng(seed)
    patients = pd.DataFrame({
        "patient_id": np.arange(n_patients),
        "age": rng.integers(30, 76, n_patients),
        "bmi": np.clip(rng.normal(27.5, 4.5, n_patients), 18, 45),
        "hba1c": np.clip(rng.normal(7.1, 1.0, n_patients), 5.5, 11.5),
        "diabetes_years": np.clip(rng.gamma(2.5, 2.0, n_patients), 0, 20),
        "systolic_bp": np.clip(rng.normal(132, 16, n_patients), 95, 190),
        "family_history": rng.binomial(1, 0.55, n_patients),
        "med_adherence": np.clip(rng.beta(7, 2, n_patients), 0.25, 1.0),
        "baseline_glucose": np.clip(rng.normal(125, 25, n_patients), 75, 220),
    })
    rows = []
    for p in patients.itertuples(index=False):
        t = np.arange(hours_per_patient)
        circadian = 8 * np.sin(2 * np.pi * (t - 7) / 24)
        meal_pattern = (22 * np.exp(-((t % 24 - 8) / 1.7) ** 2)
                        + 30 * np.exp(-((t % 24 - 13) / 1.8) ** 2)
                        + 35 * np.exp(-((t % 24 - 20) / 2.0) ** 2))
        activity = np.clip(rng.gamma(2.0, 18, hours_per_patient), 0, 180)
        sleep = np.clip(7.0 + rng.normal(0, 0.7), 4.0, 9.5)
        hr = np.clip(68 + 0.20 * activity + rng.normal(0, 5, hours_per_patient), 48, 150)
        hrv = np.clip(62 - 0.20 * (hr - 65) + rng.normal(0, 7, hours_per_patient), 18, 110)
        glucose = (p.baseline_glucose + 0.55 * (p.hba1c - 6.5) * 25 + circadian
                   + meal_pattern + 0.10 * p.bmi * activity / 10 - 0.08 * activity
                   + rng.normal(0, 10, hours_per_patient))
        glucose = np.clip(glucose, 55, 320)
        for i in range(hours_per_patient):
            rows.append({"patient_id": p.patient_id, "hour": i, "glucose": float(glucose[i]),
                         "heart_rate": float(hr[i]), "hrv": float(hrv[i]), "steps": float(activity[i]),
                         "sleep_hours": float(sleep)})
    dynamic = pd.DataFrame(rows)
    future = dynamic.groupby("patient_id")["glucose"].shift(-2)
    dynamic["event_2h"] = (future >= 200).astype(int)
    dynamic.loc[dynamic.groupby("patient_id").cumcount(ascending=False) < 2, "event_2h"] = np.nan
    return patients, dynamic
