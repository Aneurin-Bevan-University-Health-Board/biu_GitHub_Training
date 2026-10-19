"""INSTRUCTOR REFERENCE - Track B: a small Streamlit app over the synthetic dataset.

Run from the exercise folder:
    streamlit run instructor/solution_app.py

In a Codespace, a pop-up offers to open the forwarded port (8501) in your browser.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
from solution_analysis import DATA_FILE, dna_by, dna_by_month, dna_rate  # noqa: E402

st.set_page_config(page_title="Outpatient DNA explorer (synthetic data)", layout="wide")
st.title("Outpatient DNA explorer")
st.caption("SYNTHETIC DATA - training exercise only. No real patient data.")


@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(DATA_FILE, parse_dates=["appointment_date"])


df = get_data()

with st.sidebar:
    st.header("Filters")
    specialities = st.multiselect("Speciality", sorted(df["speciality"].unique()))
    sites = st.multiselect("Clinic site", sorted(df["clinic_site"].unique()))
    min_d, max_d = df["appointment_date"].min().date(), df["appointment_date"].max().date()
    date_range = st.date_input("Appointment dates", (min_d, max_d), min_value=min_d, max_value=max_d)

filtered = df
if specialities:
    filtered = filtered[filtered["speciality"].isin(specialities)]
if sites:
    filtered = filtered[filtered["clinic_site"].isin(sites)]
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = (pd.Timestamp(d) for d in date_range)
    filtered = filtered[filtered["appointment_date"].between(start, end)]

if filtered.empty:
    st.warning("No appointments match the selected filters.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Appointments", f"{len(filtered):,}")
col2.metric("DNA rate", f"{dna_rate(filtered):.1%}")
col3.metric("Median wait (days)", f"{filtered['wait_days'].median():.0f}")

left, right = st.columns(2)
with left:
    st.subheader("DNA rate by speciality")
    st.bar_chart(dna_by(filtered, "speciality"))
with right:
    st.subheader("DNA rate by month")
    st.line_chart(dna_by_month(filtered))

st.subheader("Appointments")
st.dataframe(filtered, hide_index=True)
