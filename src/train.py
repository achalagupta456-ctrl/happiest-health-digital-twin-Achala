from __future__ import annotations
import json
from pathlib import Path
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from src.data_generator import generate_dataset
from src.features import build_features

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

def train(seed: int = 42):
    patients, dynamic = generate_dataset(seed=seed)
    df, feature_cols = build_features(patients, dynamic)
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed)
    train_idx, test_idx = next(splitter.split(df, groups=df["patient_id"]))
    train_df, test_df = df.iloc[train_idx], df.iloc[test_idx]
    X_train, y_train = train_df[feature_cols], train_df["event_2h"].astype(int)
    X_test, y_test = test_df[feature_cols], test_df["event_2h"].astype(int)
    candidates = {
        "logistic_regression": Pipeline([("scale", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=seed))]),
        "random_forest": RandomForestClassifier(n_estimators=250, max_depth=9, min_samples_leaf=5,
            class_weight="balanced", random_state=seed, n_jobs=-1)}
    results = {}
    best_name, best_auc, best_model = None, -1, None
    for name, model in candidates.items():
        model.fit(X_train, y_train)
        p = model.predict_proba(X_test)[:, 1]
        pred = (p >= 0.5).astype(int)
        results[name] = {"roc_auc": roc_auc_score(y_test, p),
            "pr_auc": average_precision_score(y_test, p),
            "precision": precision_score(y_test, pred, zero_division=0),
            "recall": recall_score(y_test, pred, zero_division=0),
            "f1": f1_score(y_test, pred, zero_division=0)}
        if results[name]["roc_auc"] > best_auc:
            best_name, best_auc, best_model = name, results[name]["roc_auc"], model
    joblib.dump({"model": best_model, "features": feature_cols}, MODEL_DIR / "glucotwin.joblib")
    (MODEL_DIR / "metrics.json").write_text(json.dumps({"best_model": best_name, "metrics": results}, indent=2))
    return results

if __name__ == "__main__":
    print(json.dumps(train(), indent=2))
