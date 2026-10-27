# Patient Analytics Module: Technical Guide

## Purpose and scope

`patient_analytics.py` is a self-contained Python training example that generates fictional patient records, assesses them with a simple rule-based scoring system, and produces cohort reports. It demonstrates data classes, enums, seeded random generation, decorators, context managers, typing protocols, aggregation, CSV output, and a command-line interface.

**This is not a clinical application.** All names, identifiers, measurements, reference ranges, and rules are synthetic and illustrative. The scores and flags are not medical advice and must not be used to make decisions about real patients.

## Runtime and dependencies

The module uses only the Python standard library. Its type syntax requires Python 3.10 or later. Run it from a shell:

```bash
python patient_analytics.py
```

By default, it generates 25 fictional patients and prints a text report. Options:

| Option | Default | Description |
|---|---:|---|
| `-n`, `--count` | `25` | Number of fictional patients to generate |
| `-s`, `--seed` | `1337` | Seed used by the synthetic-data random-number generator |
| `--csv` | Off | Print assessment rows as CSV instead of the text report |

Examples:

```bash
python patient_analytics.py --count 10 --seed 42
python patient_analytics.py -n 10 --csv
```

The module can also be imported and its functions called directly. Importing it does not run the CLI; the `main()` entry point runs only when the file is executed as a script.

## Data model and reference data

- **`Sex`** is an enum with `FEMALE`, `MALE`, and `OTHER` values.
- **`RiskTier`** represents `LOW`, `MODERATE`, `HIGH`, or `CRITICAL`. `RiskTier.from_score()` maps scores below 2 to low, 2–4 to moderate, 5–7 to high, and 8 or more to critical.
- **`Vitals`** is an immutable data class containing systolic and diastolic blood pressure, heart rate, glucose, BMI, and temperature in Celsius. `as_dict()` returns those measurements by name; `abnormal_flags()` compares each value with `REFERENCE_RANGES` and returns only values outside the range, labeled `"low"` or `"high"`.
- **`Patient`** holds an MRN-like synthetic identifier, name, birth date, sex, conditions, and dated vital-sign encounters. Its `age` property calculates age from the current date. `latest_vitals()` returns the vitals from the most recent encounter, or `None` if there are no encounters.
- **`RiskAssessment`** associates a patient with a numeric score and the reasons that contributed to it; its `tier` property derives the corresponding tier.

The module-level name, condition, and reference-range lists are fabricated. The reference ranges are used by `Vitals.abnormal_flags()`; the risk-scoring rules have their own thresholds and do not use those ranges directly.

## Synthetic-data generation

`generate_patients(count, seed=RANDOM_SEED)` creates the requested number of fictional patients. A local `random.Random` instance is initialized from the supplied seed, then used to choose names, sex, conditions, birth dates, and measurements. Each patient receives one to four dated encounters. `_random_vitals()` generates the measurements using normal-distribution samples rounded to one decimal place.

Using the same seed reproduces the random choices and measurements. It does **not** make every report byte-for-byte identical: ages and risk assessments use the current date, while report and audit timestamps also change.

## Risk assessment

`assess_patient(patient, rules=DEFAULT_RULES)` runs each rule against a patient, sums the points for rules that match, and records their explanations. The default rules inspect the latest available vitals and patient information:

| Rule | Match condition | Points |
|---|---|---:|
| High blood pressure | Systolic BP ≥ 140 or diastolic BP ≥ 90 | 3 |
| Hyperglycemia | Glucose ≥ 140 | 2 |
| Elevated BMI | BMI ≥ 30 | 2 |
| Multiple conditions | At least two listed conditions | 1 |
| Advanced age | Age ≥ 65 | 1 |

A patient without encounters can still match the conditions and age rules; vital-sign rules do not match without latest vitals. The rules are injectable, so callers may supply a different sequence of rules. These thresholds are examples only, not validated clinical criteria.

## Reporting and exports

- `cohort_statistics(patients)` calculates mean and median latest glucose, population standard deviation of latest BMI, and maximum latest glucose. It returns an empty dictionary when no patient has latest vitals.
- `tier_breakdown(assessments)` counts assessments by tier.
- `condition_prevalence(patients)` counts each listed condition and orders results by descending count.
- `write_csv(assessments, stream)` writes a header and one row per assessment. Columns are `mrn`, `name`, `age`, `score`, `tier`, and `reasons`.
- `render_report(patients)` assesses and sorts patients by descending score, then renders cohort statistics, tier counts, condition prevalence, and up to five highest-scoring patients as text.

The CLI chooses either `write_csv()` or `render_report()` based on `--csv`. The CSV contains synthetic identifiers and names, but it is still example output and should not be mistaken for real patient data.

## Audit behavior

The `@audited` decorator records a timestamp, action label, and function name in the module-level `_AUDIT_TRAIL` whenever the wrapped function is called. It is applied to `generate_patients()` and `assess_patient()`. `audit_session(label)` is a context manager that adds begin and end markers, including when an exception occurs inside the context. The CLI wraps its processing in an `"cohort-run"` audit session.

The audit trail is held only in memory. The CLI does not print or persist it, and it is not a secure or durable audit system.

## Main execution flow

1. `main()` parses the command-line arguments.
2. The CLI opens an audit session and calls `generate_patients()`.
3. In CSV mode, it assesses each patient and writes CSV to standard output. Otherwise, `render_report()` creates and prints a text report.
4. `main()` returns exit code `0`; the script passes that code to `SystemExit`.

## Limitations

- The records, measurements, thresholds, and outputs are entirely fabricated.
- The random seed controls the generator but does not freeze dates or timestamps.
- The audit trail is process-local and is neither persisted nor designed for compliance.
- The module is a teaching example, not a validated analytics, diagnostic, or production data-processing system.
