# Technical guide: `patient_analytics.py`

## Purpose and scope

`patient_analytics.py` is a self-contained training example of a small patient-cohort analytics pipeline. It creates fictional patients and observations, applies a transparent rule-based score, and produces either a readable text report or CSV output. All names, identifiers, conditions, and measurements are fabricated. This module is not a clinical tool, must not be used to make care decisions, and must not be connected to real patient data.

## Pipeline overview

The command-line workflow is:

1. Generate a cohort of fictional patients using a seeded random-number generator.
2. Select each patient's latest encounter and apply the default risk rules.
3. Aggregate cohort statistics, risk-tier counts, and condition prevalence.
4. Print either a text report or CSV rows.
5. Record function calls and the run boundary in an in-memory audit trail.

The same components can also be called directly from Python.

## Data model

- **`Sex`** is an enum with `FEMALE`, `MALE`, and `OTHER` values.
- **`RiskTier`** defines `low`, `moderate`, `high`, and `critical`. `from_score()` maps scores below 2 to low, 2–4 to moderate, 5–7 to high, and 8 or more to critical.
- **`Vitals`** is an immutable dataclass containing systolic and diastolic blood pressure, heart rate, glucose, BMI, and temperature. `as_dict()` returns the measurements; `abnormal_flags()` compares each with `REFERENCE_RANGES` and marks values as low or high.
- **`Patient`** stores a fabricated medical-record number, name, birth date, sex, conditions, and dated vital-sign encounters. `full_name` formats the name, `age` calculates age against the current date, and `latest_vitals()` returns the vitals from the latest dated encounter or `None`.
- **`RiskAssessment`** holds a patient, their total score, and the reasons that contributed to it. Its `tier` property derives the corresponding `RiskTier`.

## Data generation

`generate_patients(count, seed=RANDOM_SEED)` creates `count` patients with one to four encounters each. The module-level default seed is `1337`; passing the same seed and count makes the generated records repeatable. Names, conditions, demographics, encounter dates, and measurements all come from fabricated reference data and random values. Each vital measurement is generated around a fixed mean using a Gaussian distribution.

The generator is decorated with `@audited("generate")`. This records a timestamped function-call entry in the module-level `_AUDIT_TRAIL`.

## Risk rules and scoring

`DEFAULT_RULES` contains five functions. A rule returns `(points, reason)` when it matches, or `None` otherwise:

| Rule | Match | Points |
|---|---|---:|
| High blood pressure | Latest systolic pressure ≥ 140 or diastolic pressure ≥ 90 | 3 |
| Hyperglycemia | Latest glucose ≥ 140 | 2 |
| Elevated BMI | Latest BMI ≥ 30 | 2 |
| Multiple conditions | At least two listed conditions | 1 |
| Advanced age | Age ≥ 65 | 1 |

`assess_patient()` runs the provided rules (the defaults unless overridden), sums the points, and collects the corresponding reasons. The tier thresholds are defined separately by `RiskTier.from_score()`. These are illustrative training rules, not validated clinical criteria. Although `Vitals.abnormal_flags()` uses the reference ranges, those flags are not currently inputs to the scoring rules.

## Reporting functions

- **`cohort_statistics(patients)`** calculates mean and median latest glucose, population standard deviation of latest BMI, and maximum latest glucose. Patients without encounters do not contribute; an empty set of latest glucose values returns an empty dictionary.
- **`tier_breakdown(assessments)`** counts assessments in each tier.
- **`condition_prevalence(patients)`** counts each condition and sorts the results from most common to least common.
- **`write_csv(assessments, stream)`** writes a header and one row per assessment to a text stream that supports `write()`.
- **`render_report(patients)`** assesses and sorts patients by descending score, then renders cohort statistics, tier counts, condition counts, and up to five top-scoring patients.

## Audit behavior

`audited(action)` is a decorator factory. A decorated function appends a timestamp, action label, and function name to `_AUDIT_TRAIL` before calling the function. `audit_session(label)` is a context manager that appends begin and end markers; its `finally` block ensures the end marker is recorded even if the enclosed operation raises an exception. The trail is held only in process memory and is not included in the report or CSV and is not persisted.

## Command-line use

Run the module with Python 3.10 or later; it uses only the Python standard library.

```shell
python patient_analytics.py
python patient_analytics.py --count 10 --seed 42
python patient_analytics.py --count 10 --csv
```

Options:

- `-n`, `--count`: number of fictional patients to generate (default: `25`).
- `-s`, `--seed`: random seed (default: `1337`).
- `--csv`: emit CSV instead of the text report.

The `main()` function returns exit status `0` after a successful run. When importing the file, the `if __name__ == "__main__"` guard prevents the CLI from running automatically.

## Implementation notes and limitations

- Generated data is repeatable for a fixed seed and count, but report values such as age depend on the date the program is run. Audit timestamps and the report generation timestamp also vary between runs.
- The risk assessment considers only the latest encounter's vitals, alongside the patient's condition count and age; earlier encounters are not used in scoring.
- The code is designed for learning Python and GitHub Copilot concepts, including dataclasses, enums, decorators, closures/callables, generators, comprehensions, reductions, protocols, and context managers.
- Do not replace the fabricated data with identifiable or real patient information. This example does not implement clinical validation, access controls, or production data handling.
