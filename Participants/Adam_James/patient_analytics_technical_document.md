# Patient Analytics Module: Technical Overview

## Purpose and scope

`patient_analytics.py` is a self-contained Python training example that generates fictional patient records, assigns rule-based risk scores, and produces cohort-level reports. All data and reference ranges are fabricated. The module is not a clinical system, does not use real patient data, and must not be used to guide care.

## Runtime requirements

The module uses only the Python standard library and requires Python 3.8 or later for `typing.Protocol` and postponed annotations.

## Data model

- **`Sex`** is an enum with `FEMALE`, `MALE`, and `OTHER` values.
- **`RiskTier`** defines the `low`, `moderate`, `high`, and `critical` categories. `from_score()` maps a score below 2 to low, 2–4 to moderate, 5–7 to high, and 8 or more to critical.
- **`Vitals`** is a frozen dataclass containing systolic and diastolic blood pressure, heart rate, glucose, BMI, and temperature. `as_dict()` exposes these measurements by name; `abnormal_flags()` compares each value with `REFERENCE_RANGES` and returns low/high flags for values outside those ranges.
- **`Patient`** stores a fictional medical record number (MRN), name, birth date, sex, conditions, and dated vital-sign encounters. Its `age` property calculates age using today’s date, and `latest_vitals()` returns the measurements from the most recent encounter, or `None` when there are no encounters.
- **`RiskAssessment`** associates a patient with a total score and the explanations returned by the rules. Its `tier` property derives the corresponding `RiskTier`.

The reference ranges, name lists, and condition pool are constants in the module. They are illustrative only.

## Synthetic data generation

`generate_patients(count, seed=RANDOM_SEED)` creates `count` records using a local `random.Random` instance. The default seed is `1337`, making generated records reproducible for the same Python runtime and input. Each generated patient has zero to three selected conditions and one to four encounters. Encounters contain generated measurements produced by `_random_vitals()`.

The generator is decorated with `@audited("generate")`. The decorator records a timestamp, action label, and function name in the module-level `_AUDIT_TRAIL` whenever the function is called.

## Risk assessment

Rules are functions that accept one `Patient` and return either `(points, reason)` or `None`. The default rules inspect the patient’s latest measurements and record:

| Condition | Points |
|---|---:|
| Systolic blood pressure at least 140 or diastolic blood pressure at least 90 | 3 |
| Glucose at least 140 | 2 |
| BMI at least 30 | 2 |
| At least two listed conditions | 1 |
| Age at least 65 | 1 |

`assess_patient()` runs each supplied rule, adds the points from matching rules, and collects their reason strings. The total is converted into a tier using `RiskTier.from_score()`. The assessment function is also audited. These rules and scores are example logic, not validated clinical criteria.

## Reporting

- `cohort_statistics()` calculates mean and median glucose, population standard deviation of BMI, and maximum glucose using each patient’s latest vitals. If no patients have latest vitals, it returns an empty dictionary; with one BMI value, the standard deviation is `0.0`.
- `tier_breakdown()` counts assessments by tier.
- `condition_prevalence()` counts listed conditions and sorts them from most to least frequent.
- `write_csv()` writes one row per assessment, including MRN, name, current age, score, tier, and joined reasons, to a text stream.
- `render_report()` assesses and sorts patients by descending score, then renders cohort statistics, tier counts, condition prevalence, and up to five highest-scoring patients as text.

## Audit context

`audit_session(label)` is a context manager that adds begin and end markers to `_AUDIT_TRAIL`, including when the enclosed operation exits with an exception. The current CLI uses it around a cohort run. The audit trail remains in memory; the command-line interface does not include it in either report format.

## Command-line interface

Running the file directly invokes `main()`:

```text
python patient_analytics.py [-n COUNT] [-s SEED] [--csv]
```

- `-n` / `--count` sets the number of fictional patients (default: `25`).
- `-s` / `--seed` sets the random seed (default: `1337`).
- `--csv` writes CSV output instead of the text report.

Without `--csv`, the program prints the formatted report. With `--csv`, it assesses each generated patient and writes the CSV header and rows to standard output. `main()` returns `0` on normal completion.

## Design notes and limitations

The rules are configurable through the `rules` argument to `assess_patient()`, and the report writer accepts any object implementing a text `write()` method. The module uses current system time for patient age, report timestamps, and audit timestamps, so those values are not fixed by the random seed. It performs no persistence, external data access, authentication, or validation against real clinical standards.
