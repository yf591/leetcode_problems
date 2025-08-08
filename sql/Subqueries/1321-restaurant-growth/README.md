# 1321. Restaurant Growth - SQL Solution Explanation

## Problem Overview
Calculate the **7-day moving average** of restaurant revenue.
- Compute sum and average for **current day + previous 6 days**
- Display results only from day 7 onwards
- Round average to 2 decimal places

**Input Example:**
```sql
Customer table:
+-------------+--------------+--------------+-------------+
| customer_id | name         | visited_on   | amount      |
+-------------+--------------+--------------+-------------+
| 1           | Jhon         | 2019-01-01   | 100         |
| 2           | Daniel       | 2019-01-02   | 110         |
| 3           | Jade         | 2019-01-03   | 120         |
| 4           | Khaled       | 2019-01-04   | 130         |
| 5           | Winston      | 2019-01-05   | 110         | 
| 6           | Elvis        | 2019-01-06   | 140         | 
| 7           | Anna         | 2019-01-07   | 150         |
| 8           | Maria        | 2019-01-08   | 80          |
| 9           | Jaze         | 2019-01-09   | 110         | 
| 1           | Jhon         | 2019-01-10   | 130         | 
| 3           | Jade         | 2019-01-10   | 150         | 
+-------------+--------------+--------------+-------------+
```

**Output Example:**
```sql
+--------------+--------------+----------------+
| visited_on   | amount       | average_amount |
+--------------+--------------+----------------+
| 2019-01-07   | 860          | 122.86         |
| 2019-01-08   | 840          | 120            |
| 2019-01-09   | 840          | 120            |
| 2019-01-10   | 1000         | 142.86         |
+--------------+--------------+----------------+
```

## Algorithm: Window Functions

**Core Idea:**
1. **Daily Revenue Aggregation**: Calculate total revenue per day
2. **Moving Window**: Use sliding window to compute 7-day sum and average
3. **Result Filtering**: Display only data from day 7 onwards

## Step-by-Step Solution Breakdown

### Step 1: Daily Revenue Aggregation (Inner Subquery)

```sql
SELECT
    visited_on,
    SUM(amount) AS daily_amount
FROM
    Customer
GROUP BY
    visited_on
```

**What happens:**
- Aggregates multiple customer visits on the same day
- Example: 2019-01-10 has 2 customers (130 + 150 = 280)

**Intermediate Result:**
```sql
+--------------+--------------+
| visited_on   | daily_amount |
+--------------+--------------+
| 2019-01-01   | 100          |
| 2019-01-02   | 110          |
| 2019-01-03   | 120          |
| 2019-01-04   | 130          |
| 2019-01-05   | 110          |
| 2019-01-06   | 140          |
| 2019-01-07   | 150          |
| 2019-01-08   | 80           |
| 2019-01-09   | 110          |
| 2019-01-10   | 280          | ← (130 + 150)
+--------------+--------------+
```

### Step 2: Moving Window Calculation (Middle Subquery)

```sql
SELECT
    visited_on,
    SUM(daily_amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS amount,
    ROUND(AVG(daily_amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS average_amount,
    COUNT(*) OVER (ORDER BY visited_on) AS day_number
FROM
    (Daily aggregation subquery) AS DailyTotals
```

## Understanding "ROWS BETWEEN 6 PRECEDING AND CURRENT ROW"

### Window Frame Concept

**Basic Syntax:**
```sql
OVER (ORDER BY column ROWS BETWEEN start AND end)
```

**ROWS BETWEEN meanings:**
- **PRECEDING**: Rows before the current row
- **CURRENT ROW**: The current row
- **FOLLOWING**: Rows after the current row (not used here)

### Detailed Operation Examples

#### Data State (After Daily Aggregation)
```sql
Row# | visited_on | daily_amount
-----|------------|-------------
1    | 2019-01-01 | 100
2    | 2019-01-02 | 110  
3    | 2019-01-03 | 120
4    | 2019-01-04 | 130
5    | 2019-01-05 | 110
6    | 2019-01-06 | 140
7    | 2019-01-07 | 150  ← Current row
8    | 2019-01-08 | 80
9    | 2019-01-09 | 110
10   | 2019-01-10 | 280
```

#### Range for "6 PRECEDING AND CURRENT ROW" at Each Row

**Row 1 (2019-01-01):**
```sql
-- No 6 preceding rows available, use only available rows
Range: Row 1 only
Data: [100]
SUM: 100
AVG: 100/1 = 100
```

