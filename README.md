# GlucoTwin — A Digital Twin for Proactive Glucose-Spike Risk Management

**Happiest Health Digital Twin Challenge 2026**

## Team details

- **Team:** Achala Gupta
- **Team Leader:** Achala Gupta
- **College:** Vinod Gupta School of Management (VGSoM), IIT Kharagpur
- **Incubator:** Not applicable
- **Project Title:** GlucoTwin — A Digital Twin for Proactive Glucose-Spike Risk Management

## 1. Problem Statement

Diabetes management is often retrospective: historical measurements are reviewed separately from what is happening to a patient in real time. The challenge is to maintain a continuously updated representation of a patient that combines their historical health profile with current physiological and behavioral signals, and then use that state to anticipate a specific near-term risk.

**GlucoTwin addresses this by predicting the probability of a high-glucose event in the next 2 hours for a patient with Type 2 diabetes.**

## 2. Healthcare Use Case

The prototype is designed for **proactive Type 2 diabetes risk management**.

It combines:

- **Static / historical data:** age, BMI, HbA1c, diabetes duration, systolic blood pressure, family history, medication adherence and baseline glucose.
- **Dynamic / real-time data:** current glucose, glucose slope, recent glucose trajectory, heart rate, HRV, activity/steps and sleep.

The system produces a patient-specific **2-hour risk probability** and a LOW / MODERATE / HIGH risk tier for clinician review.

> **Safety boundary:** GlucoTwin is a risk-stratification proof-of-concept. It does not diagnose disease, prescribe medication, recommend dosage changes or autonomously intervene.

## 3. What Makes It a Digital Twin?

GlucoTwin is not a one-time prediction from a static dataset. It represents a patient's current state by combining historical context with dynamic observations. As new observations arrive, the state can be recalculated and the near-term risk can change.

**Historical profile → dynamic observations → feature fusion → current digital-twin state → 2-hour risk → human review**

## 4. Technical Stack

- Python 3.11+
- Pandas
- NumPy
- scikit-learn
- Streamlit
- Plotly
- Joblib
- GitHub

## 5. AI / ML Model and Framework Details

**Models**
- Logistic Regression — interpretable baseline with feature scaling and balanced class weights.
- Random Forest Classifier — nonlinear primary comparison with class balancing.

**Feature engineering**
- Glucose slope
- 6-hour glucose mean and standard deviation
- 3-hour activity/steps aggregation
- Mean heart rate
- Mean HRV
- Static patient profile variables

**Validation**
- Patient-level GroupShuffleSplit is used so observations from the same synthetic patient do not appear in both training and test partitions.
- Evaluation metrics: ROC-AUC, PR-AUC, precision, recall and F1.
- The model with the stronger test ROC-AUC is retained as the prototype model.

## 6. Prototype and Demo

Run locally:

    python -m venv .venv
    pip install -r requirements.txt
    python src/train.py
    streamlit run app.py

The prediction helper automatically trains the model if the saved model artifact is absent.

### Demo Summary

The prototype demonstration covers the complete GlucoTwin workflow:

1. **Patient context:** a synthetic longitudinal Type 2 diabetes profile is created using historical/EHR-style attributes.
2. **Live signals:** dynamic glucose, glucose trend, heart rate, HRV, activity and sleep observations are introduced.
3. **Digital Twin state:** historical and dynamic signals are fused into a continuously updated patient representation.
4. **Prediction:** Logistic Regression provides a baseline and Random Forest provides the nonlinear comparison for predicting a high-glucose event in the next 2 hours.
5. **Risk output:** the system converts the predicted probability into LOW / MODERATE / HIGH risk for clinician review.
6. **Dashboard:** the Streamlit interface presents the patient's current glucose, trajectory, historical profile, dynamic signals and predicted risk together.
7. **Safety:** the prototype remains a decision-support proof of concept; it does not diagnose, prescribe medication or autonomously intervene.

The complete demonstration flow can be reproduced locally using the commands above and the source code in this repository.

## 7. Architecture

The architecture follows:

**Historical / EHR data + Dynamic wearable/CGM-style stream → Feature engineering → Digital Twin state vector → AI/ML prediction → Risk output → Clinician dashboard → Human review**

Files:
- [Architecture diagram — PDF](submission/GlucoTwin_Architecture.pdf)
- [Architecture diagram — PPTX](submission/GlucoTwin_Architecture.pptx)
- [Architecture documentation](docs/architecture.md)

## 8. Presentation

- [Presentation — PDF](submission/GlucoTwin_Presentation.pdf)
- [Presentation — PPTX](submission/GlucoTwin_Presentation.pptx)
- [20-minute demo script](docs/20-minute-demo-script.md)

## 9. Open-source License

This repository is released under the **MIT License**. See [LICENSE](LICENSE).

## 10. Repository Structure

    app.py
    src/
      data_generator.py
      features.py
      train.py
      predict.py
    tests/
    docs/
    submission/
      GlucoTwin_Architecture.pdf
      GlucoTwin_Architecture.pptx
      GlucoTwin_Presentation.pdf
      GlucoTwin_Presentation.pptx
    requirements.txt
    LICENSE

## 11. Reproducibility and Limitations

All demonstration data are synthetic and generated reproducibly. The prototype does **not** establish clinical validity, calibration, causal relationships or generalizability to real patients.

Before any real-world deployment, the system would require de-identified longitudinal clinical validation, calibration, subgroup/fairness analysis, prospective clinician-in-the-loop evaluation, privacy/security controls, monitoring for data drift and formal clinical governance.

## Submission readiness

- [x] Team details
- [x] College / incubator information
- [x] Project title
- [x] Problem statement
- [x] Healthcare use case
- [x] Technical stack
- [x] AI/ML model and framework details
- [ ] 20-minute unlisted YouTube demo link — **only remaining manual item**
- [x] Open-source license details
- [x] Architecture diagram in PDF/PPT
- [x] Presentation in PDF/PPT
- [x] Repository is public

## Disclaimer

This is an educational proof-of-concept using synthetic data. Predictions are not clinically validated and must not be used to make real medical decisions.
