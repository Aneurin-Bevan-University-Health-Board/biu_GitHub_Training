# Patient Analytics Module: Technical Guide

## Purpose and safety

`patient_analytics.py` is a training example that demonstrates a small,
multi-stage analytics pipeline using generated, fictional patient records. The
names, identifiers, and measurements are fabricated. This module is not a
clinical tool, does not provide medical advice, and must not be used with real
patient data or for clinical decisions.

## Overview

The module generates a cohort, assesses each patient with a configurable set
of scoring rules, calculates cohort summaries, and renders either a text report
or CSV. Its main components are:

1. **Reference data and enums** — generated names, conditions, fabricated
   vital-sign ranges, and `Sex` and `RiskTier` enums.
2. **Data model** — `Vitals`, `Patient`, and `RiskAssessment` dataclasses.
3. **Audit utilities** — a decorator and context manager that append activity
   markers to an in-memory audit trail.
4. **Generation and scoring** — seeded synthetic record generation and
   rule-based risk scoring.
5. **Reporting and CLI** — cohort summaries, report formatting, CSV output,
   and command-line argument handling.

## Data model

- `Vitals` stores systolic and diastolic blood pressure, heart rate, glucose,
  BMI, and temperature. `as_dict()` exposes those values by metric name;
  `abnormal_flags()` compares them with `REFERENCE_RANGES` and returns
  out-of-range values as `"low"` or `"high"`.
- `Patient` stores a fictional medical record number, name, birth date, sex,
  conditions, and dated vital-sign encounters. Its `age` property calculates
  age against the current date, and `latest_vitals()` returns the measurements
  from the most recent encounter, or `None` if there are no encounters.
- `RiskAssessment` pairs a patient with a score and the explanations from
  rules that matched. Its `tier` property maps the score to a `RiskTier`.

## Processing and scoring

`generate_patients(count, seed=RANDOM_SEED)` creates each patient with
1–4 encounters. A local `random.Random` instance makes the generated records
repeatable for the same count and seed. The default seed is `1337`. The
generator does not validate `count`; a non-positive count produces an empty
cohort.

`assess_patient(patient, rules=DEFAULT_RULES)` runs each supplied rule against
the patient's latest vitals and conditions, sums the points from matching
rules, and retains their reason strings. The default rules award:

| Rule | Match condition | Points |
|---|---|---:|
| High blood pressure | Systolic BP ≥ 140 or diastolic BP ≥ 90 | 3 |
| Hyperglycemia | Glucose ≥ 140 | 2 |
| Elevated BMI | BMI ≥ 30 | 2 |
| Multiple conditions | At least 2 conditions | 1 |
| Advanced age | Age ≥ 65 | 1 |

`RiskTier.from_score()` assigns **low** for 0–1 points, **moderate** for 2–4,
**high** for 5–7, and **critical** for 8 or more.

## Reporting

- `cohort_statistics()` calculates mean and median glucose, maximum glucose,
  and population standard deviation of BMI from each patient's latest vitals.
  It returns an empty dictionary when there are no glucose measurements.
- `tier_breakdown()` counts assessments by risk tier.
- `condition_prevalence()` counts conditions and sorts them by descending
  frequency.
- `render_report()` assesses and sorts patients by descending score, then
  formats cohort summaries and the five highest-scoring records as text.
- `write_csv()` writes a header and one row per assessment to a text stream.
  The columns are MRN, name, age, score, tier, and reasons.

## Audit behavior

The `@audited` decorator records a timestamp, action label, and function name
when the decorated function is called. `audit_session(label)` adds begin and
end markers around a block, including when that block exits with an exception.
Entries are kept in the module-level `_AUDIT_TRAIL` list; the CLI does not
display or export this list.

## Command-line use

Run the module with Python from the repository root:

```text
python Participants/Jerin_George/patient_analytics.py
```

The command-line options are:

| Option | Default | Description |
|---|---:|---|
| `-n`, `--count` | `25` | Number of fictional patients to generate |
| `-s`, `--seed` | `1337` | Seed used for synthetic data generation |
| `--csv` | Off | Emit CSV instead of the text report |

For example, `python Participants/Jerin_George/patient_analytics.py --count 10 --seed 7 --csv`
generates ten records with seed 7 and writes CSV to standard output.

## Implementation notes

- The code uses type hints, a `Protocol` for writable text streams, a
  generator expression, comprehensions, `functools.reduce`, and a context
  manager as training examples.
- Although generated data is seeded, output is not necessarily byte-for-byte
  identical across dates: age is calculated using the current date, and report
  and audit timestamps use the current time.
- Risk scores and reference ranges are illustrative program logic, not
  validated clinical criteria.