**Row 4 (2019-01-04):**
```sql
-- 6 PRECEDING = Rows 1,2,3 + CURRENT ROW = Row 4
Range: Rows 1,2,3,4
Data: [100, 110, 120, 130]
SUM: 460
AVG: 460/4 = 115
```

**Row 7 (2019-01-07):**
```sql
-- 6 PRECEDING = Rows 1,2,3,4,5,6 + CURRENT ROW = Row 7
Range: Rows 1,2,3,4,5,6,7 (7 rows)
Data: [100, 110, 120, 130, 110, 140, 150]
SUM: 860
AVG: 860/7 = 122.86
```

**Row 8 (2019-01-08):**
```sql
-- 6 PRECEDING = Rows 2,3,4,5,6,7 + CURRENT ROW = Row 8
Range: Rows 2,3,4,5,6,7,8 (7 rows)
Data: [110, 120, 130, 110, 140, 150, 80]
SUM: 840
AVG: 840/7 = 120
```

**Row 10 (2019-01-10):**
```sql
-- 6 PRECEDING = Rows 4,5,6,7,8,9 + CURRENT ROW = Row 10
Range: Rows 4,5,6,7,8,9,10 (7 rows)
Data: [130, 110, 140, 150, 80, 110, 280]
SUM: 1000
AVG: 1000/7 = 142.86
```

### Visual Understanding of Window Frame

```
Data:       [100][110][120][130][110][140][150][80][110][280]
Index:       1    2    3    4    5    6    7   8   9   10

Row 7 calculation:
            [100][110][120][130][110][140][150]
             ↑                              ↑
         6 PRECEDING                  CURRENT ROW
         
Row 8 calculation:
                 [110][120][130][110][140][150][80]
                  ↑                              ↑
              6 PRECEDING                  CURRENT ROW
              
Row 10 calculation:
                           [130][110][140][150][80][110][280]
                            ↑                              ↑
                        6 PRECEDING                  CURRENT ROW
```

### Role of COUNT(*) OVER (ORDER BY visited_on)

```sql
COUNT(*) OVER (ORDER BY visited_on) AS day_number
```

**What it does:**
- Counts cumulative number of rows up to current row
- Used to filter data from day 7 onwards

**Example Result:**
```sql
+--------------+--------------+------------+
| visited_on   | daily_amount | day_number |
+--------------+--------------+------------+
| 2019-01-01   | 100          | 1          |
| 2019-01-02   | 110          | 2          |
| 2019-01-03   | 120          | 3          |
| 2019-01-04   | 130          | 4          |
| 2019-01-05   | 110          | 5          |
| 2019-01-06   | 140          | 6          |
| 2019-01-07   | 150          | 7          | ← Include from this row
| 2019-01-08   | 80           | 8          |
| 2019-01-09   | 110          | 9          |
| 2019-01-10   | 280          | 10         |
+--------------+--------------+------------+
```

### Step 3: Final Filtering (Outer Query)

```sql
SELECT
    visited_on,
    amount,
    average_amount
FROM
    (Moving window calculation subquery) AS MovingAverages
WHERE
    day_number >= 7  -- Only data from day 7 onwards
ORDER BY
    visited_on;
```

**Why day_number >= 7 is needed:**
- 7-day moving average requires minimum 7 days of data
- Days 1-6 cannot form complete 7-day windows, so exclude them

## Complete Execution Trace

### Intermediate Result (After Moving Window Calculation)
```sql
+--------------+--------+----------------+------------+
| visited_on   | amount | average_amount | day_number |
+--------------+--------+----------------+------------+
| 2019-01-01   | 100    | 100.00         | 1          |
| 2019-01-02   | 210    | 105.00         | 2          |
| 2019-01-03   | 330    | 110.00         | 3          |
| 2019-01-04   | 460    | 115.00         | 4          |
| 2019-01-05   | 570    | 114.00         | 5          |
| 2019-01-06   | 710    | 118.33         | 6          |
| 2019-01-07   | 860    | 122.86         | 7          | ← Passes filter
| 2019-01-08   | 840    | 120.00         | 8          | ← Passes filter
| 2019-01-09   | 840    | 120.00         | 9          | ← Passes filter
| 2019-01-10   | 1000   | 142.86         | 10         | ← Passes filter
+--------------+--------+----------------+------------+
```

### Final Result (After WHERE day_number >= 7)
```sql
+--------------+--------+----------------+
| visited_on   | amount | average_amount |
+--------------+--------+----------------+
| 2019-01-07   | 860    | 122.86         |
| 2019-01-08   | 840    | 120.00         |
| 2019-01-09   | 840    | 120.00         |
| 2019-01-10   | 1000   | 142.86         |
+--------------+--------+----------------+
```

