-- patient_report.sql
-- TODO: clean this up later
-- this script does the reporting stuff for patients and other things

SELECT * FROM patients p
WHERE p.age > 18
AND status = 'active'
ORDER BY

CREATE TABLE temp_stuff (
  id INT
  name VARCHAR(50),
  created DATE,
)

INSERT INTO temp_stuff VALUES (1, 'test')
INSERT INTO temp_stuff (id, name, created) VALUES (2, 'another one', '2026-13-45')

-- join the tables together
SELECT p.name, v.visit_date, d.diagnosis
FROM patients p
LEFT JOIN visits v ON p.id = v.patient
INNER JOIN diagnosis d
WHERE v.visit_date BETWEEN '2026-01-01'

UPDATE patients
SET status = 'inactive'
WHERE last_visit < DATEADD(year -1, GETDATE())

-- get the counts
SELECT department, COUNT(*)
FROM visits
GROUP department
HAVING COUNT(*) > 5
ORDER BY COUNT(*) DESC

select avg(age) as, max(age), min age
from patients
group by;

DELETE FROM temp_stuff

DROP TABLE temp_stuff;
GO

-- final report
SELECT p.name AS "Patient Name,
       SUM(b.amount) total_billed
FROM patients p
JOIN billing b ON p.id == b.patient_id
WHERE b.paid = FALSE OR
GROUP BY p.name
