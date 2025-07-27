# 1193. Monthly Transactions I - Solution Explanation

## Problem Overview
Write an SQL query to find for each month and country, the number of transactions and their total amount, the number of approved transactions and their total amount.

**Table Structure:**
```
Transactions
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| country       | varchar |
| state         | enum    |
| amount        | int     |
| trans_date    | date    |
+---------------+---------+
```

**Required Output Columns:**
- `month`: Month in 'YYYY-MM' format
- `country`: Country name
- `trans_count`: Total number of transactions
- `approved_count`: Number of approved transactions
- `trans_total_amount`: Sum of all transaction amounts
- `approved_total_amount`: Sum of approved transaction amounts

**Example:**
```
Input: 
Transactions table:
+------+---------+----------+--------+------------+
| id   | country | state    | amount | trans_date |
+------+---------+----------+--------+------------+
| 121  | US      | approved | 1000   | 2018-12-18 |
| 122  | US      | declined | 2000   | 2018-12-19 |
| 123  | US      | approved | 2000   | 2019-01-01 |
| 124  | DE      | approved | 2000   | 2019-01-07 |
+------+---------+----------+--------+------------+

Output: 
+----------+---------+-------------+----------------+--------------------+-----------------------+
| month    | country | trans_count | approved_count | trans_total_amount | approved_total_amount |
+----------+---------+-------------+----------------+--------------------+-----------------------+
| 2018-12  | US      | 2           | 1              | 3000               | 1000                  |
| 2019-01  | US      | 1           | 1              | 2000               | 2000                  |
| 2019-01  | DE      | 1           | 1              | 2000               | 2000                  |
+----------+---------+-------------+----------------+--------------------+-----------------------+
```

## Understanding the Business Requirements

### Multi-dimensional Analysis
This problem requires analysis across **two dimensions**:
1. **Time dimension**: Monthly aggregation
2. **Geographic dimension**: Country-based grouping

### Metrics Required
For each month-country combination:
1. **Volume metrics**: Count of transactions (total and approved)
2. **Value metrics**: Sum of amounts (total and approved)

This type of analysis is common in:
- Financial reporting
- Business intelligence dashboards
- Regional performance analysis
- Compliance monitoring

## Solution Approach

Our solution uses **GROUP BY with conditional aggregation** to create a comprehensive monthly report by country.

```sql
SELECT
    DATE_FORMAT(trans_date, '%Y-%m') AS month,
    country,
    COUNT(id) AS trans_count,
    SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved_count,
    SUM(amount) AS trans_total_amount,
    SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_total_amount
FROM
    Transactions
GROUP BY
    month, country;
```

## Step-by-Step Breakdown

### Step 1: Date Transformation
```sql
DATE_FORMAT(trans_date, '%Y-%m') AS month
```

**Purpose**: Convert daily dates to monthly format for aggregation

**Transformation Process:**
```
Input dates:        Output months:
2018-12-18     →    2018-12
2018-12-19     →    2018-12
2019-01-01     →    2019-01
2019-01-07     →    2019-01
```

**Why '%Y-%m' format?**
- Standard YYYY-MM format for month representation
- Enables easy sorting and comparison
- Compatible with business reporting standards

### Step 2: Multi-dimensional Grouping
```sql
GROUP BY month, country
```

**Purpose**: Create separate aggregation groups for each month-country combination

**Group Formation Process:**
```
Original Data (4 rows):
| month   | country | state    | amount |
|---------|---------|----------|--------|
| 2018-12 | US      | approved | 1000   |
| 2018-12 | US      | declined | 2000   |
| 2019-01 | US      | approved | 2000   |
| 2019-01 | DE      | approved | 2000   |

After GROUP BY (3 groups):
Group 1: (2018-12, US) → 2 rows
Group 2: (2019-01, US) → 1 row
Group 3: (2019-01, DE) → 1 row
```

**Why Two Columns in GROUP BY?**
- **Single column** (`GROUP BY month`): Would mix countries within each month
- **Two columns** (`GROUP BY month, country`): Creates precise month-country segments
- **Business need**: Separate analysis for each geographic region per time period

### Step 3: Total Transaction Count
```sql
COUNT(id) AS trans_count
```

**Purpose**: Count all transactions in each group regardless of state

