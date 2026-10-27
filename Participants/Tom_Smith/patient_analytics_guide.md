# Patient Analytics: Technical Guide

## What this file does

`patient_analytics.py` creates a small set of made-up patients, checks their
latest measurements against a few simple rules, and prints a summary report.
It is a Python training example, not a medical tool. It does not read real
patient records or provide medical advice.

## How it works

1. **Creates fictional patients.** `generate_patients()` uses a random seed to
   create names, dates of birth, conditions, and one to four sets of vital
   signs. Using the same seed produces the same generated data.
2. **Stores the data in objects.** A `Patient` holds a person's details and
   encounter history. A `Vitals` object holds one set of measurements.
   `Sex` and `RiskTier` are named sets of allowed values.
3. **Checks for risk factors.** `assess_patient()` runs each default rule on a
   patient's latest measurements and details. Rules add points when they find:
   - High blood pressure: 3 points
   - High glucose: 2 points
   - BMI of 30 or more: 2 points
   - At least two listed conditions: 1 point
   - Age 65 or older: 1 point

   The score becomes a tier: 0–1 is **low**, 2–4 **moderate**, 5–7 **high**,
   and 8 or more **critical**. The report lists the reasons for any points.
4. **Summarizes the group.** The reporting functions calculate simple glucose
   and BMI statistics, count risk tiers, and count listed conditions. The
   normal-range flags in `Vitals.abnormal_flags()` are a separate feature;
   they are not used to calculate the risk score.
5. **Prints a report.** By default, `render_report()` produces a text report,
   including group summaries and up to five patients with the highest scores.
   With the CSV option, `write_csv()` outputs one row per patient assessment.

## Running it

From the repository root, run:

```text
python Participants/Tom_Smith/patient_analytics.py
```

Options:

- `-n` or `--count`: number of fictional patients to create (default: 25).
- `-s` or `--seed`: seed for repeatable generated data (default: 1337).
- `--csv`: print CSV instead of the text report.

For example:

```text
python Participants/Tom_Smith/patient_analytics.py --count 10 --seed 42 --csv
```

The generated data is repeatable with the same seed. The report's generation
time and patients' calculated ages can still change over time.

## Other Python features demonstrated

- **Audit logging:** `@audited` records calls to patient generation and risk
  assessment. `audit_session()` marks the start and end of a run. This log is
  kept only in memory and is not included in the report.
- **Reusable rules:** risk checks are functions, so `assess_patient()` can be
  given a different list of rules.
- **Typing helpers:** type hints describe expected values; `SupportsWrite`
  allows CSV output to go to different text streams.
- **Reusable reporting:** cohort statistics, tier counts, condition counts,
  CSV output, and text output are separate functions.
