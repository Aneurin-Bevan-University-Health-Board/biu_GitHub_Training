# Patient analytics example: a plain-language guide

## What this file does

[`patient_analytics.py`](patient_analytics.py) is a Python training example. It
generates fictional patient records, assigns each one a simple score using a
few rules, and prints a summary report or CSV file.

**This is not a clinical tool.** The people and measurements are fabricated.
The thresholds and scoring rules are simplified examples, not medical
guidance. Do not use real patient information with this script.

## Run it

From the repository root, use Python 3.10 or later:

```bash
python Participants/Kate_Davies/patient_analytics.py
```

By default, the script generates 25 fictional patients and prints a text
report. You can change the number of records or choose CSV output:

```bash
python Participants/Kate_Davies/patient_analytics.py --count 10 --seed 42
python Participants/Kate_Davies/patient_analytics.py --count 10 --csv
```

The same seed generates the same fictional records. The report's generated
timestamp and ages can still change over time.

## The data flow

1. **Create fictional records.** `generate_patients` uses a seeded random
   number generator to make names, birth dates, conditions, and one to four
   dated sets of vital signs for each patient.
2. **Look at the latest visit.** `Patient.latest_vitals` selects the vital
   signs from the most recent encounter date.
3. **Apply the scoring rules.** `assess_patient` runs each rule against a
   patient's latest vital signs and other details, adds the points from any
   rules that match, and keeps the reasons.
4. **Summarize the group.** The report calculates basic statistics, counts
   risk tiers and conditions, and lists up to five patients with the highest
   scores. Alternatively, the CSV option writes one row per patient.

## How the score works

Each matching rule adds points:

| Rule | Points |
|---|---:|
| Latest systolic blood pressure is at least 140, or diastolic is at least 90 | 3 |
| Latest glucose is at least 140 | 2 |
| Latest BMI is at least 30 | 2 |
| Patient has at least two listed conditions | 1 |
| Patient is 65 or older | 1 |

The total score maps to a tier:

| Score | Tier |
|---:|---|
| 0–1 | Low |
| 2–4 | Moderate |
| 5–7 | High |
| 8 or more | Critical |

These are deliberately simple programming examples. They should not be
interpreted as a real measure of a person's health or risk. The reference
ranges used by `Vitals.abnormal_flags` are a separate example and do not drive
the risk score.

## The main pieces of Python

- **`Patient` and `Vitals`** are dataclasses: convenient structures for
  holding a patient's details and measurements. `Vitals` is frozen, so its
  measurements cannot be reassigned after creation.
- **`Sex` and `RiskTier`** are enums, which represent a fixed set of choices.
- **Rules** are functions that return points and a reason when a condition
  matches, or `None` when it does not. `DEFAULT_RULES` lists the rules used by
  default; `assess_patient` can also be given a different list.
- **`@audited`** is a decorator that records when selected functions are
  called. **`audit_session`** adds begin and end markers around a run. The
  audit trail stays in memory; this script does not save or print it.
- **Reporting helpers** calculate cohort statistics, count tiers and
  conditions, write CSV, and assemble the text report.

## What the outputs contain

The text report includes the run time, number of generated patients, latest
vital-sign statistics, counts by tier, condition counts, and up to five
highest-scoring records with the reasons for their scores. The CSV output
contains each record's fictional identifier, name, age, score, tier, and
reasons; it does not include the cohort summaries.
