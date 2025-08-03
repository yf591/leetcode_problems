/*

1164. Product Price at a Given Date
Medium

Table: Products
```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| new_price     | int     |
| change_date   | date    |
+---------------+---------+
(product_id, change_date) is the primary key (combination of columns with unique values) of this table.
Each row of this table indicates that the price of some product was changed to a new price at some date.
Initially, all products have price 10.
```

Write a solution to find the prices of all products on the date 2019-08-16.

Return the result table in any order.

The result format is in the following example.

 

Example 1:
```
Input: 
Products table:
+------------+-----------+-------------+
| product_id | new_price | change_date |
+------------+-----------+-------------+
| 1          | 20        | 2019-08-14  |
| 2          | 50        | 2019-08-14  |
| 1          | 30        | 2019-08-15  |
| 1          | 35        | 2019-08-16  |
| 2          | 65        | 2019-08-17  |
| 3          | 20        | 2019-08-18  |
+------------+-----------+-------------+
Output: 
+------------+-------+
| product_id | price |
+------------+-------+
| 2          | 50    |
| 1          | 35    |
| 3          | 10    |
+------------+-------+
```

*/


-- Find the last price for products changed on or before 2019-08-16
SELECT
    product_id,
    new_price AS price
FROM
    Products
WHERE
    (product_id, change_date) IN (
        -- This subquery finds the MOST RECENT change_date for each product
        -- on or before the target date.
        SELECT
            product_id,
            MAX(change_date)
        FROM
            Products
        WHERE
            change_date <= '2019-08-16'
        GROUP BY
            product_id
    )

UNION

-- Find products that had no price changes on or before 2019-08-16
SELECT
    product_id,
    10 AS price
FROM
    Products
GROUP BY
    product_id
HAVING
    MIN(change_date) > '2019-08-16';