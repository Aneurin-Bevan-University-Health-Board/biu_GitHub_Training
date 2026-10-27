# Patient Analytics Module: Technical Overview

## Purpose and scope

`patient_analytics.py` is a self-contained training example that simulates a
clinical analytics workflow using entirely fictional patient data. It
generates a cohort, assesses each patient with a small rules engine, calculates
cohort summaries, and emits either a text report or CSV.

The measurements, reference ranges, names, and medical-looking labels are
illustrative only. This module is not a clinical system and must not be used
for diagnosis, treatment, or decisions about real patients.

## Runtime requirements

- Python 3.10 or later (the module uses modern union syntax and built-in
  collection type annotations).
- No third-party packages; all imports are from the Python standard library.

## Architecture and data flow

The normal command-line flow is:

1. Parse the cohort size, random seed, and output format.
2. Generate fictional patients and their encounter histories.
3. Assess each patient against the configured risk rules.
4. Either aggregate the results into a text report or serialize assessments
   as CSV.
5. Record the work in the module-level audit trail while the audit session is
   open.

The same main operations are also available as Python functions, so the module
can be imported without running the command-line entry point.

## Data model

### `Sex`

An enum with `FEMALE`, `MALE`, and `OTHER` values. The generator selects one
value for each fictional patient.

### `RiskTier`

An enum for the assessment categories `LOW`, `MODERATE`, `HIGH`, and
`CRITICAL`. `RiskTier.from_score(score)` maps scores as follows:

| Score | Tier |
|---:|---|
| 0–1 | Low |
| 2–4 | Moderate |
| 5–7 | High |
| 8 or more | Critical |

### `Vitals`

A frozen dataclass that stores systolic and diastolic blood pressure, heart
rate, glucose, BMI, and temperature in Celsius. `as_dict()` returns the
measurements as a mapping. `abnormal_flags()` compares each measurement with
`REFERENCE_RANGES` and returns only out-of-range values, marked `"low"` or
`"high"`.

These range checks are descriptive examples. The risk rules do not call
`abnormal_flags()`; they use their own thresholds.

### `Patient`

A mutable dataclass holding a fictional medical record number (MRN), name,
birth date, sex, conditions, and `(date, Vitals)` encounter pairs. Its
properties provide a full name and an age calculated against the current date.
`latest_vitals()` returns the vitals from the latest-dated encounter, or
`None` if the patient has no encounters.

### `RiskAssessment`

Stores a patient, their total points, and the human-readable reasons that
earned points. Its `tier` property derives the corresponding `RiskTier`.

## Synthetic data generation

`generate_patients(count, seed=RANDOM_SEED)` creates `count` fictional
patients. It uses a local `random.Random` instance, so passing the same seed
and count produces the same generated identities, conditions, encounter dates,
and measurements. The default seed is `1337`.

Each generated patient receives zero to three conditions from
`CONDITION_POOL` and one to four encounters. `_random_vitals()` samples values
from normal distributions and rounds them to one decimal place. The generator
does not validate that generated measurements fall within the illustrative
reference ranges.

The age property is evaluated at runtime using `date.today()`. As a result,
ages in a report can change over time even when the generated cohort is
otherwise identical. Encounter dates are generated relative to the birth date
and are not constrained to be in the past.

## Risk assessment

`assess_patient(patient, rules=DEFAULT_RULES)` applies each rule to the
patient, collects the non-empty `(points, reason)` results, sums the points,
and returns a `RiskAssessment`. The default rules inspect the latest vitals
where applicable:

| Rule | Condition | Points |
|---|---|---:|
| High blood pressure | Systolic BP ≥ 140 or diastolic BP ≥ 90 | 3 |
| Hyperglycemia | Glucose ≥ 140 | 2 |
| Elevated BMI | BMI ≥ 30 | 2 |
| Multiple conditions | At least two listed conditions | 1 |
| Advanced age | Age ≥ 65 | 1 |

`Rule` is a callable type alias for a function accepting a `Patient` and
returning either `(points, reason)` or `None`. Callers can pass a different
sequence of rules to `assess_patient`; `DEFAULT_RULES` defines the standard
configuration.

## Reporting and exports

- `cohort_statistics(patients)` returns mean and median latest glucose,
  population standard deviation of latest BMI, and maximum latest glucose.
  Patients without encounters are excluded. If there are no glucose values,
  the result is an empty dictionary; a single BMI value has a standard
  deviation of `0.0`.
- `tier_breakdown(assessments)` returns a `Counter` keyed by tier value.
- `condition_prevalence(patients)` counts each listed condition and sorts the
  result from most common to least common.
- `write_csv(assessments, stream)` writes a header and one row per assessment
  to a text stream. The columns are MRN, name, age, score, tier, and
  semicolon-separated reasons.
- `render_report(patients)` assesses and sorts patients by descending score,
  then returns a formatted text report with cohort statistics, tier counts,
  condition prevalence, and up to five highest-scoring patients.

The CSV and text report include generated identifiers and names. Although the
example data is fictional, treat any output as training material rather than
as a clinical record.

## Audit behavior

`audited(action)` is a decorator factory. Functions decorated with it append a
timestamp, action label, and function name to the module-level `_AUDIT_TRAIL`
before the function runs. `generate_patients` and `assess_patient` use this
decorator.

`audit_session(label)` is a context manager that appends begin and end markers
around a block of work, including when that block exits with an exception.
It yields the same in-memory list. The audit trail is process-local, has no
persistent storage, and is not included in either report format.

## Command-line interface

Run the module as a script:

```text
python patient_analytics.py [-h] [-n COUNT] [-s SEED] [--csv]
```

| Option | Default | Description |
|---|---:|---|
| `-h`, `--help` | — | Show command-line help. |
| `-n`, `--count` | 25 | Number of fictional patients to generate. |
| `-s`, `--seed` | 1337 | Random seed for reproducibility. |
| `--csv` | Off | Emit assessment CSV instead of the text report. |

Without `--csv`, the command prints the human-readable cohort report. With
`--csv`, it assesses the generated patients and writes CSV to standard output.
The `main(argv=None)` function supports passing an argument sequence directly,
which is useful when invoking it from other Python code or tests.

## Implementation notes and limitations

- All data is generated in memory; there is no database, network, or external
  service integration.
- `RANDOM_SEED` makes pseudorandom generation repeatable, but it does not make
  the full report byte-for-byte stable: generated timestamps and ages depend
  on the current date and time.
- `count` is passed to `range()` without explicit validation. A negative count
  produces an empty cohort; a non-integer is rejected by Python.
- `render_report()` handles an empty cohort, but its cohort-statistics section
  has no statistic rows because `cohort_statistics()` returns `{}`.
- `SupportsWrite` is a `Protocol` describing the `write(str)` interface
  required by `write_csv`, allowing compatible text streams without requiring
  a specific concrete stream type.
- The reference ranges, thresholds, units, and risk tiers are teaching
  examples, not validated medical criteria.
