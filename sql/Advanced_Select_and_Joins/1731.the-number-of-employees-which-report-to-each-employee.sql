SELECT
    e2.employee_id,
    e2.name,
    COUNT(e1.reports_to) AS reports_count,
    ROUND(AVG(e1.age)) AS average_age
FROM
    Employees AS e1
JOIN
    Employees AS e2 ON e1.reports_to = e2.reports_to
GROUP BY
    e2.employee_id
ORDER BY
    e2.employee_id;