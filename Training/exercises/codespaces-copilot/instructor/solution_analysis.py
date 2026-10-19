"""INSTRUCTOR REFERENCE - Track A: DNA analysis on the synthetic dataset.

Participants should build their own version with GitHub Copilot. Use this file
to check their output, not to hand out up front.

Run from the exercise folder:
    python instructor/solution_analysis.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # no display needed inside a Codespace
import matplotlib.pyplot as plt
import pandas as pd

DATA_FILE = Path(__file__).parents[1] / "data" / "synthetic_outpatient_appointments.csv"
OUTPUT_DIR = Path(__file__).parents[1] / "outputs"
VALID_STATUSES = {"Attended", "DNA", "Cancelled"}


def load_data(path=DATA_FILE):
    df = pd.read_csv(path, parse_dates=["appointment_date"])
    return df


def validate(df):
    """Return a list of data-quality problems (empty list means clean)."""
    problems = []
    if df["appointment_id"].duplicated().any():
        problems.append("Duplicate appointment_id values found")
    if df.isna().any().any():
        problems.append("Missing values found")
    bad = set(df["attendance_status"]) - VALID_STATUSES
    if bad:
        problems.append(f"Unexpected attendance_status values: {sorted(bad)}")
    if (df["wait_days"] < 0).any():
        problems.append("Negative wait_days found")
    return problems


def dna_rate(df):
    """DNA rate = DNA / (Attended + DNA). Cancelled appointments are excluded."""
    seen = df[df["attendance_status"].isin(["Attended", "DNA"])]
    if seen.empty:
        return float("nan")
    return (seen["attendance_status"] == "DNA").mean()


def dna_by(df, column):
    seen = df[df["attendance_status"].isin(["Attended", "DNA"])]
    return (
        seen.groupby(column)["attendance_status"]
        .apply(lambda s: (s == "DNA").mean())
        .sort_values(ascending=False)
    )


def dna_by_month(df):
    seen = df[df["attendance_status"].isin(["Attended", "DNA"])].copy()
    seen["month"] = seen["appointment_date"].dt.to_period("M").dt.to_timestamp()
    return seen.groupby("month")["attendance_status"].apply(lambda s: (s == "DNA").mean())


def main():
    df = load_data()
    problems = validate(df)
    print("Data quality:", problems or "no problems found")
    print(f"Overall DNA rate: {dna_rate(df):.1%}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    dna_by(df, "speciality").plot.barh(ax=axes[0], title="DNA rate by speciality")
    dna_by(df, "age_band").sort_index().plot.bar(ax=axes[1], title="DNA rate by age band")
    dna_by_month(df).plot(ax=axes[2], marker="o", title="DNA rate by month")
    for ax in axes:
        ax.xaxis.label.set_visible(False)
    fig.tight_layout()
    out = OUTPUT_DIR / "dna_summary.png"
    fig.savefig(out, dpi=120)
    print(f"Saved chart to {out}")


if __name__ == "__main__":
    main()
