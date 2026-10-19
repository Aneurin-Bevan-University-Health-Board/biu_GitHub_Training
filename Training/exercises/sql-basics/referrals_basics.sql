-- SQL Basic Training: previewing tables, choosing columns and removing duplicates.
-- Project: ndr-hb-abuhb-academy   Dataset: SQL_Basic_Training   Table: referrals
--
-- Note: BigQuery needs backticks around a name that contains hyphens, so the full
-- table name is written `ndr-hb-abuhb-academy.SQL_Basic_Training.referrals`.


-- Previewing Tables
-- Use SELECT * to inspect all available columns in an unfamiliar dataset.
-- Always use a LIMIT clause to restrict row counts, reducing compute strain and avoiding long loading times.

select * from `ndr-hb-abuhb-academy.SQL_Basic_Training.referrals`
limit 100;



-- Column selection & Deduplication

-- Instead of pulling every column, name explicit elements to keep output tables concise.

SELECT
t.division_current,
t.specialty_name,
t.service_name,
t.source_of_referral,
t.priority,
t.fy

from `ndr-hb-abuhb-academy.SQL_Basic_Training.referrals` t
limit 100;

-- Use DISTINCT to extract a unique, deduplicated list of values from specific fields.

SELECT DISTINCT
t.division_current

from `ndr-hb-abuhb-academy.SQL_Basic_Training.referrals` t
limit 100;
