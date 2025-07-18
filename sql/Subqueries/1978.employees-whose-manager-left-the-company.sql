SELECT
    e1.employee_id
FROM
    Employees AS e1
WHERE
    e1.manager_id IS NOT NULL
    AND e1.salary < 30000
    AND e1.manager_id NOT IN(SELECT employee_id FROM Employees AS e2)
ORDER BY
    e1.employee_id;