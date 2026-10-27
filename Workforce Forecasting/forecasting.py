"""Bank & agency usage forecasting for Optima (shared by the notebook and Streamlit dashboard).

All record-level data stays in BigQuery: only weekly aggregates per ward (org unit) are pulled
into memory, and nothing is written to disk.
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import Callable

import google.auth
import numpy as np
import pandas as pd
from google.cloud import bigquery
from statsmodels.tsa.exponential_smoothing.ets import ETSModel

PROJECT = "ndr-hb-abuhb-sde"
TABLE = f"{PROJECT}.sde_workforce_optima.bank_agency_usage"
TYPES = ("Bank", "Agency")
COMBINED = "Bank + Agency"
SEASON = 52
HOURS_PER_WTE = 37.5
RECENT_WEEKS = 13
MIN_ORIGINS = 5
QUANTILES = {"lower_95": 0.025, "lower_80": 0.10, "upper_80": 0.90, "upper_95": 0.975}
AUTO = "Auto (best backtest)"


# --------------------------------------------------------------------------- data access
def get_client(project: str = PROJECT) -> bigquery.Client:
    """BigQuery client using Google Application Default Credentials."""
    credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    return bigquery.Client(project=project, credentials=credentials)


def _to_dataframe(job: bigquery.QueryJob) -> pd.DataFrame:
    try:
        return job.to_dataframe()
    except Exception:
        return job.to_dataframe(create_bqstorage_client=False)


def _params(train_start: str, staff_group: str | None) -> list:
    return [
        bigquery.ArrayQueryParameter("types", "STRING", list(TYPES)),
        bigquery.ScalarQueryParameter("train_start", "DATE", train_start),
        bigquery.ScalarQueryParameter("staff_group", "STRING", staff_group),
    ]


_FILTER = """fulfillmenttype IN UNNEST(@types)
  AND weekending >= @train_start
  AND (@staff_group IS NULL OR UPPER(TRIM(staffgroup)) = UPPER(TRIM(@staff_group)))"""


def list_staff_groups(client: bigquery.Client, table: str = TABLE) -> list[str]:
    sql = f"SELECT DISTINCT staffgroup FROM `{table}` WHERE staffgroup IS NOT NULL ORDER BY 1"
    return _to_dataframe(client.query(sql))["staffgroup"].tolist()


@dataclass
class WorkforceData:
    """Weekly worked hours per ward, one wide frame (weeks x orgunitid) per staff type."""

    weekly: dict[str, pd.DataFrame]
    units: pd.DataFrame  # index orgunitid; columns division, ward, ward_long

    @property
    def divisions(self) -> list[str]:
        return sorted(self.units["division"].unique())

    def wards(self, division: str) -> pd.DataFrame:
        return self.units[self.units["division"] == division]

    def series(self, staff_type: str, division: str | None = None, orgunitid: int | None = None) -> pd.Series:
        """Weekly hours for the total (no args), a division, or a single ward."""
        if orgunitid is not None:
            cols = [orgunitid]
        elif division is not None:
            cols = self.wards(division).index
        else:
            cols = self.units.index
        types = TYPES if staff_type == COMBINED else (staff_type,)
        return sum(self.weekly[t][cols].sum(axis=1) for t in types)

    def recent_weekly_hours(self, staff_type: str, cutoff: pd.Timestamp, weeks: int = RECENT_WEEKS) -> pd.Series:
        """Average weekly hours per ward over the last `weeks` complete weeks."""
        types = TYPES if staff_type == COMBINED else (staff_type,)
        return sum(self.weekly[t].loc[:cutoff].iloc[-weeks:].mean() for t in types)


def fetch_data(client: bigquery.Client, train_start: str = "2022-01-01",
               staff_group: str | None = None, table: str = TABLE) -> WorkforceData:
    """Pull weekly hours per ward and type (aggregated in BigQuery) plus the ward→division lookup."""
    config = bigquery.QueryJobConfig(query_parameters=_params(train_start, staff_group))
    weekly_sql = f"""
        SELECT weekending, orgunitid, fulfillmenttype, SUM(workedhours) AS hours
        FROM `{table}` WHERE {_FILTER}
        GROUP BY 1, 2, 3"""
    units_sql = f"""
        SELECT orgunitid, latest.division, latest.ward, latest.ward_long FROM (
          SELECT orgunitid,
                 ARRAY_AGG(STRUCT(UPPER(TRIM(COALESCE(division, 'UNKNOWN'))) AS division,
                                  COALESCE(unitshortname, CAST(orgunitid AS STRING)) AS ward,
                                  unitlongname AS ward_long)
                           ORDER BY weekending DESC LIMIT 1)[OFFSET(0)] AS latest
          FROM `{table}` WHERE {_FILTER}
          GROUP BY 1)"""
    weekly = _to_dataframe(client.query(weekly_sql, job_config=config))
    units = _to_dataframe(client.query(units_sql, job_config=config)).set_index("orgunitid").sort_index()
    if weekly.empty:
        raise ValueError(f"No data returned for staff group {staff_group!r} since {train_start}.")

    weekly["weekending"] = pd.to_datetime(weekly["weekending"])
    index = pd.date_range(weekly["weekending"].min(), weekly["weekending"].max(), freq="W-SAT")
    wide = {
        t: (weekly[weekly["fulfillmenttype"] == t]
            .pivot_table(index="weekending", columns="orgunitid", values="hours", aggfunc="sum")
            .reindex(index=index, columns=units.index).fillna(0.0))
        for t in TYPES
    }
    return WorkforceData(weekly=wide, units=units)


# --------------------------------------------------------------------------- forecast window
@dataclass
class Window:
    cutoff: pd.Timestamp          # last complete week used for training
    months: pd.PeriodIndex        # forecast months
    future: pd.DatetimeIndex      # forecast weeks (week-ending Saturdays)

    @property
    def horizon(self) -> int:
        return len(self.future)


def make_window(forecast_months: int = 6, exclude_recent_weeks: int = 0,
                today: pd.Timestamp | None = None) -> Window:
    """Weeks end on Saturday; the cutoff is the last Saturday strictly before today."""
    today = (today or pd.Timestamp.today()).normalize()
    days_back = (today.weekday() - 5) % 7 or 7
    cutoff = today - pd.Timedelta(days=days_back) - pd.Timedelta(weeks=exclude_recent_weeks)
    first = (cutoff + pd.offsets.MonthEnd(0)).to_period("M") + 1
    months = pd.period_range(first, periods=forecast_months, freq="M")
    future = pd.date_range(cutoff + pd.Timedelta(weeks=1), months[-1].end_time.normalize(), freq="W-SAT")
    return Window(cutoff=cutoff, months=months, future=future)


# --------------------------------------------------------------------------- models
def _log_ets(train: pd.Series, h: int, trend: str | None) -> np.ndarray:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = ETSModel(np.log1p(train.clip(lower=0)), error="add", trend=trend,
                             damped_trend=trend is not None, seasonal="add",
                             seasonal_periods=SEASON, initialization_method="heuristic")
            return np.expm1(model.fit(disp=False, maxiter=2000).forecast(h).values)
    except Exception:
        return np.full(h, np.nan)


def fc_log_ets(train: pd.Series, h: int) -> np.ndarray:
    return _log_ets(train, h, trend="add")


def fc_log_ets_flat(train: pd.Series, h: int) -> np.ndarray:
    return _log_ets(train, h, trend=None)


def fc_scaled_snaive(train: pd.Series, h: int) -> np.ndarray:
    recent = train.iloc[-8:].mean()
    base = train.iloc[-SEASON - 8:-SEASON].mean()
    if base <= 0:
        return np.full(h, recent)
    return np.resize(train.iloc[-SEASON:].values, h) * recent / base


def fc_snaive(train: pd.Series, h: int) -> np.ndarray:
    return np.resize(train.iloc[-SEASON:].values, h)


def fc_recent_mean(train: pd.Series, h: int) -> np.ndarray:
    return np.full(h, train.iloc[-8:].mean())


@dataclass(frozen=True)
class Model:
    fn: Callable[[pd.Series, int], np.ndarray]
    min_history: int
    description: str


MODELS: dict[str, Model] = {
    "Log ETS": Model(fc_log_ets, 2 * SEASON,
                     "Exponential smoothing on log hours with damped trend and 52-week seasonality."),
    "Log ETS (no trend)": Model(fc_log_ets_flat, 2 * SEASON,
                                "As Log ETS without a trend, so recent rises/falls are not extrapolated."),
    "Seasonal naive, level-scaled": Model(fc_scaled_snaive, SEASON + 8,
                                          "Last year's weekly pattern × (latest 8-week level ÷ same 8 weeks a year earlier)."),
    "Seasonal naive": Model(fc_snaive, SEASON, "Same week last year."),
    "Recent 8-week mean": Model(fc_recent_mean, 4, "Flat line at the average of the last 8 weeks."),
}
FALLBACK_MODEL = "Recent 8-week mean"


# --------------------------------------------------------------------------- forecasting
@dataclass
class ForecastResult:
    label: str
    model: str
    scores: pd.Series                  # WAPE % by candidate model (lower is better)
    weekly: pd.DataFrame               # forecast weeks: forecast, intervals, prebooked_so_far
    monthly: pd.DataFrame              # forecast months: weeks, forecast_hours, intervals, avg_weekly_wte, last_year
    summary: dict                      # totals over all forecast months
    actual: pd.Series                  # training history up to the cutoff
    n_origins: int
    notes: list[str] = field(default_factory=list)


def _wape(pred: np.ndarray, act: np.ndarray) -> float:
    if np.isnan(pred).any() or act.sum() <= 0:
        return np.nan
    return float(np.abs(act - pred).sum() / act.sum() * 100)


def _choose_origins(n: int, h: int, span: int, step: int) -> tuple[list[int], list[str]]:
    """Backtest origins shared by all feasible models; drops the most data-hungry models if history is short."""
    feasible = sorted([m for m in MODELS if MODELS[m].min_history <= n - h],
                      key=lambda m: MODELS[m].min_history, reverse=True)
    while feasible:
        start = max(n - h - span, MODELS[feasible[0]].min_history)
        origins = list(range(n - h, start - 1, -step))[::-1]
        if len(origins) >= MIN_ORIGINS:
            return origins, feasible
        need = MODELS[feasible[0]].min_history
        feasible = [m for m in feasible if MODELS[m].min_history < need]
    return [], []


def _interval(bt: tuple | None, positions, point_sum: float, current_level: float, q: float) -> float:
    """Point + quantile of backtest errors over the same horizon weeks, rescaled to today's level."""
    if bt is None:
        return np.nan
    if point_sum <= 0 and current_level <= 0:
        return point_sum
    pred, act, level = bt
    err = act[:, positions].sum(axis=1) - pred[:, positions].sum(axis=1)
    ok = level > 0
    if ok.sum() >= MIN_ORIGINS and current_level > 0:
        return max(point_sum + np.quantile(err[ok] / level[ok], q) * current_level, 0.0)
    return max(point_sum + np.quantile(err, q), 0.0)


