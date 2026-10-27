from datetime import date
import os
import time

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


st.set_page_config(
    page_title="COVID-19 Case Surveillance | CDC",
    layout="wide",
)

BASE_URL = "https://data.cdc.gov/resource/vbim-akqf.json"
SOURCE_COLUMNS = [
    "cdc_case_earliest_dt",
    "cdc_report_dt",
    "onset_dt",
    "current_status",
    "sex",
    "age_group",
    "race_ethnicity_combined",
    "hosp_yn",
    "icu_yn",
    "death_yn",
    "medcond_yn",
]
COLUMN_RENAME = {
    "cdc_case_earliest_dt": "earliest_case_date",
    "cdc_report_dt": "report_date",
    "onset_dt": "onset_date",
    "current_status": "case_status",
    "race_ethnicity_combined": "race_ethnicity",
    "hosp_yn": "hospitalized",
    "icu_yn": "icu_admission",
    "death_yn": "death",
    "medcond_yn": "underlying_condition",
}
DATE_COLUMNS = ["earliest_case_date", "report_date", "onset_date"]


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_cases(start_date: date, end_date: date, max_records: int) -> tuple[pd.DataFrame, bool]:
    """Fetch a bounded report-date window with stable, paginated API requests."""
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=0.8,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    token = os.getenv("SOCRATA_APP_TOKEN")
    if token:
        session.headers.update({"X-App-Token": token})

    start_text = f"{start_date.isoformat()}T00:00:00.000"
    end_text = f"{end_date.isoformat()}T00:00:00.000"
    where_clause = f"cdc_report_dt >= '{start_text}' AND cdc_report_dt < '{end_text}'"
    records = []
    page_size = 10_000

    while len(records) < max_records:
        limit = min(page_size, max_records - len(records))
        response = session.get(
            BASE_URL,
            params={
                "$select": ",".join(SOURCE_COLUMNS),
                "$where": where_clause,
                "$order": "cdc_report_dt ASC, cdc_case_earliest_dt ASC, :id ASC",
                "$limit": limit,
                "$offset": len(records),
            },
            timeout=(10, 90),
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            raise requests.HTTPError(
                f"CDC Socrata API returned {response.status_code}: {response.text[:500]}"
            ) from error

        try:
            page = response.json()
        except ValueError as error:
            raise ValueError("CDC Socrata returned a non-JSON response.") from error
        if not isinstance(page, list):
            raise ValueError("CDC Socrata returned an unexpected response format.")
        if not page:
            break

        records.extend(page)
        if len(page) < limit:
            break
        time.sleep(0.1)

    hit_limit = len(records) >= max_records
    frame = pd.DataFrame.from_records(records, columns=SOURCE_COLUMNS)
    frame = frame.rename(columns=COLUMN_RENAME)
    for column in DATE_COLUMNS:
        frame[column] = pd.to_datetime(frame[column], errors="coerce")
    for column in frame.select_dtypes(include="object").columns:
        frame[column] = frame[column].astype("string").str.strip()
    return frame, hit_limit


def count_yes(values: pd.Series) -> int:
    return int(values.eq("Yes").sum())


MISSING_LABEL = "(Missing / not reported)"


def filter_options(values: pd.Series) -> list[str]:
    options = sorted(values.dropna().unique().tolist())
    if values.isna().any():
        options.append(MISSING_LABEL)
    return options


def matches_selection(values: pd.Series, selected: list[str]) -> pd.Series:
    mask = values.isna() & (MISSING_LABEL in selected)
    selected_values = [value for value in selected if value != MISSING_LABEL]
    if selected_values:
        mask |= values.isin(selected_values)
    return mask


def make_daily_summary(frame: pd.DataFrame) -> pd.DataFrame:
    dated = frame.dropna(subset=["report_date"]).copy()
    if dated.empty:
        return pd.DataFrame(
            columns=["report_date", "case_records", "reported_deaths", "reported_hospitalizations", "seven_day_average"]
        )

    daily = (
        dated.groupby(dated["report_date"].dt.floor("D"))
        .agg(
            case_records=("report_date", "size"),
            reported_deaths=("death", count_yes),
            reported_hospitalizations=("hospitalized", count_yes),
        )
        .rename_axis("report_date")
        .reset_index()
        .sort_values("report_date")
    )
    daily["seven_day_average"] = daily["case_records"].rolling(7, min_periods=1).mean()
    return daily


st.markdown("#### CDC CASE SURVEILLANCE / PUBLIC USE DATA")
st.title("COVID-19 case surveillance")
st.caption(
    "A descriptive view of CDC case reports. The source stopped receiving new reports on July 1, 2024; "
    "records are provisional, reporting varies, and suppressed or missing values are retained."
)

with st.sidebar:
    st.header("Data window")
    with st.form("data_window"):
        start_date = st.date_input("Report date from", value=date(2024, 1, 1))
        end_date = st.date_input("Report date to (exclusive)", value=date(2024, 2, 1))
        max_records = st.select_slider(
            "Maximum records",
            options=[10_000, 25_000, 50_000],
            value=25_000,
            format_func=lambda value: f"{value:,}",
        )
        load_data = st.form_submit_button("Load data", type="primary", use_container_width=True)

    st.divider()
    st.caption("The dataset has no state or county fields. Counts are not population rates or estimates of individual risk.")
    st.markdown("[CDC dataset documentation](https://data.cdc.gov/Case-Surveillance/COVID-19-Case-Surveillance-Public-Use-Data/vbim-akqf/about_data)")

if start_date >= end_date:
    st.error("Choose an end date later than the start date.")
    st.stop()

if "dashboard_window" not in st.session_state:
    st.session_state.dashboard_window = (date(2024, 1, 1), date(2024, 2, 1), 25_000)
if load_data:
    st.session_state.dashboard_window = (start_date, end_date, max_records)

active_start, active_end, active_limit = st.session_state.dashboard_window

try:
    with st.spinner("Loading the selected CDC report-date window..."):
        cases, hit_limit = fetch_cases(active_start, active_end, active_limit)
except (requests.RequestException, ValueError) as error:
    st.error(f"Could not load CDC data: {error}")
    st.stop()

if cases.empty:
    st.warning("No records were returned for this date window.")
    st.stop()

if hit_limit:
    st.warning(
        f"The {active_limit:,}-record cap was reached. Results may be incomplete for "
        "this window; increase the cap or narrow the dates before interpreting totals."
    )

with st.sidebar:
    st.header("Case filters")
    age_values = filter_options(cases["age_group"])
    sex_values = filter_options(cases["sex"])
    race_values = filter_options(cases["race_ethnicity"])
    selected_ages = st.multiselect("Age group", age_values, default=age_values)
    selected_sexes = st.multiselect("Sex", sex_values, default=sex_values)
    selected_races = st.multiselect("Race / ethnicity", race_values, default=race_values)
    death_filter = st.selectbox("Death indicator", ["All", "Yes", "No", "Unknown", "Missing", "NA"])
    hospitalization_filter = st.selectbox(
        "Hospitalization indicator", ["All", "Yes", "No", "Unknown", "Missing", "NA"]
    )

filtered = cases[
    matches_selection(cases["age_group"], selected_ages)
    & matches_selection(cases["sex"], selected_sexes)
    & matches_selection(cases["race_ethnicity"], selected_races)
].copy()
if death_filter != "All":
    filtered = filtered[filtered["death"] == death_filter]
if hospitalization_filter != "All":
    filtered = filtered[filtered["hospitalized"] == hospitalization_filter]

st.caption(
    f"Report-date window: {active_start:%d %b %Y} to {active_end:%d %b %Y} (exclusive)  ·  "
    f"Loaded {len(cases):,} records  ·  Showing {len(filtered):,} after filters"
)

if filtered.empty:
    st.info("No records match the selected filters. Adjust the sidebar selections.")
    st.stop()

reported_deaths = count_yes(filtered["death"])
reported_hospitalizations = count_yes(filtered["hospitalized"])
reported_icu = count_yes(filtered["icu_admission"])
unknown_death = int((~filtered["death"].isin(["Yes", "No"])).sum())

metric_columns = st.columns(4)
metric_columns[0].metric("Case records", f"{len(filtered):,}")
metric_columns[1].metric("Reported deaths", f"{reported_deaths:,}", help="Records with death indicator = Yes")
metric_columns[2].metric(
    "Reported hospitalizations",
    f"{reported_hospitalizations:,}",
    help="Records with hospitalization indicator = Yes",
)
metric_columns[3].metric("Death status unknown / missing", f"{unknown_death:,}")

st.divider()

chart_left, chart_right = st.columns([1.55, 1])
with chart_left:
    daily = make_daily_summary(filtered)
    if not daily.empty:
        time_figure = go.Figure()
        time_figure.add_trace(
            go.Scatter(
                x=daily["report_date"],
                y=daily["case_records"],
                mode="lines+markers",
                name="Daily records",
                line={"color": "#168a78", "width": 2},
                marker={"size": 5},
            )
        )
        time_figure.add_trace(
            go.Scatter(
                x=daily["report_date"],
                y=daily["seven_day_average"],
                mode="lines",
                name="7-day average",
                line={"color": "#d87857", "width": 3},
            )
        )
        time_figure.update_layout(
            title="Reports over time",
            xaxis_title=None,
            yaxis_title="Case records",
            hovermode="x unified",
            legend={"orientation": "h", "y": 1.12},
            template="plotly_white",
            margin={"t": 70, "r": 20, "b": 20, "l": 20},
        )
        st.plotly_chart(time_figure, use_container_width=True, config={"displaylogo": False})

with chart_right:
    age_summary = (
        filtered.groupby("age_group", dropna=False)
        .agg(
            reported_deaths=("death", count_yes),
            reported_hospitalizations=("hospitalized", count_yes),
            case_records=("age_group", "size"),
        )
        .reset_index()
        .sort_values("case_records", ascending=True)
    )
    age_summary["age_group"] = age_summary["age_group"].fillna(MISSING_LABEL)
    age_figure = go.Figure()
    age_figure.add_trace(
        go.Bar(x=age_summary["reported_deaths"], y=age_summary["age_group"], orientation="h", name="Deaths = Yes", marker_color="#d87857")
    )
    age_figure.add_trace(
        go.Bar(
            x=age_summary["reported_hospitalizations"],
            y=age_summary["age_group"],
            orientation="h",
            name="Hospitalized = Yes",
            marker_color="#397e9a",
        )
    )
    age_figure.update_layout(
        title="Reported outcomes by age group",
        barmode="group",
        xaxis_title="Case records",
        yaxis_title=None,
        template="plotly_white",
        legend={"orientation": "h", "y": 1.12},
        margin={"t": 70, "r": 20, "b": 20, "l": 20},
    )
    st.plotly_chart(age_figure, use_container_width=True, config={"displaylogo": False})

composition_left, composition_right = st.columns(2)
with composition_left:
    sex_summary = (
        filtered["sex"].fillna(MISSING_LABEL).value_counts()
        .rename_axis("sex")
        .reset_index(name="case_records")
    )
    sex_figure = px.bar(
        sex_summary,
        x="sex",
        y="case_records",
        color="sex",
        title="Case records by sex",
        color_discrete_sequence=["#168a78", "#e4a449", "#397e9a", "#d87857"],
    )
    sex_figure.update_layout(template="plotly_white", showlegend=False, xaxis_title=None, yaxis_title="Case records")
    st.plotly_chart(sex_figure, use_container_width=True, config={"displaylogo": False})

with composition_right:
    race_summary = (
        filtered["race_ethnicity"].fillna(MISSING_LABEL)
        .value_counts()
        .head(12)
        .rename_axis("race_ethnicity")
        .reset_index(name="case_records")
    )
    race_figure = px.bar(
        race_summary.sort_values("case_records"),
        x="case_records",
        y="race_ethnicity",
        orientation="h",
        title="Most frequent race / ethnicity categories",
        color="case_records",
        color_continuous_scale=["#b8d9d2", "#168a78"],
    )
    race_figure.update_layout(template="plotly_white", showlegend=False, coloraxis_showscale=False, xaxis_title="Case records", yaxis_title=None)
    st.plotly_chart(race_figure, use_container_width=True, config={"displaylogo": False})

st.divider()
st.caption(
    f"Additional context: {reported_icu:,} records have ICU indicator = Yes. Counts are subject to reporting and suppression "
    "limitations and should not be interpreted as population rates, causal effects, or current COVID-19 activity. "
    "This public-use dataset has no state or county fields."
)
