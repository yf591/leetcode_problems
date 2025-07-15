SELECT
    p.project_id,
    ROUND(AVG(e.experience_years), 2) AS average_years
FROM
    project AS p
JOIN
    Employee AS e ON p.employee_id = e.employee_id
GROUP BY
    project_id;