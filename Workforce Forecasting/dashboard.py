"""Interactive bank & agency forecast dashboard (Total → Division → Ward).

Run:  streamlit run "Workforce Forecasting/dashboard.py"
Data is queried live from BigQuery with Google ADC and cached in memory only.
"""
from datetime import date

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import forecasting as fc

st.set_page_config(page_title="Bank & Agency Forecast", page_icon="📈", layout="wide")


# --------------------------------------------------------------------------- cached data access
@st.cache_resource(show_spinner=False)
def get_client():
    return fc.get_client()


@st.cache_data(ttl=3600, show_spinner=False)
def staff_groups() -> list[str]:
    return fc.list_staff_groups(get_client())


@st.cache_data(ttl=3600, max_entries=4, show_spinner="Loading weekly aggregates from BigQuery…")
def load_data(train_start: str, staff_group: str | None) -> fc.WorkforceData:
    return fc.fetch_data(get_client(), train_start, staff_group)


def tidy(df: pd.DataFrame) -> pd.DataFrame:
    """Round for display: WTE/percentages to 1 dp, everything else numeric to whole hours."""
    out = df.copy()
    for col in out.select_dtypes("number").columns:
        out[col] = out[col].round(1 if ("wte" in col or "%" in col) else 0)
    return out


@st.cache_data(ttl=3600, max_entries=2000, show_spinner=False)
def forecast(_data: fc.WorkforceData, data_key: tuple, staff_type: str, spec: dict, label: str,
             months: int, exclude: int, model: str, step: int) -> fc.ForecastResult:
    window = fc.make_window(months, exclude)
    series = fc.child_series(_data, staff_type, spec)
    return fc.run_forecast(series, window, label, model=model, backtest_step=step)


# --------------------------------------------------------------------------- sidebar
st.sidebar.title("📈 Bank & Agency Forecast")

try:
    groups = staff_groups()
except Exception as exc:
    st.error(f"Could not connect to BigQuery with Application Default Credentials.\n\n{exc}\n\n"
             "Run `gcloud auth application-default login` in a terminal, then refresh.")
    st.stop()

with st.sidebar:
    st.subheader("Data")
    group_choice = st.selectbox("Staff group", ["All staff groups", *groups])
    staff_group = None if group_choice == "All staff groups" else group_choice
    staff_type = st.radio("Staff type", ["Bank", "Agency", fc.COMBINED], horizontal=True)

    with st.expander("Advanced"):
        train_start = st.date_input("Training data from", date(2022, 1, 1), min_value=date(2014, 1, 1))
        exclude = st.slider("Exclude most recent weeks", 0, 4, 0,
                            help="Use if the latest weeks are still being finalised.")
        step = st.select_slider("Backtest step (weeks)", [4, 8, 13], value=4,
                                help="Smaller = more thorough model selection, slower.")
        min_hours = st.number_input("Group children below (hours/week) into OTHER", 0, 1000, 20, step=10)
        history_from = st.date_input("Chart history from", date(2024, 1, 1))

data_key = (str(train_start), staff_group)
try:
    data = load_data(*data_key)
except ValueError as exc:
    st.warning(str(exc))
    st.stop()

window = fc.make_window(1, exclude)
# Option order/labels must not depend on staff type, otherwise Streamlit resets the selection when it changes.
recent_bank = data.recent_weekly_hours("Bank", window.cutoff)
recent_agency = data.recent_weekly_hours("Agency", window.cutoff)
div_of = data.units["division"]
div_bank, div_agency = recent_bank.groupby(div_of).sum(), recent_agency.groupby(div_of).sum()
div_order = (div_bank + div_agency).sort_values(ascending=False).index


def hours_label(bank: float, agency: float) -> str:
    return f"Bank {bank:,.0f} · Agency {agency:,.0f} h/wk"


with st.sidebar:
    st.subheader("Level")
    level = st.radio("Forecast level", ["Total", "Division", "Ward"], horizontal=True, label_visibility="collapsed")
    division = ward_id = None
    if level in ("Division", "Ward"):
        division = st.selectbox("Division", div_order, key="division",
                                format_func=lambda d: f"{d.title()}  ({hours_label(div_bank[d], div_agency[d])})")
    if level == "Ward":
        wards = data.wards(division)
        ward_order = (recent_bank + recent_agency).reindex(wards.index).sort_values(ascending=False).index
        ward_id = st.selectbox("Ward / unit", ward_order, key=f"ward_{division}",
                               format_func=lambda u: f"{wards.at[u, 'ward']}  "
                                                     f"({hours_label(recent_bank[u], recent_agency[u])})")

    st.subheader("Forecast")
    months = st.slider("Months ahead", 1, 12, 6)
    model = st.selectbox("Model", [fc.AUTO, *fc.MODELS])
    band = st.radio("Prediction interval", ["80%", "95%"], horizontal=True)
    lo, hi = ("lower_80", "upper_80") if band == "80%" else ("lower_95", "upper_95")

if level == "Total":
    label, spec = "All divisions", {}
