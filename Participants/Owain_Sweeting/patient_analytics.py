"""
patient_analytics.py
=====================

A deliberately dense, multi-layered example module used for GitHub Copilot
training sessions. It simulates a small clinical analytics pipeline over
FICTITIOUS patient data. Nothing in here is real medical advice, and every
name, MRN, and value is randomly generated.

The module demonstrates a bit of everything so that "Explain this file" has
plenty to chew on:

    * dataclasses + enums
    * a synthetic data generator with seeded randomness
    * a small rules engine driven by closures
    * a decorator-based audit log
    * generators / comprehensions / functools reductions
    * type hints, protocols, and a context manager
    * a tiny command-line entry point

Author:  Training Example (not for clinical use)
"""

from __future__ import annotations

import csv
import functools
import io
import random
import statistics
from collections import Counter, defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum, auto
from typing import Callable, Iterable, Iterator, Protocol, Sequence

# --------------------------------------------------------------------------- #
# Constants & reference data (all fabricated)
# --------------------------------------------------------------------------- #

RANDOM_SEED = 1337

FIRST_NAMES = [
    "Avery", "Blake", "Casey", "Dakota", "Emerson", "Finley", "Gray",
    "Harper", "Indigo", "Jules", "Kai", "Lior", "Monroe", "Nova", "Onyx",
]
LAST_NAMES = [
    "Alvarez", "Bennett", "Cho", "Delgado", "Everly", "Farooq", "Gupta",
    "Haddad", "Ibrahim", "Johansson", "Kowalski", "Lindqvist", "Mbeki",
]

# Normal-ish reference ranges used only to flag "fictional" abnormalities.
REFERENCE_RANGES: dict[str, tuple[float, float]] = {
    "systolic_bp": (90.0, 120.0),
    "diastolic_bp": (60.0, 80.0),
    "heart_rate": (60.0, 100.0),
    "glucose": (70.0, 110.0),
    "bmi": (18.5, 24.9),
    "temperature_c": (36.1, 37.2),
}


class Sex(Enum):
    FEMALE = auto()
    MALE = auto()
    OTHER = auto()


class RiskTier(Enum):
    """Coarse risk buckets produced by the rules engine."""

    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

    @classmethod
    def from_score(cls, score: int) -> "RiskTier":
        if score >= 8:
            return cls.CRITICAL
        if score >= 5:
            return cls.HIGH
        if score >= 2:
            return cls.MODERATE
        return cls.LOW


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Vitals:
    """A single set of vital-sign measurements for one encounter."""

    systolic_bp: float
    diastolic_bp: float
    heart_rate: float
    glucose: float
    bmi: float
    temperature_c: float

    def as_dict(self) -> dict[str, float]:
        return {
            "systolic_bp": self.systolic_bp,
            "diastolic_bp": self.diastolic_bp,
            "heart_rate": self.heart_rate,
            "glucose": self.glucose,
            "bmi": self.bmi,
            "temperature_c": self.temperature_c,
        }

    def abnormal_flags(self) -> dict[str, str]:
        """Return a mapping of metric -> 'low'/'high' for out-of-range values."""
        flags: dict[str, str] = {}
        for metric, value in self.as_dict().items():
            low, high = REFERENCE_RANGES[metric]
            if value < low:
                flags[metric] = "low"
            elif value > high:
                flags[metric] = "high"
        return flags


@dataclass
class Patient:
    """A fictional patient and their encounter history."""

    mrn: str
    first_name: str
    last_name: str
    birth_date: date
    sex: Sex
    conditions: list[str] = field(default_factory=list)
    encounters: list[tuple[date, Vitals]] = field(default_factory=list)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        today = date.today()
        had_birthday = (today.month, today.day) >= (
            self.birth_date.month,
            self.birth_date.day,
        )
        return today.year - self.birth_date.year - (0 if had_birthday else 1)

    def latest_vitals(self) -> Vitals | None:
        if not self.encounters:
            return None
        return max(self.encounters, key=lambda enc: enc[0])[1]


# --------------------------------------------------------------------------- #
# Audit log via a decorator
# --------------------------------------------------------------------------- #

_AUDIT_TRAIL: list[str] = []


