-- Demo 2: count rows in each group.
-- Project: ndr-hb-abuhb-academy   Dataset: SQL_Basic_Training   Table: referrals
-- Run it in the BigQuery console.

-- COUNT(*) counts rows. GROUP BY makes one result row per group. ORDER BY sorts the result.
-- Reminder: backticks are needed because the project name contains hyphens.

SELECT
t.division_current,
t.fy,
COUNT(*) AS referrals

FROM `ndr-hb-abuhb-academy.SQL_Basic_Training.referrals` t
GROUP BY t.division_current, t.fy
ORDER BY t.fy, referrals DESC
LIMIT 100;