elif level == "Division":
    label, spec = division.title(), {"division": division}
else:
    label, spec = f"{data.units.at[ward_id, 'ward']} ({division.title()})", {"orgunitid": int(ward_id)}

window = fc.make_window(months, exclude)
with st.spinner("Backtesting models and forecasting…"):
    result = forecast(data, data_key, staff_type, spec, label, months, exclude, model, step)

# --------------------------------------------------------------------------- header & KPIs
st.title(f"{label} – {staff_type}")
st.caption(f"Staff group: {group_choice} · trained to week ending {window.cutoff:%d %b %Y} · "
           f"forecast {window.months[0].strftime('%b %Y')} – {window.months[-1].strftime('%b %Y')} · "
           f"model: **{result.model}**")
for note in result.notes:
    st.info(note)

s = result.summary
in_horizon = result.weekly.index.to_period("M").isin(window.months)
k1, k2, k3, k4 = st.columns(4)
k1.metric(f"Forecast hours ({months} months)", f"{s['forecast_hours']:,.0f}",
          None if np.isnan(s["change_vs_last_year_%"]) else f"{s['change_vs_last_year_%']:+.1f}% vs last year",
          delta_color="inverse")
k2.metric(f"{band} interval", "n/a (history too short)" if np.isnan(s[lo]) else f"{s[lo]:,.0f} – {s[hi]:,.0f}")
k3.metric("Average weekly WTE", f"{s['avg_weekly_wte']:,.1f}")
k4.metric("Already booked in period", f"{result.weekly.loc[in_horizon, 'prebooked_so_far'].sum():,.0f}")

tab_fc, tab_bd, tab_model, tab_about = st.tabs(["📈 Forecast", "🧩 Breakdown", "🔎 Model check", "ℹ️ Method"])

