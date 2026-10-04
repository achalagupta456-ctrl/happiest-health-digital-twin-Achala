# GlucoTwin — 20-Minute Demonstration Script

## 0:00–2:00 — Opening
Introduce GlucoTwin as a healthcare Digital Twin PoC for Type 2 diabetes risk management. State the core question: can a continuously updated virtual patient combine historical health information with what is happening now to anticipate a high-glucose event two hours ahead?

## 2:00–5:00 — Problem and use case
Explain the shift from retrospective monitoring to proactive risk identification. Keep the outcome narrow: a binary 2-hour-ahead high-glucose event. Explain why this is suitable for a PoC: measurable, time-bound and directly connected to longitudinal glucose data.

## 5:00–8:00 — Digital Twin architecture
Walk through:
1. Synthetic EHR/static patient profile.
2. Dynamic CGM/wearable-style time series.
3. Feature-engineering layer.
4. Digital Twin state vector.
5. Risk model.
6. Clinician-facing dashboard.

Emphasize that the twin is not just a dashboard: the patient's state is recomputed from two data streams and passed into a predictive model.

## 8:00–11:00 — Data and feature fusion
Show examples of static variables: age, BMI, HbA1c, diabetes duration, blood pressure and medication adherence.

Show dynamic variables: current glucose, glucose slope, recent glucose mean/variation, activity, heart rate, HRV and sleep.

Explain that the same current glucose value can mean different things for different virtual patients because the historical profile changes the combined state.

## 11:00–14:00 — Model and validation
Explain the Logistic Regression baseline and Random Forest model. Explain patient-level splitting: observations from the same virtual patient are kept together to reduce leakage between training and testing.

Show ROC-AUC, PR-AUC, precision, recall and F1 after running the final training pipeline. Explicitly state that these are synthetic-data prototype metrics, not clinical validation.

## 14:00–18:00 — Live prototype demonstration
Run: streamlit run app.py

Select a patient. Point out:
- 2-hour risk probability
- risk tier
- current glucose
- HbA1c
- longitudinal glucose trajectory
- historical profile
- current dynamic signals

Switch patients to demonstrate that the twin is patient-specific.

Explain the safety boundary: a high-risk flag would route to human/clinician review in a real deployment; the PoC does not diagnose, prescribe or automatically alter treatment.

## 18:00–19:00 — Real-world pathway
Explain the scale-up path:
real EHR/CGM/wearable ingestion -> personalized baseline -> calibrated model -> clinician workflow -> prospective validation.

Mention privacy, consent, auditability, model monitoring and calibration as deployment requirements.

## 19:00–20:00 — Closing
Close with three points:
1. GlucoTwin fuses static and dynamic patient information.
2. It converts the fused state into an actionable early-warning signal.
3. It provides a feasible path from a student PoC to a clinically validated decision-support system.

End with: “This prototype is intentionally narrow, measurable and human-in-the-loop. The next step is validation on real longitudinal data.”