def run_forecast(series: pd.Series, window: Window, label: str = "", model: str = AUTO,
                 backtest_span: int = 104, backtest_step: int = 4) -> ForecastResult:
    """Backtest candidate models, pick one (or use `model`), and forecast with empirical intervals."""
    h = window.horizon
    full_actual = series.reindex(pd.date_range(series.index.min(), window.cutoff, freq="W-SAT")).fillna(0.0)
    prebooked = series.reindex(window.future).fillna(0.0)
    notes: list[str] = []

    nonzero = np.flatnonzero(full_actual.values > 0)
    actual = full_actual.iloc[nonzero[0]:] if len(nonzero) else full_actual.iloc[-8:]
    if not len(nonzero):
        notes.append("No worked hours in the history.")
    n = len(actual)

    origins, feasible = _choose_origins(n, h, backtest_span, backtest_step)
    backtests, scores = {}, {}
    if origins:
        act = np.array([actual.iloc[o:o + h].values for o in origins])
        level = np.array([actual.iloc[max(o - 8, 0):o].mean() for o in origins])
        for name in feasible:
            pred = np.clip(np.array([MODELS[name].fn(actual.iloc[:o], h) for o in origins]), 0, None)
            backtests[name] = (pred, act, level)
            scores[name] = _wape(pred, act)
    else:
        notes.append(f"Only {n} weeks of history: too short to backtest, so no intervals.")
    scores = pd.Series(scores, dtype=float).reindex(list(MODELS))

    valid = scores.dropna()
    if model != AUTO and model in backtests:
        chosen = model
    else:
        if model != AUTO:
            notes.append(f"{model} needs more history than this series has; using automatic choice.")
        chosen = valid.idxmin() if len(valid) else FALLBACK_MODEL
    if len(feasible) < len(MODELS) and origins:
        notes.append(f"{n} weeks of history: some models skipped (need more history).")

    point = np.clip(MODELS[chosen].fn(actual, h), 0, None)
    if np.isnan(point).any():
        chosen = FALLBACK_MODEL
        point = np.clip(MODELS[chosen].fn(actual, h), 0, None)
        notes.append("Selected model failed to fit; fell back to recent mean.")
    bt = backtests.get(chosen)
    current_level = float(actual.iloc[-8:].mean())

    weekly = pd.DataFrame({"forecast": point}, index=window.future)
    for col, q in QUANTILES.items():
        weekly[col] = [_interval(bt, [i], point[i], current_level, q) for i in range(h)]
    weekly["prebooked_so_far"] = prebooked.values
    weekly.index.name = "weekending"

    month_of = window.future.to_period("M")
    actual_month = full_actual.index.to_period("M")

    def summarise(positions, months) -> dict:
        total = float(point[positions].sum())
        last_year = float(full_actual[actual_month.isin(months - 12)].sum())
        out = {"weeks": len(positions), "forecast_hours": total,
               **{col: _interval(bt, positions, total, current_level, q) for col, q in QUANTILES.items()},
               "avg_weekly_wte": total / max(len(positions), 1) / HOURS_PER_WTE,
               "same_period_last_year": last_year}
        out["change_vs_last_year_%"] = (total / last_year - 1) * 100 if last_year > 0 else np.nan
        return out

    monthly = pd.DataFrame({
        str(m): summarise(np.where(month_of == m)[0], pd.PeriodIndex([m])) for m in window.months
    }).T
    monthly.index.name = "month"
    summary = summarise(np.where(month_of.isin(window.months))[0], window.months)

    return ForecastResult(label=label, model=chosen, scores=scores, weekly=weekly, monthly=monthly,
                          summary=summary, actual=actual, n_origins=len(origins), notes=notes)


