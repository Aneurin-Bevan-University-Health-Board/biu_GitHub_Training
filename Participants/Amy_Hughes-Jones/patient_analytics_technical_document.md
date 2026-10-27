# `patient_analytics.py` — Technical Documentation

## Purpose and scope

`patient_analytics.py` is a self-contained training example of a small patient-cohort analytics pipeline. It generates fictional patients and encounter measurements, applies configurable demonstration risk rules, and produces a text or CSV report.

**This module is not for clinical use.** Its data and thresholds are fabricated and are not medical advice or a validated clinical assessment.

## Requirements and dependencies

The module uses only the Python standard library. Its type annotations use modern syntax, including `X | None`, so it requires Python 3.10 or later.

## Main components

### Reference data and types

- `RANDOM_SEED` provides the default random seed. Name lists, a condition list, and `REFERENCE_RANGES` provide fabricated inputs.
- `Sex` enumerates the generated sex values.
- `RiskTier` defines `low`, `moderate`, `high`, and `critical`. `RiskTier.from_score()` maps scores below 2 to low, 2–4 to moderate, 5–7 to high, and 8 or more to critical.
- `Vitals` is a frozen dataclass holding six measurements. `as_dict()` converts them to a mapping, and `abnormal_flags()` compares each value with its fabricated reference range and returns only values outside that range.
- `Patient` stores a fictional identifier, demographic fields, conditions, and dated vital-sign encounters. `full_name` combines the names; `age` calculates age against the current date; `latest_vitals()` returns the measurements from the latest dated encounter or `None` when there are no encounters.
- `RiskAssessment` pairs a patient with a total score and rule-hit reasons; its `tier` property derives the corresponding `RiskTier`.

### Synthetic data generation

`generate_patients(count, seed=RANDOM_SEED)` creates `count` fictional patients. It uses a local `random.Random(seed)` instance, so the generated data is repeatable for the same count and seed without changing the process-wide random generator. Each patient receives fabricated demographics, zero to three conditions, and one to four encounters with generated vitals.

`_random_vitals()` samples values from normal distributions and rounds them to one decimal place. The generated data is illustrative only; it is not guaranteed to be clinically realistic. The generator does not validate `count`: a negative count produces an empty list.

### Risk rules and assessment

Each rule accepts a `Patient` and returns either `(points, reason)` or `None`. The default rules award:

| Rule | Condition | Points |
|---|---|---:|
| High blood pressure | Latest systolic blood pressure is at least 140, or diastolic is at least 90 | 3 |
| Hyperglycemia | Latest glucose is at least 140 | 2 |
| Elevated BMI | Latest BMI is at least 30 | 2 |
| Multiple conditions | Patient has at least two listed conditions | 1 |
| Advanced age | Patient is at least 65 years old | 1 |

`assess_patient()` runs the provided rules (the default is `DEFAULT_RULES`), sums their points, and collects their reasons. Callers can supply a different sequence of rules. The resulting score and tier are demonstration outputs, not clinical recommendations.

### Audit trail

`@audited(action)` is a decorator factory that appends a timestamp, action label, and function name to the module-level `_AUDIT_TRAIL` whenever the decorated function is called. It is applied to `generate_patients()` and `assess_patient()`.

`audit_session(label)` is a context manager that appends begin and end markers around a block, including when that block exits with an exception. The trail is held only in memory; the command-line interface does not print or persist it.

### Reporting helpers

- `cohort_statistics()` calculates mean and median latest glucose, population standard deviation of latest BMI, and maximum latest glucose. Patients without encounters are excluded; if there are no glucose values, it returns an empty dictionary. BMI standard deviation is `0.0` for a single value.
- `tier_breakdown()` counts assessments by tier.
- `condition_prevalence()` counts listed conditions and returns them in descending frequency order.
- `write_csv()` writes a header and one row per assessment to any text stream with a `write()` method.
- `render_report()` assesses and sorts patients by descending score, then renders cohort statistics, tier counts, condition prevalence, and up to five top-scoring patients as text.

## Command-line interface

Run the module directly to generate and print a text report:

```shell
python patient_analytics.py
```

Options:

| Option | Default | Description |
|---|---:|---|
| `-n`, `--count` | `25` | Number of fictional patients to generate |
| `-s`, `--seed` | `1337` | Seed used for repeatable data generation |
| `--csv` | Off | Write assessment results as CSV instead of the text report |

Examples:

```shell
python patient_analytics.py --count 10 --seed 42
python patient_analytics.py --count 10 --csv
```

The command-line workflow opens an `audit_session`, generates the cohort, then either assesses patients and writes CSV to standard output or renders the text report. The generated records are not saved to files.

## Important behavior and limitations

- A fixed seed makes generated demographic and measurement values repeatable, but report timestamps and age calculations depend on the current date and time.
- The default generator creates encounters for each generated patient, but helper functions also handle patients without encounter data.
- The audit trail is a module-level in-memory list and is not reset when a session ends.
- Names and MRNs are randomly generated examples. Do not treat the output as real patient data or use this module for patient care.

## Source map

The implementation is in `patient_analytics.py`: constants and enums (lines 42–87), data model (94–155), audit utilities (162–187), generation (194–242), rules and assessment (249–313), reporting (321–403), and CLI (411–437).
