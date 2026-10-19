"""Demo 2: count and chart. Saves a PNG in an `outputs/` folder (ignored by Git).

Run from the repository root:
    python Participant_Pack/demos/python/02_chart_demo.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # no screen needed in a Codespace
import matplotlib.pyplot as plt

from importlib.util import module_from_spec, spec_from_file_location

# Reuse the loader from demo 1.
_spec = spec_from_file_location("demo1", Path(__file__).with_name("01_explore_data.py"))
demo1 = module_from_spec(_spec)
_spec.loader.exec_module(demo1)

OUT = Path("outputs")


def main() -> None:
    df = demo1.load()
    counts = df["speciality"].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(8, 4))
    counts.plot.barh(ax=ax, color="#002060")
    ax.set_title("Appointments by speciality (synthetic data)")
    ax.set_xlabel("Number of appointments")
    ax.set_ylabel("")
    fig.tight_layout()
    OUT.mkdir(exist_ok=True)
    target = OUT / "appointments_by_speciality.png"
    fig.savefig(target, dpi=150)
    print("Saved", target)


if __name__ == "__main__":
    main()
