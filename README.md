# GlucoTwin — A Digital Twin for Proactive Glucose-Spike Prevention

Happiest Health Digital Twin Challenge 2026 | IIT Kharagpur, VGSoM

GlucoTwin is a proof-of-concept healthcare Digital Twin for Type 2 diabetes risk management. It fuses a patient's static/historical health profile with dynamic wearable/CGM-style time-series signals to estimate the probability of a clinically meaningful glucose spike in the next 2 hours.

Synthetic-data research PoC only. It is not a medical device and must not be used for diagnosis or treatment.

## Problem & healthcare use case

Diabetes management is often retrospective. GlucoTwin creates a continuously updated virtual patient state and asks: Given this patient's history and what their body is doing now, how likely is a glucose spike in the next 2 hours?

The prototype targets 2-hour-ahead high-glucose event prediction.

## Required data fusion

Static/historical EHR: age, BMI, HbA1c, diabetes duration, blood pressure, family history, medication adherence and baseline glucose.

Dynamic/real-time: current glucose, glucose slope, heart rate, HRV, steps/activity, sleep duration and recent glucose trajectory.

## Architecture

Synthetic EHR + wearable/CGM stream -> feature engineering -> Digital Twin state -> ML risk model -> risk explanation -> clinician dashboard.

See docs/architecture.md and docs/architecture.svg.

## Technical stack

Python 3.11+, Pandas, NumPy, Scikit-learn, Streamlit, Plotly and Joblib. Models: Logistic Regression baseline and Random Forest classifier.

## Run locally

    python -m venv .venv
    pip install -r requirements.txt
    python src/train.py
    streamlit run app.py

The application automatically trains the model if it does not exist.

## Repository structure

app.py — clinician-facing dashboard
src/data_generator.py — reproducible synthetic EHR + dynamic data
src/features.py — static/dynamic feature fusion
src/train.py — model training and evaluation
src/predict.py — prediction helper
tests/ — pipeline test
docs/ — architecture and presentation material

## Model and evaluation

The pipeline generates synthetic longitudinal patients, creates static EHR profiles, generates hourly dynamic observations, creates a 2-hour-ahead event label, uses patient-level splitting to reduce leakage, compares Logistic Regression and Random Forest, and reports ROC-AUC, PR-AUC, precision, recall and F1.

## Submission checklist

[x] Working Digital Twin PoC
[x] Static + dynamic data fusion
[x] Localized healthcare outcome
[x] Clinician conceptual dashboard
[x] Technical documentation
[x] Open-source license
[ ] 20-minute demonstration video link (record after final model/demo QA)
[ ] PDF/PPT architecture diagram
[ ] PDF/PPT presentation
[ ] Team details / final submission metadata

The repository is now **Public** and is intended to be directly accessible to the evaluation team. Before final submission, verify that every linked file/video is also accessible without login.

## Disclaimer

This is an educational prototype using synthetic data. Predictions are not clinically validated and should not guide real medical decisions.
