# Methodology

## Target

For each hourly virtual-patient observation, the label is 1 when the glucose value two hours ahead is at least 200 mg/dL.

## Feature groups

**Historical:** age, BMI, HbA1c, diabetes duration, systolic BP, family history, medication adherence and baseline glucose.

**Dynamic:** current glucose, glucose slope, six-hour glucose mean/std, three-hour steps, three-hour mean HR, three-hour mean HRV and sleep duration.

## Leakage control

Patient IDs are used as groups during train/test splitting, so a patient's observations remain on one side of the split.

## Models

- Logistic Regression provides an interpretable baseline.
- Random Forest captures non-linear interactions among static and dynamic signals.

The higher ROC-AUC model is saved as the PoC model.

## Evaluation

The training script reports ROC-AUC, PR-AUC, precision, recall and F1 on the held-out patient group.

## Clinical interpretation

The risk score is a probability estimate for the synthetic target event. It is not a diagnosis and has no validated clinical threshold.