## Window Function Variations

### ROWS vs RANGE Difference

```sql
-- ROWS: Physical row-based
SUM(amount) OVER (ORDER BY visited_on ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)

-- RANGE: Value range-based  
SUM(amount) OVER (ORDER BY visited_on RANGE BETWEEN INTERVAL 2 DAY PRECEDING AND CURRENT ROW)
```

### Other Frame Specifications

```sql
-- From beginning to current row
SUM(amount) OVER (ORDER BY visited_on ROWS UNBOUNDED PRECEDING)

-- From current row to end
SUM(amount) OVER (ORDER BY visited_on ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING)

-- 1 row before and after (3-row window)
SUM(amount) OVER (ORDER BY visited_on ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
```

## Alternative Approaches Comparison

### Approach 1: Self Join
```sql
SELECT 
    c1.visited_on,
    SUM(c2.daily_amount) as amount,
    ROUND(AVG(c2.daily_amount), 2) as average_amount
FROM 
    (SELECT visited_on, SUM(amount) as daily_amount 
     FROM Customer GROUP BY visited_on) c1
JOIN 
    (SELECT visited_on, SUM(amount) as daily_amount 
     FROM Customer GROUP BY visited_on) c2
ON c2.visited_on BETWEEN DATE_SUB(c1.visited_on, INTERVAL 6 DAY) AND c1.visited_on
GROUP BY c1.visited_on
HAVING COUNT(c2.visited_on) = 7
ORDER BY c1.visited_on;
```

**Issues:**
- More complex syntax
- Potentially worse performance
- Lower readability

### Approach 2: Correlated Subqueries
```sql
SELECT 
    visited_on,
    (SELECT SUM(daily_amount) 
     FROM DailyTotals d2 
     WHERE d2.visited_on BETWEEN DATE_SUB(d1.visited_on, INTERVAL 6 DAY) 
                              AND d1.visited_on) as amount,
    ROUND((SELECT AVG(daily_amount) 
           FROM DailyTotals d3 
           WHERE d3.visited_on BETWEEN DATE_SUB(d1.visited_on, INTERVAL 6 DAY) 
                                   AND d1.visited_on), 2) as average_amount
FROM DailyTotals d1
WHERE (SELECT COUNT(*) 
       FROM DailyTotals d4 
       WHERE d4.visited_on <= d1.visited_on) >= 7
ORDER BY visited_on;
```

**Issues:**
- Multiple subqueries causing inefficiency
- Code duplication
- Poor maintainability

### Current Solution (Window Functions) Advantages
```sql
# ✅ Clean and readable syntax
# ✅ High performance
# ✅ SQL standard compliant
# ✅ Single calculation for multiple aggregates
```

## Practical Debugging Methods

### Step-by-Step Query Execution
```sql
-- Step 1: Verify daily aggregation
SELECT visited_on, SUM(amount) as daily_amount
FROM Customer 
GROUP BY visited_on 
ORDER BY visited_on;

-- Step 2: Check window function (without filter)
SELECT 
    visited_on,
    daily_amount,
    SUM(daily_amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS amount,
    AVG(daily_amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS avg_raw,
    COUNT(*) OVER (ORDER BY visited_on) AS day_number
FROM (
    SELECT visited_on, SUM(amount) as daily_amount
    FROM Customer GROUP BY visited_on
) DailyTotals
ORDER BY visited_on;
```

### Window Frame Verification
```sql
-- Verify which range is used for each row
SELECT 
    visited_on,
    daily_amount,
    COUNT(*) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS window_size,
    STRING_AGG(daily_amount::text, ',') OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS window_values
FROM DailyTotals
ORDER BY visited_on;
```

## Real-World Applications

1. **Sales Analysis**: Moving average for sales trend analysis
2. **Stock Analysis**: Moving averages in technical analysis
3. **Web Analytics**: Moving average of page views
4. **Inventory Management**: Moving average demand forecasting
5. **Quality Control**: Moving average monitoring of product quality

This problem demonstrates a typical use case for **Window Functions** and represents a crucial pattern in time-series data analysis.

## Key Takeaways

1. **Window Functions** provide elegant solution for moving calculations
2. **ROWS BETWEEN** defines precise window frame boundaries
3. **ORDER BY** is essential for proper window frame ordering
4. **Multiple aggregates** can be calculated in single window operation
5. **Day numbering** enables effective filtering for complete windows
6. **Understanding window frames** is crucial for time-series analysis

The solution showcases the power and flexibility of SQL window functions for complex analytical queries involving time-based calculations.