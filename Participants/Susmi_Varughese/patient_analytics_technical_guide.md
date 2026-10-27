# Patient Analytics: Technical Guide

## Purpose and safety

`patient_analytics.py` is a Python training example that simulates a small
clinical analytics pipeline. All names, medical record numbers, conditions,
dates, and measurements are fabricated. The module is not medical advice and
must not be used for clinical decisions or with real patient information.

## Design overview

The pipeline has four main stages:

1. **Generate a cohort.** `generate_patients(count, seed)` uses a local seeded
   random number generator to create fictional patients and one to four dated
   vital-sign encounters for each. The default seed is `1337`.
2. **Assess risk.** `assess_patient(patient)` applies each rule in
   `DEFAULT_RULES` to the patient's latest encounter and adds the points from
   each matching rule.
3. **Summarize results.** Reporting functions calculate cohort statistics,
   count risk tiers, tally conditions, and produce either a text report or CSV.
4. **Run from the command line.** `main()` parses options, wraps the run in an
   audit session, generates the cohort, and prints the selected output format.

## Data model

- `Sex` and `RiskTier` are enums. Risk tiers are derived from the total score:
  **low** below 2, **moderate** from 2, **high** from 5, and **critical** from
  8.
- `Vitals` stores systolic and diastolic blood pressure, heart rate, glucose,
  BMI, and temperature. `as_dict()` exposes those measurements as a mapping;
  `abnormal_flags()` compares them with `REFERENCE_RANGES` and reports values
  below or above those ranges.
- `Patient` stores a fictional MRN, name, birth date, sex, conditions, and
  dated `Vitals` encounters. Its `age` property calculates age relative to the
  current date, and `latest_vitals()` returns the measurements from the most
  recent encounter (or `None` if there are no encounters).
- `RiskAssessment` groups a patient, their score, and the reasons returned by
  rules; its `tier` property converts the score to a `RiskTier`.

## Risk rules

The default rules are additive and inspect the latest vitals where applicable:

| Condition | Points |
|---|---:|
| Systolic blood pressure at least 140 or diastolic at least 90 | 3 |
| Glucose at least 140 | 2 |
| BMI at least 30 | 2 |
| Two or more listed conditions | 1 |
| Age at least 65 | 1 |

Each matching rule also returns a short reason. The measurement reference
ranges used by `Vitals.abnormal_flags()` are separate from these risk rules;
those flags do not directly add points to an assessment.

## Reporting and audit behavior

- `cohort_statistics()` reports mean and median glucose, maximum glucose, and
  population standard deviation of BMI for patients with available vitals.
- `tier_breakdown()` counts assessments by tier.
- `condition_prevalence()` counts listed conditions across the cohort.
- `render_report()` combines those summaries and lists up to five patients in
  descending score order.
- `write_csv()` writes one row per assessment with MRN, name, age, score, tier,
  and reasons to a text stream.
- `@audited` appends timestamped function-call entries to the in-memory
  `_AUDIT_TRAIL`. `audit_session()` appends begin/end markers even if the
  enclosed work raises an exception. The command-line entry point does not
  print or persist this trail.

## Command-line use

Run the script with Python. The options are:

- `-n` / `--count`: number of fictional patients (default `25`).
- `-s` / `--seed`: random seed (default `1337`).
- `--csv`: print CSV instead of the text report.

For example, `python patient_analytics.py --count 10 --seed 42` prints a text
report, while adding `--csv` prints CSV. A seed makes the generated random
cohort repeatable, but reported ages depend on the date when the program runs.

## Limitations

This is a self-contained demonstration, not a validated clinical model. It
uses fixed illustrative thresholds and a simple point system, does not read
from or write to a patient database, and does not provide clinical
interpretation. Do not use its scores, ranges, or reports to guide patient
care.
