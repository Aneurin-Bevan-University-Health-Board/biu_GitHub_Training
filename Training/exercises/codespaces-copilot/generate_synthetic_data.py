"""Generate a FULLY SYNTHETIC outpatient appointments dataset for the training exercise.

Nothing here is derived from real patients, real clinics or real NHS data.
There are no patient identifiers of any kind. The data is created from a fixed
random seed, so everyone who runs this script gets exactly the same file.

Usage (from this folder):
    python generate_synthetic_data.py
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 20251019
N_ROWS = 3000
OUT_FILE = Path(__file__).parent / "data" / "synthetic_outpatient_appointments.csv"

SPECIALITIES = {
    # speciality: (relative volume, base DNA probability)
    "Cardiology": (3, 0.06),
    "Diabetes": (3, 0.14),
    "Dermatology": (2, 0.10),
    "Ophthalmology": (3, 0.08),
    "Orthopaedics": (3, 0.07),
    "Respiratory": (2, 0.09),
}
SITES = ["Site A", "Site B", "Site C"]
AGE_BANDS = {
    # age band: (relative volume, DNA probability multiplier)
    "16-24": (1, 1.9),
    "25-39": (2, 1.4),
    "40-59": (3, 1.0),
    "60-74": (3, 0.7),
    "75+": (2, 0.8),
}
START = date(2025, 1, 6)  # a Monday
END = date(2025, 12, 19)


def weighted_choice(rng, options):
    names = list(options)
    weights = [options[n][0] for n in names]
    return rng.choices(names, weights=weights, k=1)[0]


def random_weekday(rng):
    while True:
        d = START + timedelta(days=rng.randint(0, (END - START).days))
        if d.weekday() < 5:
            return d


def main():
    rng = random.Random(SEED)
    rows = []
    for i in range(1, N_ROWS + 1):
        speciality = weighted_choice(rng, SPECIALITIES)
        age_band = weighted_choice(rng, AGE_BANDS)
        appt_date = random_weekday(rng)
        appt_type = rng.choices(["New", "Follow-up"], weights=[35, 65], k=1)[0]
        wait_days = max(1, int(rng.gauss(55 if appt_type == "New" else 28, 22)))

        p_dna = SPECIALITIES[speciality][1] * AGE_BANDS[age_band][1]
        p_dna *= 1 + min(wait_days, 120) / 240  # longer waits -> slightly more DNAs
        p_dna *= 1.25 if appt_date.month in (1, 2, 12) else 1.0  # winter effect
        p_dna = min(p_dna, 0.6)
        p_cancel = 0.07

        r = rng.random()
        if r < p_dna:
            status = "DNA"
        elif r < p_dna + p_cancel:
            status = "Cancelled"
        else:
            status = "Attended"

        rows.append(
            {
                "appointment_id": f"SYN-{i:05d}",
                "appointment_date": appt_date.isoformat(),
                "speciality": speciality,
                "clinic_site": rng.choice(SITES),
                "age_band": age_band,
                "appointment_type": appt_type,
                "wait_days": wait_days,
                "attendance_status": status,
            }
        )

    rows.sort(key=lambda row: (row["appointment_date"], row["appointment_id"]))
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} synthetic rows to {OUT_FILE}")


if __name__ == "__main__":
    main()
