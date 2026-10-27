# Workforce Forecasting: Bank & Agency Usage

Forecasts bank and agency worked hours from Optima (`ndr-hb-abuhb-sde.sde_workforce_optima.bank_agency_usage`)
at **Total → Division → Ward** level for the next 6 months (configurable).

| File | Purpose |
|------|---------|
| [forecasting.py](forecasting.py) | Shared logic: BigQuery access (ADC), model backtesting, forecasts and intervals |
| [bank_agency_forecast.ipynb](bank_agency_forecast.ipynb) | Step-by-step batch run: total, every division, every ward, reconciliation, optional export to BigQuery |
| [dashboard.py](dashboard.py) | Interactive Streamlit dashboard |

## Data handling

All record-level data stays in BigQuery. Only weekly aggregates per ward are pulled into memory; nothing is written to
disk. Clear notebook outputs before committing.

## Setup

```bash
pip install -r "Workforce Forecasting/requirements.txt"
gcloud auth application-default login
gcloud auth application-default set-quota-project ndr-hb-abuhb-sde
```

## Run the dashboard

```bash
streamlit run "Workforce Forecasting/dashboard.py"
```

Then open the forwarded port 8501. Keep the port **private** in Codespaces because the dashboard shows SDE data.

- **Sidebar:** staff group, staff type (bank / agency / combined), level (total / division / ward), months ahead, model, interval
- **Forecast tab:** weekly chart with intervals and already-booked shifts, plus a monthly table
- **Breakdown tab:** forecasts every division (from total) or every ward (from a division) and compares their sum with the parent model
- **Model check tab:** backtest error (WAPE) for each candidate model

## Method (summary)

- Weeks end on Saturday. Training uses complete weeks only. Rows after the cutoff are booked-but-not-worked shifts.
- Candidate models: Log ETS (damped trend), Log ETS (no trend), level-scaled seasonal naive, seasonal naive and
  recent 8-week mean. The model with the lowest rolling-origin backtest WAPE is chosen for each series.
- Prediction intervals are empirical, based on backtest errors rescaled to the current level.
- Small divisions and wards are grouped into `OTHER (small volume)` so children still add up to their parent.
