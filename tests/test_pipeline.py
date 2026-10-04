from src.data_generator import generate_dataset
from src.features import build_features

def test_static_dynamic_fusion():
    patients, dynamic = generate_dataset(n_patients=8, hours_per_patient=24, seed=7)
    df, features = build_features(patients, dynamic)
    assert len(df) > 0
    assert "hba1c" in features
    assert "glucose" in features
    assert "hrv_mean_3h" in features
    assert df["patient_id"].nunique() == 8
