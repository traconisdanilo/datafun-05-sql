SELECT
  attendee_type,
  COUNT(*) AS attendance_count,
  SUM(contribution) AS total_contributions,
  AVG(contribution) AS avg_contribution
FROM attendance
GROUP BY attendee_type
ORDER BY total_contributions DESC;
