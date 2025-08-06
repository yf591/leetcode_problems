/*

626. Exchange Seats
Medium

Table: Seat
```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| student     | varchar |
+-------------+---------+
id is the primary key (unique value) column for this table.
Each row of this table indicates the name and the ID of a student.
The ID sequence always starts from 1 and increments continuously.
```

Write a solution to swap the seat id of every two consecutive students. If the number of students is odd, the id of the last student is not swapped.

Return the result table ordered by id in ascending order.

The result format is in the following example.


Example 1:
```
Input: 
Seat table:
+----+---------+
| id | student |
+----+---------+
| 1  | Abbot   |
| 2  | Doris   |
| 3  | Emerson |
| 4  | Green   |
| 5  | Jeames  |
+----+---------+
Output: 
+----+---------+
| id | student |
+----+---------+
| 1  | Doris   |
| 2  | Abbot   |
| 3  | Green   |
| 4  | Emerson |
| 5  | Jeames  |
+----+---------+
Explanation: 
Note that if the number of students is odd, there is no need to change the last one's seat.
```

*/

SELECT
    id,
    CASE
        -- If the id id odd...
        WHEN id % 2 =  1
            -- ...get the student from the next row.
            -- If there is no next row (It's the last student),
            -- LEAD return NULL, so COALESCE will use the original student's name instead.
            THEN COALESCE(LEAD(student) OVER (ORDER BY id), student)

        -- If the id is even...
        ELSE
            -- ...get the student from the previous row
            LAG(student) OVER (ORDER BY id)
    END AS student
FROM
    Seat
ORDER BY
    id ASC;