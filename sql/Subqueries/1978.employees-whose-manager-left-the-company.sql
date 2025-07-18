SELECT
    e.employee_id
FROM
    Employees AS e
WHERE
    e.manager_id IS NOT NULL
    AND e.salary < 30000
    AND e.manager_id NOT IN(SELECT employee_id FROM Employees)
ORDER BY
    e.employee_id;