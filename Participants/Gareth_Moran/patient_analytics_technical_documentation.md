# Patient Analytics Module: Technical Documentation

## Purpose and scope

`patient_analytics.py` is a self-contained training example of a small analytics pipeline. It generates fictional patients and encounter measurements, applies configurable rules to produce coarse risk scores, and reports cohort summaries. The data and thresholds are illustrative only: this module is not clinical software, must not be used for care decisions, and does not contain real patient information.

## Requirements and execution

The module uses only the Python standard library and requires Python 3.10 or later. Run it from a terminal:

```bash
python Participants/Gareth_Moran/patient_analytics.py
```

By default, it generates 25 patients with seed `1337` and prints a text report. Options are:

| Option | Default | Description |
|---|---:|---|
| `-n`, `--count` | `25` | Number of fictional patients to generate |
| `-s`, `--seed` | `1337` | Seed for reproducible synthetic data |
| `--csv` | Off | Print assessment rows as CSV instead of the text report |

For example, `python Participants/Gareth_Moran/patient_analytics.py --count 10 --seed 42 --csv` prints a CSV header and ten assessment rows. Output is written to standard output; the program does not save reports or patient data to files.

## Processing flow

1. **Generate data:** `generate_patients` uses a local seeded random-number generator to create patient records, conditions, and one to four dated encounters. `_random_vitals` generates six measurements for each encounter.
2. **Assess patients:** `assess_patient` runs each configured rule against a patient, sums the returned points, and collects the corresponding reasons. By default, rules inspect the latest encounter's blood pressure, glucose, and BMI, as well as the number of listed conditions and the patient's age.
3. **Summarize and render:** `render_report` sorts assessments by score and combines cohort statistics, risk-tier counts, condition prevalence, and up to five top-scoring records. Alternatively, the command-line CSV option uses `write_csv`.

The `Patient`, `Vitals`, and `RiskAssessment` dataclasses represent the main data structures. `Sex` and `RiskTier` are enums. The rules are callables, so `assess_patient` can also receive a custom sequence of rules.

## Risk scoring

The default rules assign points as follows:

| Rule condition | Points |
|---|---:|
| Latest systolic blood pressure is at least 140 or diastolic is at least 90 | 3 |
| Latest glucose is at least 140 | 2 |
| Latest BMI is at least 30 | 2 |
| At least two listed conditions | 1 |
| Age is at least 65 | 1 |

Scores map to tiers as follows: `0–1` low, `2–4` moderate, `5–7` high, and `8+` critical. These are demonstration rules and thresholds, not validated clinical criteria. `Vitals.abnormal_flags` separately compares measurements with the module's illustrative reference ranges; those flags are not used in the risk score.

## Reports and supporting utilities

- The text report includes generation time, patient count, mean and median latest glucose, population standard deviation of latest BMI, maximum latest glucose, risk-tier counts, condition counts, and the five highest-scoring patients.
- The CSV output contains `mrn`, `name`, `age`, `score`, `tier`, and `reasons`.
- `cohort_statistics`, `tier_breakdown`, and `condition_prevalence` provide reusable summaries.
- The `audited` decorator appends calls to a module-level in-memory audit trail. `audit_session` adds begin/end markers, but the trail is not persisted or included in command-line output.

## Important limitations

- All names, medical record numbers, conditions, encounter dates, and measurements are fabricated for training.
- A fixed seed makes generated data repeatable, but displayed ages depend on the date when the program is run.
- Generated identifiers are random examples and are not guaranteed to be unique.
- Reference ranges, scoring rules, and outputs have no diagnostic or treatment validity.
- The module has no database, external service, file-writing, or real-patient data integration.
