"""Demo 3: the smallest useful Streamlit app, with one filter.

Run from the repository root:
    streamlit run Participant_Pack/demos/python/03_streamlit_hello.py
"""
from pathlib import Path

import pandas as pd
import streamlit as st

REPO = Path(__file__).resolve().parents[3]
DATA = REPO / "Training" / "exercises" / "codespaces-copilot" / "data" / "synthetic_outpatient_appointments.csv"

st.title("Appointments explorer (synthetic data)")


@st.cache_data
def load() -> pd.DataFrame:
    return pd.read_csv(DATA, parse_dates=["appointment_date"])


df = load()
site = st.selectbox("Clinic site", ["All"] + sorted(df["clinic_site"].unique()))
if site != "All":
    df = df[df["clinic_site"] == site]

st.metric("Appointments", f"{len(df):,}")
st.bar_chart(df["speciality"].value_counts())
st.dataframe(df.head(20))
