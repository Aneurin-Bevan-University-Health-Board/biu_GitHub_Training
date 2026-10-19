"""Demo 1: explore a dataset before you analyse it.

Uses the SYNTHETIC appointments file. Run from the repository root:
    python Participant_Pack/demos/python/01_explore_data.py
"""
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[3]
DATA = REPO / "Training" / "exercises" / "codespaces-copilot" / "data" / "synthetic_outpatient_appointments.csv"


def load(path: Path = DATA) -> pd.DataFrame:
    """Load the appointments CSV, parsing the date column."""
    return pd.read_csv(path, parse_dates=["appointment_date"])


def main() -> None:
    df = load()
    print("Rows and columns:", df.shape)
    print("\nColumn types:\n", df.dtypes)
    print("\nFirst five rows:\n", df.head())
    print("\nMissing values per column:\n", df.isna().sum())
    print("\nDuplicate appointment IDs:", df["appointment_id"].duplicated().sum())
    # Always look at the categories before you trust them.
    print("\nAttendance status:\n", df["attendance_status"].value_counts())
    print("\nSpecialities:\n", df["speciality"].value_counts())


if __name__ == "__main__":
    main()
