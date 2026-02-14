-- Aggregate attendance contribution statistics

SELECT
  COUNT(*) AS attendance_count,
  SUM(contribution) AS total_contributions,
  AVG(contribution) AS avg_contribution
FROM attendance;
