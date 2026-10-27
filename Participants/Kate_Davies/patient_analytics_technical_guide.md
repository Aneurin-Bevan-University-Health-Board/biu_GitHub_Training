# Patient Analytics Module: Technical Guide

## Purpose and safety

`patient_analytics.py` is a self-contained training example that demonstrates a
small analytics pipeline using entirely fictional patient data. Names, medical
record numbers, conditions, dates, and measurements are generated for the
example. The module is not medical advice, is not a clinical decision-support
system, and must not be used with real patient data or for clinical decisions.

The implementation uses only the Python standard library. Its main concepts
include dataclasses, enums, seeded randomness, decorators, closures and
callables, generators, protocols, a context manager, aggregation, CSV output,
and a command-line interface.

## Data model

- **`Sex`** is an enum with `FEMALE`, `MALE`, and `OTHER` values.
- **`RiskTier`** defines `low`, `moderate`, `high`, and `critical` categories.
  `from_score()` maps scores below 2 to low, 2–4 to moderate, 5–7 to high, and
  8 or above to critical.
- **`Vitals`** is a frozen dataclass holding six measurements:
  systolic and diastolic blood pressure, heart rate, glucose, BMI, and
  temperature in Celsius. `as_dict()` returns the measurements as a mapping;
  `abnormal_flags()` compares each one with `REFERENCE_RANGES` and returns
  `"low"` or `"high"` flags for values outside those ranges.
- **`Patient`** stores a fictional MRN, name, birth date, sex, conditions, and
  dated vital-sign encounters. Its `age` property calculates age from the
  current date, and `latest_vitals()` returns the measurements from the most
  recent encounter, or `None` when there are no encounters.
- **`RiskAssessment`** associates a patient with a score and the reasons that
  contributed to it. Its `tier` property derives the corresponding `RiskTier`.

## Synthetic data generation

`generate_patients(count, seed=RANDOM_SEED)` creates `count` patients and gives
each one between one and four encounters. Names and conditions are selected
from fixed fabricated lists; measurements are generated around example
distributions by `_random_vitals()`.

The function creates a local `random.Random` instance from its seed, so the
generated data can be reproduced by using the same count and seed. Generated
MRNs are random and are not checked for uniqueness. The default seed is `1337`.

## Risk assessment

`assess_patient(patient, rules=DEFAULT_RULES)` runs each supplied rule against
the patient and adds the points from rules that return a result. Each matching
rule also supplies a human-readable reason. The built-in rules use the latest
vitals, where available, and the patient's conditions and age:

| Rule | Condition | Points |
|------|-----------|-------:|
| High blood pressure | Systolic BP ≥ 140 or diastolic BP ≥ 90 | 3 |
| Hyperglycemia | Glucose ≥ 140 | 2 |
| Elevated BMI | BMI ≥ 30 | 2 |
| Multiple conditions | At least two listed conditions | 1 |
| Advanced age | Age ≥ 65 | 1 |

Rules are callables with the `Rule` shape: they receive a `Patient` and return
either `(points, reason)` or `None`. A caller can pass a different sequence of
rules to `assess_patient()`. These are illustrative thresholds and weights,
not clinically validated criteria. `Vitals.abnormal_flags()` uses the separate
reference ranges and is not used by the risk-scoring rules.

## Reporting

- **`cohort_statistics(patients)`** calculates mean and median glucose,
  population standard deviation of BMI, and maximum glucose using the latest
  available measurements. It returns an empty dictionary when no patients have
  latest measurements.
- **`tier_breakdown(assessments)`** counts assessments in each risk tier.
- **`condition_prevalence(patients)`** counts each listed condition and sorts
  the results by descending count.
- **`write_csv(assessments, stream)`** writes a header and one row per
  assessment to a text stream. The `SupportsWrite` protocol describes the
  required `write()` interface.
- **`render_report(patients)`** assesses and sorts patients by descending
  score, then returns a formatted text report with cohort statistics, tier
  counts, condition prevalence, and up to five top-scoring patients.

## Audit behavior

The `@audited` decorator factory wraps selected functions and appends a
timestamp, action label, and function name to the module-level `_AUDIT_TRAIL`
when they are called. `audit_session(label)` is a context manager that appends
begin and end markers around a block; its `finally` clause ensures the end
marker is added even if the block raises an exception. The command-line flow
uses this context manager. The audit trail is in memory and is not included in
the text or CSV report.

## Command-line use

Run the module with Python 3.10 or later:

```text
python patient_analytics.py
python patient_analytics.py --count 10 --seed 42
python patient_analytics.py --count 10 --csv
```

`--count` (or `-n`) sets the number of generated patients; it defaults to 25.
`--seed` (or `-s`) sets the random seed and defaults to 1337. `--csv` emits CSV
instead of the text report. Without `--csv`, the module prints
`render_report()` output. The `main()` function accepts an optional argument
sequence, which also makes the CLI easier to call from Python code.

## Data flow summary

1. The CLI starts an audit session and generates a cohort.
2. The selected output path either assesses each patient and writes CSV, or
   calls `render_report()` to assess the cohort and assemble text output.
3. Assessments are scored from the latest encounter and patient details; cohort
   summaries aggregate the generated data.
4. The CLI prints the output and closes the audit session.
