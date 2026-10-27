# `patient_analytics.py` Technical Guide

## Purpose and safety

This module is a Python training example that generates fictional patient records, assigns rule-based risk scores, and produces cohort reports. The records and reference values are fabricated. The module is not a clinical system and must not be used for medical advice, real patient data, or care decisions.

## Module structure

The code is organized into these layers:

1. **Reference data and enums** define synthetic names, vital-sign ranges, the `Sex` values, and the risk tiers.
2. **Data models** represent vital measurements, patients, and risk assessments.
3. **Audit utilities** record decorated function calls and bracket a run with audit-session markers.
4. **Synthetic data generation** creates reproducible patients and encounter histories.
5. **Rules engine** evaluates each patient and turns matching rules into a score and reasons.
6. **Reporting** calculates cohort summaries and writes either a text report or CSV.
7. **Command-line entry point** connects generation and reporting to command-line arguments.

## Data model

- `Vitals` is a frozen dataclass containing systolic and diastolic blood pressure, heart rate, glucose, BMI, and temperature. `as_dict()` exposes those values by metric name; `abnormal_flags()` compares each value with `REFERENCE_RANGES` and returns `"low"` or `"high"` flags.
- `Patient` stores a fictional MRN, name, birth date, sex, conditions, and dated vital-sign encounters. Its `age` property calculates age using the current date. `latest_vitals()` returns the measurements from the most recent encounter, or `None` when there are no encounters.
- `RiskAssessment` groups a patient with the accumulated score and the reasons that contributed to it. Its `tier` property maps the score to a `RiskTier`.

The normal-range flags and risk rules are separate mechanisms: `abnormal_flags()` uses `REFERENCE_RANGES`, while the default assessment rules use their own thresholds.

## Synthetic data generation

`generate_patients(count, seed=RANDOM_SEED)` creates `count` fictional patients using a local `random.Random` instance. Supplying the same seed and count reproduces the same generated records. Each patient receives a randomly selected set of conditions and one to four dated encounters. Measurements are sampled around fixed means with Gaussian variation.

Although random generation is seeded by default, some displayed values can vary between runs: patient age depends on the date the report is generated, and report and audit timestamps use the current time.

## Risk assessment

`assess_patient(patient, rules=DEFAULT_RULES)` runs each rule against a patient, sums the points from matching rules, and collects their reason strings. The default rules use the patient's latest vital signs, condition count, and age:

| Rule | Condition | Points |
|---|---|---:|
| Elevated blood pressure | Systolic blood pressure ≥ 140 or diastolic blood pressure ≥ 90 | 3 |
| Hyperglycemia | Glucose ≥ 140 | 2 |
| Elevated BMI | BMI ≥ 30 | 2 |
| Multiple conditions | At least two listed conditions | 1 |
| Advanced age | Age ≥ 65 | 1 |

`RiskTier.from_score()` assigns **low** to scores below 2, **moderate** to 2–4, **high** to 5–7, and **critical** to 8 or more. These are illustrative training rules, not validated clinical criteria.

## Reporting

- `cohort_statistics()` summarizes the latest glucose and BMI measurements across patients. It returns an empty dictionary when no patients have latest measurements.
- `tier_breakdown()` counts assessments by risk tier.
- `condition_prevalence()` counts listed conditions and sorts them by frequency, highest first.
- `write_csv()` writes a header and one row per assessment, including MRN, name, age, score, tier, and reasons.
- `render_report()` assesses and sorts patients by descending score, then renders cohort statistics, tier counts, condition prevalence, and up to five top-scoring patients.

The CSV and text reports contain names and MRNs generated for this example. They are still fictional training output and should not be mixed with real patient information.

## Audit behavior

The `@audited` decorator adds a timestamped entry to the module-level `_AUDIT_TRAIL` whenever a decorated function is called. `audit_session()` adds begin and end markers, including when an exception occurs inside the context. The command-line entry point uses this context manager, but it does not print or export the audit trail.

## Command-line use

Run the module with Python from the repository root:

```shell
python Participants/Amy_Hughes-Jones/patient_analytics.py
```

By default, it generates 25 patients and prints a text report. Options are:

| Option | Effect |
|---|---|
| `-n`, `--count` | Number of fictional patients to generate (default: `25`) |
| `-s`, `--seed` | Random seed (default: `1337`) |
| `--csv` | Print CSV instead of the text report |

For example, `python Participants/Amy_Hughes-Jones/patient_analytics.py --count 10 --seed 42 --csv` produces a CSV for a reproducible cohort of ten fictional patients.
