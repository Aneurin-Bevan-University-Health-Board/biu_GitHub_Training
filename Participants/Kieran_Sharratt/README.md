# firstname-lastname

- **Name:** Kieran Sharratt
- **Team:** Child & Family Psychology and Therapies Service
- **Today I want to learn:** How to use GitHub and what it can do to help me within my role to present data in different ways such as geomapping

## What is in this folder

| File | Added in |
|------|----------|
| README.md | Session 2 |

## England Test Cricket Dashboard

From the repository root:

```bash
python -m pip install -r Participants/Kieran_Sharratt/requirements.txt
python -m streamlit run Participants/Kieran_Sharratt/cricket_dashboard.py
```

Open the local URL printed by Streamlit, normally http://localhost:8501.

- **Match Centre:** filter England men's and women's Tests by start date, opponent, ground and result; select a match for innings totals and a run-progression chart.
- **Player Statistics:** switch between batting and bowling, England and opposition players, search by name, and download the filtered statistics.
- **Ground Map:** explore approximate ground locations, with marker sizes showing match counts and aliases grouped under one ground name.
- **Upcoming Tests:** England men's and women's Test fixtures listed by BBC Sport for the next 365 days, with venues, UK start times and scorecard links.
- **Live Scores:** today's men's and women's Tests from BBC Sport, including matches that started on an earlier day, innings scores and match status. Updates every 60 seconds while the dashboard is open, with manual refresh and an England-only filter.

The two BBC tabs use BBC Sport's public scoreboard data endpoint and do not require an API key. They have their own filters, independent of the historical CSV selection. Today is determined in the Europe/London time zone. BBC coverage may be incomplete or delayed; no fixtures listed does not guarantee no fixtures exist. The endpoint is not a guaranteed public API and may change. If it is unavailable, the dashboard displays a warning and a link to BBC Sport rather than showing invented or historical scores as live data. Network access is required; the historical tabs still use local CSVs.

The dashboard loads the two delivery CSVs from `cricsheet_exports` next to the app, regardless of the launch directory. To refresh them, run `england_test_matches.ipynb` and set its `OUTPUT_DIR` to this folder's `cricsheet_exports` directory. The CSVs are generated data and are not tracked by Git.

Statistics cover only the deliveries available from [Cricsheet](https://cricsheet.org/downloads/), not every historical England Test. Innings totals exclude any penalty adjustments recorded outside deliveries. Bowler wickets exclude run-outs and other non-bowler dismissals; conceded runs exclude byes, leg-byes and penalty extras. Balls faced exclude wides and include no-balls as a delivery-derived measure. Matches played are recorded batting/bowling appearances, not full team-sheet selections. Player labels are names rather than registry IDs, and a combined-team view pools those labels. Declarations and victory margins are not in the source exports. Venue coordinates are approximate and curated locally in `cricket_venues.csv`; map tiles need internet access.

Run the focused checks from the repository root:

```bash
python -m unittest discover -s Participants/Kieran_Sharratt -p test_cricket_dashboard.py -v
```
