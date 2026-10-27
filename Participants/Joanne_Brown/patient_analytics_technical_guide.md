# Patient Analytics Technical Guide

## Purpose and safety

`patient_analytics.py` is a Python training example that demonstrates a small
analytics pipeline using fabricated patient data. Names, medical record
numbers, conditions, and measurements are synthetic. The module is not medical
advice and must not be used for clinical decisions or with real patient data.

The program generates data in memory and prints either a text report or CSV to
standard output. It does not connect to a clinical system or save reports to
files.

## Architecture

The module is organized into five main parts:

1. **Reference data and enums** define the random seed, fabricated name and
   condition lists, example vital-sign ranges, sex categories, and risk tiers.
2. **Data model** represents vital measurements, a patient, and a scored risk
   assessment.
3. **Generation and rules** create a reproducible cohort and apply configurable
   scoring rules.
4. **Reporting** aggregates cohort statistics and formats text or CSV output.
5. **Command-line entry point** parses options and runs generation and output
   inside an audit session.

## Data model

- `Vitals` stores systolic and diastolic blood pressure, heart rate, glucose,
  BMI, and temperature. `as_dict()` provides these values by metric name, and
  `abnormal_flags()` compares each value with `REFERENCE_RANGES` to mark it
  low or high.
- `Patient` stores a fabricated MRN, name, date of birth, sex, conditions, and
  dated vital-sign encounters. Its `age` property calculates age against the
  current date, and `latest_vitals()` returns the measurements from the most
  recent encounter, or `None` when there are no encounters.
- `RiskAssessment` combines a patient with a numeric score and the reasons
  that contributed to it. Its `tier` property maps the score to a `RiskTier`.

The vital-sign reference ranges are used by `abnormal_flags()`. The risk
scoring rules are separate and use their own thresholds.

## Synthetic cohort generation

`generate_patients(count, seed)` uses a local `random.Random` instance. The
default seed is `1337`, so the random choices are repeatable for the same
inputs. For each requested patient, it fabricates a birth date, identity,
zero to three conditions, and one to four encounters. Each encounter receives
a newly generated set of measurements.

Measurements are drawn from normal distributions with the means and standard
deviations specified in `_random_vitals()`, then rounded to one decimal place.
The values are examples for exercising code, not validated clinical
measurements. Although generation is seeded, reported ages depend on the date
the program runs, and report timestamps are also current.

## Risk scoring

`assess_patient()` runs each function in `DEFAULT_RULES` against one patient.
Rules inspect the latest available measurements or patient attributes and
return a point value plus a human-readable reason when they match:

| Rule | Condition | Points |
|---|---|---:|
| High blood pressure | Systolic pressure is at least 140 or diastolic pressure is at least 90 | 3 |
| Hyperglycemia | Glucose is at least 140 | 2 |
| Elevated BMI | BMI is at least 30 | 2 |
| Multiple conditions | At least two listed conditions | 1 |
| Advanced age | Age is at least 65 | 1 |

The score is the sum of all matching rules. `RiskTier.from_score()` assigns
`low` below 2, `moderate` from 2 through 4, `high` from 5 through 7, and
`critical` at 8 or above. The rules can be replaced or extended by passing a
different sequence to `assess_patient()`.

## Reporting

- `cohort_statistics()` summarizes the latest glucose and BMI values across
  patients with measurements. It returns mean and median glucose, maximum
  glucose, and population standard deviation of BMI. With no available glucose
  values, it returns an empty dictionary; with one BMI value, the standard
  deviation is `0.0`.
- `tier_breakdown()` counts assessments in each tier.
- `condition_prevalence()` counts listed conditions and sorts them by
  descending frequency.
- `render_report()` assesses and sorts patients by descending score, then
  combines the cohort statistics, tier counts, condition counts, and up to
  five highest-scoring patients into a text report.
- `write_csv()` writes one row per assessment with MRN, name, age, score, tier,
  and rule reasons. It writes to a caller-provided text stream.

## Audit behavior

The `@audited` decorator records calls to generation and assessment functions
in the module-level `_AUDIT_TRAIL`, including a timestamp, action label, and
function name. `audit_session()` appends begin and end markers, including when
an exception occurs within the context. The trail is only held in memory; the
program does not persist or print it.

## Command-line usage

Run the module with Python. The available options are:

| Option | Default | Description |
|---|---:|---|
| `-n`, `--count` | `25` | Number of fictional patients to generate |
| `-s`, `--seed` | `1337` | Seed for random data generation |
| `--csv` | Off | Emit CSV instead of the text report |

For example, `python patient_analytics.py --count 10 --seed 42` prints a text
report, while `python patient_analytics.py -n 10 --csv` prints CSV. Output is
written to standard output and can be redirected by the caller if desired.

## Design concepts demonstrated

The module illustrates dataclasses, enums, type hints, a `Protocol`, a
decorator factory, a context manager, seeded randomness, generators,
comprehensions, `functools.reduce`, aggregation, and basic command-line
argument parsing.
