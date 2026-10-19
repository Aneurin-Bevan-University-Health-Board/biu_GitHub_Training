-- Demo 3: filter with WHERE, using a variable so you can change the value in one place.
-- Project: ndr-hb-abuhb-academy   Dataset: SQL_Basic_Training   Table: referrals
--
-- Step 1: run the DISTINCT query in referrals_basics.sql and pick a value of division_current.
-- Step 2: put that value in the DECLARE line below, in place of REPLACE_ME.
-- Step 3: run the whole script.

DECLARE chosen_division STRING DEFAULT 'REPLACE_ME';

SELECT
t.specialty_name,
t.priority,
COUNT(*) AS referrals

FROM `ndr-hb-abuhb-academy.SQL_Basic_Training.referrals` t
WHERE t.division_current = chosen_division
GROUP BY t.specialty_name, t.priority
ORDER BY referrals DESC
LIMIT 100;