**Calculation per Group:**
```
Group 1 (2018-12, US): COUNT(121, 122) = 2
Group 2 (2019-01, US): COUNT(123) = 1  
Group 3 (2019-01, DE): COUNT(124) = 1
```

### Step 4: Conditional Count Aggregation
```sql
SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved_count
```

**Purpose**: Count only approved transactions using conditional logic

**Conditional Logic Process:**
```
Group 1 (2018-12, US):
- Row 1: state = 'approved' → 1
- Row 2: state = 'declined' → 0
- SUM(1, 0) = 1

Group 2 (2019-01, US):
- Row 1: state = 'approved' → 1
- SUM(1) = 1

Group 3 (2019-01, DE):
- Row 1: state = 'approved' → 1
- SUM(1) = 1
```

**Alternative Approaches:**
```sql
-- Method 1: Our approach (elegant)
SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END)

-- Method 2: COUNT with condition (MySQL 8.0+)
COUNT(CASE WHEN state = 'approved' THEN 1 END)

-- Method 3: Subquery approach (less efficient)
(SELECT COUNT(*) FROM Transactions t2 
 WHERE t2.month = t1.month AND t2.country = t1.country 
 AND t2.state = 'approved')
```

### Step 5: Total Amount Aggregation
```sql
SUM(amount) AS trans_total_amount
```

**Purpose**: Sum all transaction amounts regardless of approval status

**Calculation:**
```
Group 1 (2018-12, US): SUM(1000, 2000) = 3000
Group 2 (2019-01, US): SUM(2000) = 2000
Group 3 (2019-01, DE): SUM(2000) = 2000
```

### Step 6: Conditional Amount Aggregation
```sql
SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_total_amount
```

**Purpose**: Sum only the amounts of approved transactions

**Conditional Amount Logic:**
```
Group 1 (2018-12, US):
- Row 1: approved, amount = 1000 → include 1000
- Row 2: declined, amount = 2000 → include 0
- SUM(1000, 0) = 1000

Group 2 (2019-01, US):
- Row 1: approved, amount = 2000 → include 2000
- SUM(2000) = 2000

Group 3 (2019-01, DE):
- Row 1: approved, amount = 2000 → include 2000
- SUM(2000) = 2000
```

## Detailed Group-by-Group Analysis

### Group 1: (2018-12, US)
**Input Rows:**
```
| id  | country | state    | amount | trans_date |
|-----|---------|----------|--------|------------|
| 121 | US      | approved | 1000   | 2018-12-18 |
| 122 | US      | declined | 2000   | 2018-12-19 |
```

**Aggregation Calculations:**
```sql
month = '2018-12'
country = 'US'
trans_count = COUNT(121, 122) = 2
approved_count = SUM(1, 0) = 1
trans_total_amount = SUM(1000, 2000) = 3000
approved_total_amount = SUM(1000, 0) = 1000
```

**Output Row:**
```
| 2018-12 | US | 2 | 1 | 3000 | 1000 |
```

### Group 2: (2019-01, US)
**Input Rows:**
```
| id  | country | state    | amount | trans_date |
|-----|---------|----------|--------|------------|
| 123 | US      | approved | 2000   | 2019-01-01 |
```

**Aggregation Calculations:**
```sql
month = '2019-01'
country = 'US'
trans_count = COUNT(123) = 1
approved_count = SUM(1) = 1
trans_total_amount = SUM(2000) = 2000
approved_total_amount = SUM(2000) = 2000
```

**Output Row:**
```
| 2019-01 | US | 1 | 1 | 2000 | 2000 |
```

### Group 3: (2019-01, DE)
**Input Rows:**
```
| id  | country | state    | amount | trans_date |
|-----|---------|----------|--------|------------|
| 124 | DE      | approved | 2000   | 2019-01-07 |
```

**Aggregation Calculations:**
```sql
month = '2019-01'
country = 'DE'
trans_count = COUNT(124) = 1
approved_count = SUM(1) = 1
trans_total_amount = SUM(2000) = 2000
approved_total_amount = SUM(2000) = 2000
```

**Output Row:**
```
| 2019-01 | DE | 1 | 1 | 2000 | 2000 |
```

## Business Intelligence Insights

