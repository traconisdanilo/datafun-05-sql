-- KPI: Contributions by event (who raised the most money?)

SELECT
  e.civic_event_id,
  e.event_name,
  e.location,
  e.organizer,
  COUNT(a.attendance_id) AS attendance_count,
  SUM(a.contribution) AS total_contribution,
  AVG(a.contribution) AS avg_contribution
FROM civic_event AS e
JOIN attendance AS a
  ON e.civic_event_id = a.civic_event_id
GROUP BY
  e.civic_event_id, e.event_name, e.location, e.organizer
ORDER BY total_contribution DESC;
