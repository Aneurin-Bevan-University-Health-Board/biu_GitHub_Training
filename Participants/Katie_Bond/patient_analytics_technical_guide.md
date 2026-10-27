# Patient Analytics Module: Technical Guide

## Purpose and safety

`patient_analytics.py` is a Python training example that generates fictional
patients, assigns illustrative risk scores, and produces cohort summaries. Its
names, medical record numbers, conditions, and measurements are fabricated.
This module is not a clinical tool: its thresholds and scores are not validated
for diagnosis, treatment, or decisions about real patients. Do not use it with
real patient data.

The module is self-contained and uses only the Python standard library. Its
main stages are:

1. Generate a reproducible synthetic cohort.
2. Assess each patient's latest available measurements and conditions.
3. Summarize the cohort and render either a text report or CSV.

## Data model

- **`Sex`** is an enum with `FEMALE`, `MALE`, and `OTHER` values.
- **`RiskTier`** contains the `low`, `moderate`, `high`, and `critical`
  categories. `RiskTier.from_score()` maps a numeric score to a category.
- **`Vitals`** is a frozen dataclass containing systolic and diastolic blood
  pressure, heart rate, glucose, BMI, and temperature in Celsius.
  `as_dict()` returns these measurements by name, and `abnormal_flags()`
  compares them with the illustrative `REFERENCE_RANGES`.
- **`Patient`** stores a fictional MRN, name, birth date, sex, conditions, and
  a list of `(date, Vitals)` encounters. Its `age` property calculates age
  against the current date; `latest_vitals()` returns the measurements from
  the most recent encounter, or `None` if there are no encounters.
- **`RiskAssessment`** associates a patient with a total score and the reasons
  that contributed to it. Its `tier` property derives the corresponding
  `RiskTier`.

## Synthetic data generation

`generate_patients(count, seed=RANDOM_SEED)` creates `count` fictional
patients. It uses a local `random.Random` instance, seeded by default with
`1337`, so the generated cohort can be reproduced by passing the same count
and seed. The generator chooses names and conditions from fixed lists, creates
one to four dated encounters per patient, and uses Gaussian distributions to
produce the measurements.

The generated birth dates span 1945–2010. The encounter dates are generated
relative to each birth date, rather than from real clinical records. Reusing a
seed reproduces the generated fields, but a full report is not completely
time-invariant: patient ages and report timestamps depend on the date and time
when it is run.

## Risk rules and scoring

`assess_patient(patient, rules=DEFAULT_RULES)` runs each rule against the
patient's latest vitals where applicable. A matching rule contributes points
and a human-readable reason; the points are added to produce the total score.
The default rules are:

| Rule | Match condition | Points |
|---|---|---:|
| Elevated blood pressure | Latest systolic pressure ≥ 140 **or** diastolic pressure ≥ 90 | 3 |
| Hyperglycemia | Latest glucose ≥ 140 | 2 |
| Elevated BMI | Latest BMI ≥ 30 | 2 |
| Multiple conditions | At least two listed conditions | 1 |
| Advanced age | Age ≥ 65 | 1 |

Blood pressure, glucose, and BMI rules do not match when the patient has no
encounters. The conditions and age rules can still contribute in that case.
Callers can supply another sequence of `Rule` functions to `assess_patient`;
each rule returns `(points, reason)` when it matches, or `None` otherwise.

Scores map to tiers as follows:

| Score | Tier |
|---:|---|
| 0–1 | `low` |
| 2–4 | `moderate` |
| 5–7 | `high` |
| 8 or more | `critical` |

These are example software rules only, not medical guidance.

## Reporting functions

- **`cohort_statistics(patients)`** calculates mean and median latest glucose,
  population standard deviation of latest BMI, and maximum latest glucose.
  Patients without encounters are excluded. It returns an empty dictionary
  when no patient has latest vitals.
- **`tier_breakdown(assessments)`** counts assessments by tier.
- **`condition_prevalence(patients)`** counts each listed condition and orders
  the results by descending count.
- **`write_csv(assessments, stream)`** writes a header and one row per
  assessment. The columns are `mrn`, `name`, `age`, `score`, `tier`, and
  `reasons`.
- **`render_report(patients)`** assesses and sorts patients by descending
  score, then renders cohort statistics, tier counts, condition prevalence,
  and up to five top-scoring patients as text.

## Audit behavior

The `@audited` decorator records calls to decorated functions in the
module-level `_AUDIT_TRAIL`, with a local timestamp, action label, and function
name. `audit_session(label)` appends begin and end markers around a block,
including when that block exits with an exception. The audit trail exists only
in process memory; this example does not persist it or provide a production
audit or security control.

## Command-line interface

Run the module from the repository root:

```shell
python Participants/Katie_Bond/patient_analytics.py
```

Options:

| Option | Default | Description |
|---|---:|---|
| `-n`, `--count` | `25` | Number of fictional patients to generate |
| `-s`, `--seed` | `1337` | Seed used for synthetic data generation |
| `--csv` | Off | Write assessment CSV instead of the text report |

For example, `python Participants/Katie_Bond/patient_analytics.py --count 10 --seed 42`
generates a ten-patient text report, while adding `--csv` writes the CSV
format to standard output. The command-line entry point wraps generation and
output in an audit session.

## Implementation notes

The module also demonstrates type hints, dataclasses, enums, generators,
comprehensions, `functools.reduce`, a `Protocol` for writable text streams,
and a context manager. Its use of standard-library components means no
additional package installation is required.
