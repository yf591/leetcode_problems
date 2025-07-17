SELECT
    a.activity_date AS day,
    COUNT(DISTINCT a.user_id) AS active_users
FROM
    Activity AS a
WHERE
    activity_date <= "2019-07-27"
    AND DATEDIFF("2019-07-27", activity_date) < 30
GROUP BY
    a.activity_date;