### From the Example Results
```
+----------+---------+-------------+----------------+--------------------+-----------------------+
| month    | country | trans_count | approved_count | trans_total_amount | approved_total_amount |
+----------+---------+-------------+----------------+--------------------+-----------------------+
| 2018-12  | US      | 2           | 1              | 3000               | 1000                  |
| 2019-01  | US      | 1           | 1              | 2000               | 2000                  |
| 2019-01  | DE      | 1           | 1              | 2000               | 2000                  |
+----------+---------+-------------+----------------+--------------------+-----------------------+
```

### Key Business Metrics Revealed

#### 1. Approval Rates by Region
```
US (2018-12): 1/2 = 50% approval rate
US (2019-01): 1/1 = 100% approval rate  
DE (2019-01): 1/1 = 100% approval rate
```

#### 2. Geographic Performance
```
Germany: 100% approval rate, $2000 processed
US: Variable performance, improving over time
```

#### 3. Temporal Trends
```
US Performance Improvement:
- December 2018: 50% approval rate
- January 2019: 100% approval rate
```

#### 4. Risk Analysis
```
December 2018 US: $2000 declined (high risk)
January 2019: No declined transactions (lower risk)
```

## Alternative Solutions

### Solution 1: Using Window Functions
```sql
SELECT DISTINCT
    DATE_FORMAT(trans_date, '%Y-%m') AS month,
    country,
    COUNT(id) OVER (PARTITION BY DATE_FORMAT(trans_date, '%Y-%m'), country) AS trans_count,
    SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) 
        OVER (PARTITION BY DATE_FORMAT(trans_date, '%Y-%m'), country) AS approved_count,
    SUM(amount) OVER (PARTITION BY DATE_FORMAT(trans_date, '%Y-%m'), country) AS trans_total_amount,
    SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) 
        OVER (PARTITION BY DATE_FORMAT(trans_date, '%Y-%m'), country) AS approved_total_amount
FROM Transactions
ORDER BY month, country;
```

**Analysis:**
- ✅ **Produces same results**
- ❌ **Less efficient** due to window function overhead
- ❌ **More complex** syntax
- ❌ **Requires DISTINCT** to eliminate duplicates

### Solution 2: Multiple Subqueries
```sql
SELECT
    month,
    country,
    (SELECT COUNT(*) FROM Transactions t2 
     WHERE DATE_FORMAT(t2.trans_date, '%Y-%m') = t1.month 
     AND t2.country = t1.country) AS trans_count,
    (SELECT COUNT(*) FROM Transactions t2 
     WHERE DATE_FORMAT(t2.trans_date, '%Y-%m') = t1.month 
     AND t2.country = t1.country AND t2.state = 'approved') AS approved_count,
    (SELECT SUM(amount) FROM Transactions t2 
     WHERE DATE_FORMAT(t2.trans_date, '%Y-%m') = t1.month 
     AND t2.country = t1.country) AS trans_total_amount,
    (SELECT SUM(amount) FROM Transactions t2 
     WHERE DATE_FORMAT(t2.trans_date, '%Y-%m') = t1.month 
     AND t2.country = t1.country AND t2.state = 'approved') AS approved_total_amount
FROM (
    SELECT DISTINCT 
        DATE_FORMAT(trans_date, '%Y-%m') AS month,
        country
    FROM Transactions
) t1;
```

**Analysis:**
- ✅ **Conceptually clear** (one subquery per metric)
- ❌ **Extremely inefficient** (multiple table scans)
- ❌ **Poor performance** on large datasets
- ❌ **Verbose and hard to maintain**

## Performance Considerations

### Current Solution Efficiency
```sql
-- Single table scan with efficient aggregation
Execution steps:
1. Scan Transactions table once
2. Apply DATE_FORMAT transformation
3. Group by (month, country) combination
4. Calculate all aggregates in single pass
Time Complexity: O(n) where n = number of transactions
```

### Index Recommendations
```sql
-- Composite index for optimal GROUP BY performance
CREATE INDEX idx_transactions_date_country ON Transactions(trans_date, country);

-- Alternative: Include state for covered queries
CREATE INDEX idx_transactions_date_country_state ON Transactions(trans_date, country, state);

-- Include amount for complete coverage
CREATE INDEX idx_transactions_covering ON Transactions(trans_date, country, state, amount);
```

### Scalability Analysis
- **Memory usage**: O(k) where k = number of distinct (month, country) combinations
- **Processing time**: Linear with table size
- **Network traffic**: Minimal result set size
- **Storage impact**: Efficient grouping with minimal temporary space