# --------------------------------------------------------------------------- hierarchy helpers
OTHER = "OTHER (small volume)"


def children(data: WorkforceData, staff_type: str, cutoff: pd.Timestamp, division: str | None = None,
             min_weekly_hours: float = 0.0) -> list[tuple[str, dict]]:
    """Child series one level below: divisions (for the total) or wards (for a division).

    Returns (label, kwargs for WorkforceData.series) pairs; children below `min_weekly_hours`
    recently are combined into OTHER so children still add up to the parent.
    """
    recent = data.recent_weekly_hours(staff_type, cutoff)
    if division is None:
        by_div = recent.groupby(data.units["division"]).sum().sort_values(ascending=False)
        big = by_div[by_div >= min_weekly_hours].index.tolist()
        small_units = data.units.index[~data.units["division"].isin(big)]
        items = [(d, {"division": d}) for d in big]
    else:
        wards = data.wards(division)
        r = recent.reindex(wards.index).sort_values(ascending=False)
        big = r[r >= min_weekly_hours].index.tolist()
        small_units = wards.index.difference(big)
        items = [(f"{wards.at[u, 'ward']} [{u}]", {"orgunitid": u}) for u in big]
    if len(small_units) and recent.reindex(small_units).sum() > 0:
        items.append((OTHER, {"orgunitids": list(small_units)}))
    return items


def child_series(data: WorkforceData, staff_type: str, spec: dict) -> pd.Series:
    if "orgunitids" in spec:
        types = TYPES if staff_type == COMBINED else (staff_type,)
        return sum(data.weekly[t][spec["orgunitids"]].sum(axis=1) for t in types)
    return data.series(staff_type, **spec)


def summary_row(label: str, result: ForecastResult, recent_hours: float) -> dict:
    return {"name": label, "recent_weekly_hours": recent_hours, "model": result.model,
            "backtest_wape_%": result.scores.get(result.model, np.nan), **result.summary}
