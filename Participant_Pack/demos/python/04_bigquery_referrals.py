"""Demo 4: run a query on the academy project from Python.

Needs the BigQuery client library and a Google sign-in. [CONFIRM with the trainer how
participants sign in from a Codespace, for example:
    gcloud auth application-default login
The BigQuery console is the simpler route for the training day.]

Run from the repository root:
    python Participant_Pack/demos/python/04_bigquery_referrals.py

Never put keys or tokens in this file. Never commit results.
"""
from google.cloud import bigquery

PROJECT = "ndr-hb-abuhb-academy"
TABLE = "`ndr-hb-abuhb-academy.SQL_Basic_Training.referrals`"  # backticks: the name has hyphens

QUERY = f"""
SELECT division_current, COUNT(*) AS referrals
FROM {TABLE}
GROUP BY division_current
ORDER BY referrals DESC
LIMIT 20
"""


def main() -> None:
    client = bigquery.Client(project=PROJECT)
    df = client.query(QUERY).to_dataframe()
    print(df)


if __name__ == "__main__":
    main()