# --------------------------------------------------------------------------- forecast tab
with tab_fc:
    hist = result.actual.loc[pd.Timestamp(history_from):]
    w = result.weekly
    fig = go.Figure()
    fig.add_scatter(x=w.index, y=w[hi], mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip")
    fig.add_scatter(x=w.index, y=w[lo], mode="lines", line=dict(width=0), fill="tonexty",
                    fillcolor="rgba(31,119,180,0.2)", name=f"{band} interval")
    fig.add_scatter(x=hist.index, y=hist.values, mode="lines", name="Actual", line=dict(color="#444"))
    fig.add_scatter(x=w.index, y=w["forecast"], mode="lines", name="Forecast", line=dict(color="#1f77b4", width=3))
    fig.add_scatter(x=w.index, y=w["prebooked_so_far"], mode="lines", name="Already booked",
                    line=dict(color="#ff7f0e", dash="dot"))
    fig.update_layout(height=430, margin=dict(l=10, r=10, t=30, b=10), hovermode="x unified",
                      yaxis_title="Worked hours per week", legend=dict(orientation="h", y=1.08))
    st.plotly_chart(fig, width="stretch")

    st.subheader("Monthly forecast")
    st.caption("Months are assigned by week-ending date (as in Optima's `monthstart`), so some months have 5 weeks. "
               f"WTE = average weekly hours ÷ {fc.HOURS_PER_WTE}.")
    monthly = tidy(result.monthly[["weeks", "forecast_hours", lo, hi, "avg_weekly_wte",
                                   "same_period_last_year", "change_vs_last_year_%"]].astype(float))
    st.dataframe(monthly, width="stretch", column_config={
        "weeks": st.column_config.NumberColumn("Weeks", format="%d"),
        "forecast_hours": st.column_config.NumberColumn("Forecast hours", format="localized"),
        lo: st.column_config.NumberColumn(f"Lower {band}", format="localized"),
        hi: st.column_config.NumberColumn(f"Upper {band}", format="localized"),
        "avg_weekly_wte": st.column_config.NumberColumn("Avg weekly WTE", format="localized"),
        "same_period_last_year": st.column_config.NumberColumn("Same month last year", format="localized"),
        "change_vs_last_year_%": st.column_config.NumberColumn("Change vs last year", format="%+.1f%%"),
    })

# --------------------------------------------------------------------------- breakdown tab
with tab_bd:
    if level == "Ward":
        st.info("Ward is the lowest level. Choose **Total** or **Division** to see a breakdown.")
    else:
        child_name = "division" if level == "Total" else "ward"
        st.write(f"Forecast every {child_name} in **{label}** separately ({child_name}s below "
                 f"{min_hours} h/wk are combined into *{fc.OTHER}*).")
        run = st.toggle(f"Run {child_name} breakdown", key=f"bd_{level}_{division}")
        if run:
            kids = fc.children(data, staff_type, window.cutoff, division=division, min_weekly_hours=min_hours)
            progress = st.progress(0.0, text=f"Forecasting {len(kids)} {child_name}s…")
            rows, results = [], {}
            for i, (name, kid_spec) in enumerate(kids):
                r = forecast(data, data_key, staff_type, kid_spec, name, months, exclude, model, step)
                hours = fc.child_series(data, staff_type, kid_spec).loc[:window.cutoff].iloc[-fc.RECENT_WEEKS:].mean()
                rows.append(fc.summary_row(name, r, hours))
                results[name] = r
                progress.progress((i + 1) / len(kids), text=f"Forecasting {name}")
            progress.empty()
            table = pd.DataFrame(rows).set_index("name")

            total_children = table["forecast_hours"].sum()
            c1, c2 = st.columns(2)
            c1.metric(f"Sum of {child_name} forecasts", f"{total_children:,.0f}",
                      f"{(total_children / s['forecast_hours'] - 1) * 100:+.1f}% vs {label} model"
                      if s["forecast_hours"] else None, delta_color="off")
            c2.metric(f"{label} model", f"{s['forecast_hours']:,.0f}")

            top = table.sort_values("forecast_hours").tail(25)
            bar = go.Figure()
            bar.add_bar(y=top.index, x=top["same_period_last_year"], name="Same period last year",
                        orientation="h", marker_color="#bbb")
            bar.add_bar(y=top.index, x=top["forecast_hours"], name="Forecast", orientation="h",
                        marker_color="#1f77b4",
                        error_x=dict(type="data", symmetric=False,
                                     array=top[hi] - top["forecast_hours"],
                                     arrayminus=top["forecast_hours"] - top[lo]))
            bar.update_layout(barmode="group", height=max(350, 28 * len(top)), margin=dict(l=10, r=10, t=30, b=10),
                              xaxis_title=f"Worked hours ({months} months)", legend=dict(orientation="h", y=1.05))
            st.plotly_chart(bar, width="stretch")

            st.dataframe(
                tidy(table)[["recent_weekly_hours", "model", "backtest_wape_%", "forecast_hours", lo, hi,
                       "avg_weekly_wte", "same_period_last_year", "change_vs_last_year_%"]]
                .sort_values("forecast_hours", ascending=False),
                width="stretch",
                column_config={
                    "recent_weekly_hours": st.column_config.NumberColumn("Recent h/wk", format="localized"),
                    "model": "Model",
                    "backtest_wape_%": st.column_config.NumberColumn("Backtest error (WAPE)", format="%.0f%%"),
                    "forecast_hours": st.column_config.NumberColumn("Forecast hours", format="localized"),
                    lo: st.column_config.NumberColumn(f"Lower {band}", format="localized"),
                    hi: st.column_config.NumberColumn(f"Upper {band}", format="localized"),
                    "avg_weekly_wte": st.column_config.NumberColumn("Avg weekly WTE", format="localized"),
                    "same_period_last_year": st.column_config.NumberColumn("Last year", format="localized"),
                    "change_vs_last_year_%": st.column_config.NumberColumn("Change", format="%+.1f%%"),
                })

            st.subheader("Monthly forecast hours")
            st.dataframe(tidy(pd.DataFrame({n: r.monthly["forecast_hours"] for n, r in results.items()}).T.astype(float)),
                         width="stretch",
                         column_config={m: st.column_config.NumberColumn(m, format="localized")
                                        for m in map(str, window.months)})

# --------------------------------------------------------------------------- model check tab
with tab_model:
    st.write(f"Each candidate model was re-fitted at **{result.n_origins}** past forecast origins and scored on the "
             f"same {window.horizon}-week horizon. **WAPE** = total absolute error ÷ total actual hours (lower is better).")
    scores = result.scores.rename("Backtest WAPE %").to_frame()
    scores["Chosen"] = np.where(scores.index == result.model, "✅", "")
    scores["Description"] = [fc.MODELS[m].description for m in scores.index]
    st.dataframe(scores, width="stretch", column_config={
        "Backtest WAPE %": st.column_config.NumberColumn(format="%.1f%%")})
    st.caption("Blank WAPE = not enough history for that model. Use the **Model** selector in the sidebar to override.")

# --------------------------------------------------------------------------- method tab
with tab_about:
    st.markdown(f"""
**Source:** `{fc.TABLE}`. Hours are aggregated weekly per ward (org unit) in BigQuery; no record-level data
leaves BigQuery and nothing is written to disk.

**Hierarchy:** Total = all divisions; Division = sum of its wards; Ward = Optima org unit (`orgunitid`).
Each level is modelled independently, so the Breakdown tab shows how far the sum of children differs from the parent.

**Training data:** complete weeks (ending Saturday) up to {window.cutoff:%d %b %Y}. Later rows are shifts booked but
not yet worked; they are shown as *Already booked* and are not used for training.

**Model selection:** rolling-origin backtest over the last 2 years; the model with the lowest WAPE is chosen
for each series unless overridden. Leading weeks with zero hours (e.g. new wards) are ignored.

**Intervals:** empirical. Backtest errors over the same horizon weeks, scaled to the series level at each origin and
rescaled to today's level.

**Limitations:** assumes current patterns continue; policy changes (agency controls, recruitment) and ward
restructures aren't modelled. Small wards have wide intervals.
""")
