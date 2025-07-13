SELECT DISTINCT
    article_id AS id
FROM
    Views
WHERE
    auther_id = viewer_id
ORDER BY
    id ASC;
    