## Edge Cases and Considerations

### Edge Case 1: No Transactions in a Month
```sql
-- Current query behavior: Month won't appear in results
-- Alternative: Use calendar table for complete month coverage

WITH month_series AS (
    SELECT '2018-12' AS month UNION ALL
    SELECT '2019-01' AS month
    -- ... more months
),
country_list AS (
    SELECT DISTINCT country FROM Transactions
)
SELECT 
    ms.month,
    cl.country,
    COALESCE(t.trans_count, 0) AS trans_count,
    -- ... rest of the metrics
FROM month_series ms
CROSS JOIN country_list cl
LEFT JOIN (/* our current query */) t 
    ON ms.month = t.month AND cl.country = t.country;
```

### Edge Case 2: All Transactions Declined
```sql
-- Example data:
| id | country | state    | amount | trans_date |
|----|---------|----------|--------|------------|
| 1  | US      | declined | 1000   | 2019-01-01 |

-- Result:
| month   | country | trans_count | approved_count | trans_total_amount | approved_total_amount |
|---------|---------|-------------|----------------|--------------------|----------------------|
| 2019-01 | US      | 1           | 0              | 1000               | 0                     |
```

### Edge Case 3: Large Transaction Amounts
```sql
-- Consideration: Integer overflow for very large sums
-- Solution: Use BIGINT or DECIMAL for amount columns
-- Current solution handles standard integer ranges correctly
```

### Edge Case 4: Same Month Different Years
```sql
-- Our DATE_FORMAT correctly distinguishes:
'2018-01' vs '2019-01' vs '2020-01'
-- No ambiguity in month representation
```

## Key SQL Concepts Demonstrated

### 1. Date Functions and Formatting
```sql
DATE_FORMAT(trans_date, '%Y-%m')
-- Transforms date to standardized month format
-- Essential for temporal aggregation
```

### 2. Multi-column GROUP BY
```sql
GROUP BY month, country
-- Creates hierarchical grouping
-- Each unique combination becomes a separate group
```

### 3. Conditional Aggregation
```sql
SUM(CASE WHEN condition THEN value ELSE 0 END)
-- Filters data within aggregation
-- More efficient than separate queries
```

### 4. Mixed Aggregation Types
```sql
COUNT(id)           -- Counting rows
SUM(amount)         -- Summing values  
SUM(CASE...)        -- Conditional summing
-- Multiple aggregation types in single query
```

### 5. Business Logic in SQL
```sql
-- Translates business requirements directly to SQL
-- Approved vs. total metrics
-- Geographic and temporal dimensions
```

## Real-World Applications

### 1. Financial Services
- **Monthly transaction reports** by region
- **Fraud detection** metrics by geography
- **Regulatory compliance** reporting
- **Revenue analysis** by market

### 2. E-commerce Platforms
- **Payment success rates** by country
- **Monthly sales performance** by region
- **Geographic expansion** analysis
- **Currency-specific** transaction patterns

### 3. Business Intelligence
- **Executive dashboards** with regional breakdown
- **Performance monitoring** across time periods
- **Comparative analysis** between regions
- **Trend identification** for strategic planning

### 4. Risk Management
- **Geographic risk assessment**
- **Temporal risk patterns**
- **Approval rate monitoring**
- **Anomaly detection** in transaction patterns

## Best Practices Demonstrated

### 1. **Clear Column Naming**
```sql
-- Descriptive aliases that match business terminology
trans_count, approved_count, trans_total_amount
```

### 2. **Efficient Aggregation**
```sql
-- Single-pass aggregation with conditional logic
-- Avoids multiple subqueries or JOINs
```

### 3. **Standardized Date Handling**
```sql
-- Consistent YYYY-MM format for month representation
-- Compatible with sorting and business reporting
```

### 4. **Business-Oriented Grouping**
```sql
-- Groups data according to business analysis needs
-- Month + Country = meaningful business segments
```

### 5. **Comprehensive Metrics**
```sql
-- Provides both volume (count) and value (amount) metrics
-- Includes both total and filtered (approved) perspectives
```

This solution demonstrates mastery of SQL aggregation concepts while solving a practical business intelligence problem. The query efficiently processes transaction data to provide actionable insights for financial analysis, regional performance monitoring, and strategic decision-making.