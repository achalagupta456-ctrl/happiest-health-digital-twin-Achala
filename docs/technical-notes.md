# Technical Notes

## Reproducibility
Synthetic data generation is seeded. The training script creates the model artifact and metrics file under models/.

## Leakage control
The split is performed with GroupShuffleSplit using patient ID as the grouping variable. This prevents rows from the same synthetic patient appearing in both train and test partitions.

## Model selection
Logistic Regression is retained as a simple baseline. Random Forest provides a nonlinear comparison. The model with the higher test ROC-AUC is saved as the prototype model.

## Safety
The system is a risk-stratification prototype. It does not diagnose diabetes, prescribe medication, recommend dosage changes or autonomously intervene.

## Data limitations
All data are synthetic. The simulation does not establish clinical validity, calibration, causal relationships or generalizability to real patients.

## Next validation steps
- Validate on a real longitudinal CGM/EHR cohort.
- Evaluate calibration and decision-curve utility.
- Test subgroup performance and fairness.
- Compare personalized versus population-level baselines.
- Add drift monitoring and model versioning.
- Conduct prospective clinician-in-the-loop evaluation.
