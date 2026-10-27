# Technical Documentation: `patient_analytics.py`

## Purpose and scope

`patient_analytics.py` is a self-contained training example of a small clinical-style analytics pipeline. It generates fictional patients and encounter measurements, calculates rule-based risk scores, summarizes a cohort, and prints either a text report or CSV. The module uses only the Python standard library.

All records and measurements are fabricated. The reference ranges and scoring rules are illustrative only: this program is not a clinical decision-support system and must not be used to assess real people or guide care.

## Main components

### Reference data and types

- `RANDOM_SEED` sets the default seed for reproducible synthetic records. Name lists, the condition pool, and `REFERENCE_RANGES` provide generated values and illustrative ranges.
- `Sex` enumerates the generated sex categories. `RiskTier` defines `low`, `moderate`, `high`, and `critical`; `RiskTier.from_score()` maps scores below 2 to low, 2–4 to moderate, 5–7 to high, and 8 or above to critical.
- `Vitals` is a frozen dataclass containing six measurements. `as_dict()` exposes them as a mapping, while `abnormal_flags()` compares each measurement with `REFERENCE_RANGES` and returns a `"low"` or `"high"` flag for values outside the range.
- `Patient` stores a fictional identifier, demographic fields, conditions, and dated vital-sign encounters. Its `age` is calculated against the current date; `latest_vitals()` returns the measurements from the latest encounter or `None` when there are no encounters.
- `RiskAssessment` groups a patient, their score, and the reasons that contributed to it. Its `tier` property derives the corresponding `RiskTier`.

### Audit helpers

`audited(action)` is a decorator factory. It records a timestamp, action label, and function name in the module-level `_AUDIT_TRAIL` whenever a decorated function is called, then calls the function. `audit_session(label)` is a context manager that adds begin and end markers to the same list, including the end marker if the block exits with an exception.

The audit trail is held in memory and is not written to a file or included in the reports. The CLI uses the context manager for the cohort run; `generate_patients()` and `assess_patient()` are decorated.

### Synthetic data generation

`generate_patients(count, seed)` creates `count` fictional patients using a local `random.Random` instance. Reusing the same seed produces the same generated input data. Each patient receives a generated birth date, identifier, name, sex, zero to three conditions, and one to four dated encounters. `_random_vitals()` creates each encounter's measurements from fixed normal-distribution parameters.

### Risk scoring

`assess_patient(patient, rules)` runs each supplied rule, adds the points from rules that match, and collects their explanations. By default, `DEFAULT_RULES` checks:

| Rule | Match condition | Points |
|---|---|---:|
| High blood pressure | Latest systolic measurement is at least 140 or diastolic is at least 90 | 3 |
| Hyperglycemia | Latest glucose is at least 140 | 2 |
| Elevated BMI | Latest BMI is at least 30 | 2 |
| Multiple conditions | Patient has at least two listed conditions | 1 |
| Advanced age | Patient is at least 65 years old | 1 |

Rules that require measurements use only the latest encounter. A patient without encounters therefore does not match those measurement rules, but can still match condition or age rules. These thresholds and scores are example logic, not validated clinical criteria. `REFERENCE_RANGES` and `Vitals.abnormal_flags()` are separate from the risk rules; the risk assessment does not call `abnormal_flags()`.

### Cohort reporting and CSV

- `cohort_statistics()` calculates mean and median glucose, population standard deviation of BMI, and maximum glucose from patients' latest measurements. It returns an empty dictionary when no glucose measurements are available.
- `tier_breakdown()` counts assessments by risk tier.
- `condition_prevalence()` counts listed conditions and sorts them by descending count.
- `render_report()` assesses and sorts patients by descending score, then builds a text report with cohort statistics, tier counts, condition prevalence, and up to five highest-scoring patients.
- `write_csv()` writes a header and one row per assessment to a text stream. The reasons are joined with semicolons.

## Execution flow

Importing the module defines its constants, types, and functions; the CLI runs only when the file is executed directly. `main()` parses command-line options, opens an audit session, generates the cohort, and either writes CSV or prints the text report.

```text
main()
  ├─ generate_patients(count, seed)
  ├─ if --csv: assess each patient → write_csv()
  └─ otherwise: render_report()
                 ├─ assess each patient → sort scores
                 ├─ calculate cohort statistics and tier counts
                 └─ calculate condition prevalence and list top five
```

## Command-line options

```text
python patient_analytics.py [-h] [-n COUNT] [-s SEED] [--csv]
```

- `-n` / `--count`: number of fictional patients to generate (default: `25`).
- `-s` / `--seed`: random seed for repeatable input data (default: `1337`).
- `--csv`: emit CSV instead of the text report.

For example, `python patient_analytics.py --count 10 --seed 42` prints the text report for ten generated patients; adding `--csv` selects CSV output. The current date affects patient ages and report timestamps, so complete output is not necessarily identical across different run dates, even with the same seed.

## Limitations and operational notes

- The program generates synthetic data in memory and has no database, network, or file input/output integration. CSV is written to standard output.
- The random generator is seeded for repeatable generated inputs; current-date age calculations and timestamps are time-dependent.
- Generated identifiers are random values and the code does not enforce uniqueness across a generated cohort.
- The CLI does not explicitly reject negative patient counts; the generation loop then creates an empty cohort.
- Output includes generated names and identifiers for demonstration. Do not substitute real patient information or treat outputs as clinical advice.
