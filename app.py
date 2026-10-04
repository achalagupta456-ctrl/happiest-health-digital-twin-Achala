from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from src.data_generator import generate_dataset
from src.predict import predict

st.set_page_config(page_title="GlucoTwin", page_icon="🧬", layout="wide")
st.title("🧬 GlucoTwin")
st.caption("Synthetic Digital Twin for 2-hour-ahead glucose-spike risk prediction")

patients, dynamic = generate_dataset(n_patients=50, hours_per_patient=48, seed=11)
patient_id = st.sidebar.selectbox("Select virtual patient", patients["patient_id"].tolist())
p = patients.loc[patients.patient_id == patient_id].iloc[0]
history = dynamic.loc[dynamic.patient_id == patient_id].copy()
latest = history.iloc[-1]

state = {
    "age": p.age, "bmi": p.bmi, "hba1c": p.hba1c, "diabetes_years": p.diabetes_years,
    "systolic_bp": p.systolic_bp, "family_history": p.family_history,
    "med_adherence": p.med_adherence, "baseline_glucose": p.baseline_glucose,
    "glucose": latest.glucose, "glucose_slope": history.glucose.diff().tail(3).mean(),
    "glucose_mean_6h": history.glucose.tail(6).mean(), "glucose_std_6h": history.glucose.tail(6).std(),
    "steps_3h": history.steps.tail(3).sum(), "hr_mean_3h": history.heart_rate.tail(3).mean(),
    "hrv_mean_3h": history.hrv.tail(3).mean(), "sleep_hours": latest.sleep_hours,
}
risk = predict(state)
tier = "HIGH" if risk >= 0.70 else "MODERATE" if risk >= 0.40 else "LOW"

c1, c2, c3, c4 = st.columns(4)
c1.metric("2-hour risk", f"{risk:.0%}")
c2.metric("Risk tier", tier)
c3.metric("Current glucose", f"{latest.glucose:.0f} mg/dL")
c4.metric("HbA1c", f"{p.hba1c:.1f}%")

st.subheader("Live digital-twin state")
fig = go.Figure()
fig.add_trace(go.Scatter(x=history.hour, y=history.glucose, mode="lines+markers", name="Glucose"))
fig.add_hline(y=200, line_dash="dash", annotation_text="High-glucose threshold")
fig.update_layout(height=330, xaxis_title="Simulation hour", yaxis_title="Glucose (mg/dL)")
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Historical profile")
    st.dataframe(pd.DataFrame({
        "Factor": ["Age", "BMI", "Diabetes duration", "HbA1c", "Systolic BP", "Medication adherence", "Family history"],
        "Value": [f"{p.age} y", f"{p.bmi:.1f}", f"{p.diabetes_years:.1f} y", f"{p.hba1c:.1f}%",
                  f"{p.systolic_bp:.0f} mmHg", f"{p.med_adherence:.0%}", "Yes" if p.family_history else "No"]}),
        hide_index=True, use_container_width=True)
with right:
    st.subheader("Current dynamic signals")
    st.dataframe(pd.DataFrame({
        "Signal": ["Glucose", "Glucose slope", "3h steps", "3h mean HR", "3h mean HRV", "Sleep"],
        "Value": [f"{latest.glucose:.0f} mg/dL", f"{state['glucose_slope']:+.1f} mg/dL/h",
                  f"{state['steps_3h']:.0f}", f"{state['hr_mean_3h']:.0f} bpm",
                  f"{state['hrv_mean_3h']:.0f} ms", f"{p.sleep_hours:.1f} h"]}),
        hide_index=True, use_container_width=True)

st.subheader("Digital-twin interpretation")
if tier == "HIGH":
    st.warning("High predicted probability of a glucose-spike event within 2 hours. In real deployment this would trigger clinician review, not automated treatment.")
elif tier == "MODERATE":
    st.info("Intermediate predicted risk. Recent glucose trajectory and physiological signals warrant closer observation.")
else:
    st.success("Lower predicted risk at this point. Continue monitoring the evolving state.")
st.caption("Synthetic data only • Educational prototype • Not for clinical decision-making")