def audited(action: str) -> Callable[[Callable[..., object]], Callable[..., object]]:
    """Decorator factory that records each call into a module-level audit trail."""

    def decorator(func: Callable[..., object]) -> Callable[..., object]:
        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            stamp = datetime.now().isoformat(timespec="seconds")
            _AUDIT_TRAIL.append(f"{stamp} | {action} | {func.__name__}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@contextmanager
def audit_session(label: str) -> Iterator[list[str]]:
    """Context manager that brackets a block of work in the audit trail."""
    _AUDIT_TRAIL.append(f"--- BEGIN {label} ---")
    try:
        yield _AUDIT_TRAIL
    finally:
        _AUDIT_TRAIL.append(f"--- END {label} ---")


# --------------------------------------------------------------------------- #
# Synthetic data generation
# --------------------------------------------------------------------------- #

CONDITION_POOL = [
    "hypertension", "type-2-diabetes", "asthma", "hyperlipidemia",
    "obesity", "anxiety", "migraine", "hypothyroidism",
]


def _random_vitals(rng: random.Random) -> Vitals:
    """Produce one plausible-but-fake set of vitals using a seeded RNG."""
    return Vitals(
        systolic_bp=round(rng.gauss(122, 18), 1),
        diastolic_bp=round(rng.gauss(78, 11), 1),
        heart_rate=round(rng.gauss(78, 14), 1),
        glucose=round(rng.gauss(105, 30), 1),
        bmi=round(rng.gauss(26, 5), 1),
        temperature_c=round(rng.gauss(36.8, 0.4), 1),
    )


@audited("generate")
def generate_patients(count: int, seed: int = RANDOM_SEED) -> list[Patient]:
    """Create `count` fictional patients, each with 1-4 encounters."""
    rng = random.Random(seed)
    patients: list[Patient] = []

    for i in range(count):
        birth = date(
            rng.randint(1945, 2010),
            rng.randint(1, 12),
            rng.randint(1, 28),
        )
        patient = Patient(
            mrn=f"MRN-{rng.randint(10_000, 99_999)}",
            first_name=rng.choice(FIRST_NAMES),
            last_name=rng.choice(LAST_NAMES),
            birth_date=birth,
            sex=rng.choice(list(Sex)),
            conditions=rng.sample(
                CONDITION_POOL, k=rng.randint(0, 3)
            ),
        )

        encounter_date = birth + timedelta(days=rng.randint(6_000, 20_000))
        for _ in range(rng.randint(1, 4)):
            encounter_date += timedelta(days=rng.randint(30, 400))
            patient.encounters.append((encounter_date, _random_vitals(rng)))

        patients.append(patient)

    return patients


# --------------------------------------------------------------------------- #
# Rules engine
# --------------------------------------------------------------------------- #

# A rule takes a patient and returns (points, human-readable reason) or None.
Rule = Callable[[Patient], tuple[int, str] | None]


def _rule_high_blood_pressure(patient: Patient) -> tuple[int, str] | None:
    v = patient.latest_vitals()
    if v and (v.systolic_bp >= 140 or v.diastolic_bp >= 90):
        return 3, f"Elevated BP {v.systolic_bp:.0f}/{v.diastolic_bp:.0f}"
    return None


def _rule_hyperglycemia(patient: Patient) -> tuple[int, str] | None:
    v = patient.latest_vitals()
    if v and v.glucose >= 140:
        return 2, f"Glucose {v.glucose:.0f} mg/dL"
    return None


def _rule_elevated_bmi(patient: Patient) -> tuple[int, str] | None:
    v = patient.latest_vitals()
    if v and v.bmi >= 30:
        return 2, f"BMI {v.bmi:.1f}"
    return None


def _rule_multiple_conditions(patient: Patient) -> tuple[int, str] | None:
    if len(patient.conditions) >= 2:
        return 1, f"{len(patient.conditions)} chronic conditions"
    return None


def _rule_advanced_age(patient: Patient) -> tuple[int, str] | None:
    if patient.age >= 65:
        return 1, f"Age {patient.age}"
    return None


DEFAULT_RULES: tuple[Rule, ...] = (
    _rule_high_blood_pressure,
    _rule_hyperglycemia,
    _rule_elevated_bmi,
    _rule_multiple_conditions,
    _rule_advanced_age,
)


@dataclass
class RiskAssessment:
    patient: Patient
    score: int
    reasons: list[str]

    @property
    def tier(self) -> RiskTier:
        return RiskTier.from_score(self.score)


@audited("assess")
def assess_patient(patient: Patient, rules: Sequence[Rule] = DEFAULT_RULES) -> RiskAssessment:
    """Run every rule against one patient and fold the hits into a score."""
    hits = (rule(patient) for rule in rules)
    scored = [hit for hit in hits if hit is not None]
    total = functools.reduce(lambda acc, hit: acc + hit[0], scored, 0)
    reasons = [reason for _, reason in scored]
    return RiskAssessment(patient=patient, score=total, reasons=reasons)


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #


class SupportsWrite(Protocol):
    def write(self, s: str) -> int | None: ...


def cohort_statistics(patients: Iterable[Patient]) -> dict[str, float]:
    """Compute a few aggregate stats across the cohort's latest vitals."""
    latest = [p.latest_vitals() for p in patients]
    glucose = [v.glucose for v in latest if v is not None]
    bmi = [v.bmi for v in latest if v is not None]
    if not glucose:
        return {}
    return {
        "mean_glucose": round(statistics.fmean(glucose), 1),
        "median_glucose": round(statistics.median(glucose), 1),
        "stdev_bmi": round(statistics.pstdev(bmi), 2) if len(bmi) > 1 else 0.0,
        "max_glucose": max(glucose),
    }


def tier_breakdown(assessments: Iterable[RiskAssessment]) -> Counter[str]:
    """Count how many patients fall into each risk tier."""
    return Counter(a.tier.value for a in assessments)


def condition_prevalence(patients: Iterable[Patient]) -> dict[str, int]:
    """Tally how often each condition appears across the cohort."""
    tally: dict[str, int] = defaultdict(int)
    for patient in patients:
        for condition in patient.conditions:
            tally[condition] += 1
    return dict(sorted(tally.items(), key=lambda kv: kv[1], reverse=True))


def write_csv(assessments: Sequence[RiskAssessment], stream: SupportsWrite) -> None:
    """Serialize assessments to CSV into any text stream."""
    writer = csv.writer(stream)
    writer.writerow(["mrn", "name", "age", "score", "tier", "reasons"])
    for a in assessments:
        writer.writerow(
            [
                a.patient.mrn,
                a.patient.full_name,
                a.patient.age,
                a.score,
                a.tier.value,
                "; ".join(a.reasons),
            ]
        )


def render_report(patients: Sequence[Patient]) -> str:
    """Build a full human-readable text report for the cohort."""
    assessments = [assess_patient(p) for p in patients]
    assessments.sort(key=lambda a: a.score, reverse=True)

    buffer = io.StringIO()
    buffer.write("FICTIONAL PATIENT RISK REPORT\n")
    buffer.write("=" * 48 + "\n")
    buffer.write(f"Generated: {datetime.now():%Y-%m-%d %H:%M}\n")
    buffer.write(f"Patients:  {len(patients)}\n\n")

    stats = cohort_statistics(patients)
    buffer.write("Cohort statistics\n-----------------\n")
    for key, value in stats.items():
        buffer.write(f"  {key:<16}: {value}\n")

    buffer.write("\nRisk tiers\n----------\n")
    for tier, n in tier_breakdown(assessments).most_common():
        buffer.write(f"  {tier:<10}: {n}\n")

    buffer.write("\nCondition prevalence\n--------------------\n")
    for condition, n in condition_prevalence(patients).items():
        buffer.write(f"  {condition:<18}: {n}\n")

    buffer.write("\nTop at-risk patients\n--------------------\n")
    for a in assessments[:5]:
        reasons = ", ".join(a.reasons) or "no flags"
        buffer.write(
            f"  [{a.tier.value.upper():<8}] {a.patient.full_name} "
            f"({a.patient.mrn}, age {a.patient.age}) score={a.score} :: {reasons}\n"
        )

    return buffer.getvalue()


# --------------------------------------------------------------------------- #
# Command-line entry point
# --------------------------------------------------------------------------- #


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", "--count", type=int, default=25,
                        help="number of fictional patients to generate")
    parser.add_argument("-s", "--seed", type=int, default=RANDOM_SEED,
                        help="random seed for reproducibility")
    parser.add_argument("--csv", action="store_true",
                        help="emit CSV instead of the text report")
    args = parser.parse_args(argv)

    with audit_session("cohort-run"):
        patients = generate_patients(args.count, seed=args.seed)
        if args.csv:
            assessments = [assess_patient(p) for p in patients]
            out = io.StringIO()
            write_csv(assessments, out)
            print(out.getvalue(), end="")
        else:
            print(render_report(patients))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
