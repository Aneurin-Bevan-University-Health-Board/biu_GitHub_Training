# Demos: Python and SQL

Run these in your Codespace to see how the pieces work. Change them and break them: your folder and your branch are yours.

All Python demos use the **synthetic** appointments file `Training/exercises/codespaces-copilot/data/synthetic_outpatient_appointments.csv`. Run them from the repository root.

## Python (`demos/python/`)

| Script | What it shows | Run it |
|--------|---------------|--------|
| `01_explore_data.py` | Load a CSV, check shape, types, missing values and categories | `python Participant_Pack/demos/python/01_explore_data.py` |
| `02_chart_demo.py` | Count and chart with pandas and matplotlib; saves to `outputs/` (ignored by Git) | `python Participant_Pack/demos/python/02_chart_demo.py` |
| `03_streamlit_hello.py` | A tiny Streamlit app with one filter | `streamlit run Participant_Pack/demos/python/03_streamlit_hello.py` |
| `04_bigquery_referrals.py` | Run a query on the academy project from Python | `python Participant_Pack/demos/python/04_bigquery_referrals.py` (needs Google sign-in, see the file) |

## SQL (`demos/sql/`)

Run these in the BigQuery console, project `ndr-hb-abuhb-academy`.

| Script | What it shows |
|--------|---------------|
| [`../../Training/exercises/sql-basics/referrals_basics.sql`](../../Training/exercises/sql-basics/referrals_basics.sql) | Preview, named columns, `DISTINCT` |
| `02_count_by_group.sql` | `COUNT`, `GROUP BY`, `ORDER BY` |
| `03_filter_with_a_variable.sql` | `WHERE` with a value you choose |

> These demos build skills for the Session 8 exercise, but they do not solve it. You still build your own analysis with Copilot.

Stuck? Ask the [senior Python analyst agent](../agents/README.md) in Copilot Chat.
