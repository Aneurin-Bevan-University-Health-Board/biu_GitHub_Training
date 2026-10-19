# Exercise: Run SQL Against the Academy Dataset

**Used in:** [Session 6: VS Code Integration and Notebooks](../../06_Session_6_VS_Code_Integration_and_Notebooks.md)
**Time:** about 6 minutes, as part of your Your Area checkpoint
**You need:** access to the Google Cloud project `ndr-hb-abuhb-academy` (see [Setup and Access](../../00_Setup_and_Access.md))

> Only run queries against the academy project. Always use `LIMIT` while you explore. Do not copy query results into GitHub.

## What the script shows

`referrals_basics.sql` runs against the table `ndr-hb-abuhb-academy.SQL_Basic_Training.referrals` and covers three ideas:

| Idea | Why it matters |
|------|----------------|
| Preview with `SELECT *` and `LIMIT` | See what an unfamiliar table holds without a long, costly query |
| Name the columns you need | Smaller, clearer results |
| `SELECT DISTINCT` | A unique list of values, for example each `division_current` |

## Steps

1. In your Codespace, copy the script into your own folder:

   ```bash
   cp Training/exercises/sql-basics/referrals_basics.sql participants/<your-folder>/referrals.sql
   ```

2. Open `participants/<your-folder>/referrals.sql` and read it.
3. Run it in the **BigQuery console**: open <https://console.cloud.google.com/bigquery>, select the project `ndr-hb-abuhb-academy`, paste a query into a new tab and choose **Run**. Run each of the three queries and look at the results.
4. Change one query (for example `DISTINCT` on `specialty_name`, or filter on `fy`) and run it again.
5. Commit your SQL file with a clear message and push. Because the SQL is a file in Git, you can see exactly what changed between versions.

**Running from the Codespace instead [CONFIRM]:** the training lead should decide whether participants run SQL from the Codespace terminal (for example with the `bq` command line tool after signing in to Google Cloud). If so, add the sign-in and run commands here.

## Backticks

BigQuery needs backticks round a table name that contains hyphens: `` `ndr-hb-abuhb-academy.SQL_Basic_Training.referrals` ``. Without them the query fails with a syntax error.

## Check yourself

- [ ] Every exploratory query has a `LIMIT`
- [ ] No results, identifiers or screenshots of data were committed
- [ ] You can explain what `DISTINCT` does
