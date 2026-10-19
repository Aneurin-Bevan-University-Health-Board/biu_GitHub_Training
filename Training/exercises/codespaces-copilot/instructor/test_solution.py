"""INSTRUCTOR REFERENCE tests - also a good stretch task: ask Copilot to write these."""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from solution_analysis import dna_rate, load_data, validate  # noqa: E402


def make_df(statuses):
    return pd.DataFrame({"attendance_status": statuses})


def test_dna_rate_excludes_cancelled():
    # 1 DNA out of (3 attended + 1 DNA) = 25%; the cancelled row is ignored
    df = make_df(["Attended", "Attended", "Attended", "DNA", "Cancelled"])
    assert dna_rate(df) == 0.25


def test_dna_rate_empty_is_nan():
    assert pd.isna(dna_rate(make_df(["Cancelled"])))


def test_synthetic_data_is_clean():
    assert validate(load_data()) == []
