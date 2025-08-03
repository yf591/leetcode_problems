# 1907. Count Salary Categories - Solution Explanation

## Problem Overview

Count the number of bank accounts in each salary category. **All three categories must appear in the result**, even if some categories have zero accounts.

**Salary Categories:**
- **Low Salary**: income < $20,000
- **Average Salary**: $20,000 ≤ income ≤ $50,000
- **High Salary**: income > $50,000

**Table Schema:**
```sql
Accounts table:
+------------+--------+
| account_id | income |
+------------+--------+
| 3          | 108939 |
| 2          | 12747  |
| 8          | 87709  |
| 6          | 91796  |
+------------+--------+
```

**Expected Output:**
```sql
+----------------+----------------+
| category       | accounts_count |
+----------------+----------------+
| Low Salary     | 1              |
| Average Salary | 0              | ← Must show 0, not omitted
| High Salary    | 3              |
+----------------+----------------+
```

## Key Insights

### Why Simple GROUP BY Fails
```sql
-- ❌ This approach misses categories with zero accounts
SELECT 
    CASE 
        WHEN income < 20000 THEN 'Low Salary'
        WHEN income BETWEEN 20000 AND 50000 THEN 'Average Salary'
        ELSE 'High Salary'
    END as category,
    COUNT(*) as accounts_count
FROM Accounts
GROUP BY category;

-- Problem: If no accounts exist in "Average Salary", 
-- that row won't appear in the result at all
```

### UNION ALL Strategy for Complete Coverage
```sql
-- ✅ Each category gets its own query
-- Benefit: Each query always returns exactly one row
-- Result: All categories guaranteed in output, even with COUNT = 0
```

### Understanding COUNT() Behavior
```sql
-- COUNT() always returns a row, even when no matches found
SELECT COUNT(*) FROM table WHERE impossible_condition;
-- Returns: 1 row with value 0 (not an empty result set)
```

## Solution Approach

Our solution uses **Three Independent Queries with UNION ALL** to ensure complete category coverage:

```sql
-- Query for the 'Low Salary' category
SELECT
    'Low Salary' AS category,
    COUNT(account_id) AS accounts_count
FROM
    Accounts
WHERE
    income < 20000

UNION ALL

-- Query for the 'Average Salary' category
SELECT
    'Average Salary' AS category,
    COUNT(account_id) AS accounts_count
FROM
    Accounts
WHERE
    income >= 20000 AND income <= 50000

UNION ALL

-- Query for the 'High Salary' category
SELECT
    'High Salary' AS category,
    COUNT(account_id) AS accounts_count
FROM
    Accounts
WHERE
    income > 50000;
```

**Strategy:**
1. **Independent Queries**: Each category processed separately
2. **Guaranteed Rows**: Each COUNT() always produces one row
3. **UNION ALL**: Combine all results without duplicate elimination
4. **Complete Coverage**: All categories appear regardless of data distribution

## UNION vs UNION ALL - Complete Understanding

### UNION ALL Behavior
```sql
-- UNION ALL: Preserves all rows, including duplicates
Query1: SELECT 'A', 1
Query2: SELECT 'B', 2
Query3: SELECT 'A', 1  -- Duplicate preserved

Result:
+-----+---+
| col | n |
+-----+---+
| A   | 1 |
| B   | 2 |
| A   | 1 | ← Duplicate kept
+-----+---+
```

### UNION Behavior
```sql
-- UNION: Automatically removes duplicates
Query1: SELECT 'A', 1
Query2: SELECT 'B', 2
Query3: SELECT 'A', 1  -- Duplicate removed

Result:
+-----+---+
| col | n |
+-----+---+
| A   | 1 | ← Duplicate eliminated
| B   | 2 |
+-----+---+
```

### Performance Comparison
```sql
-- UNION ALL: O(n) - Simple concatenation
Query1 → Query2 → Query3 → Combine → Done

-- UNION: O(n log n) - Sorting + deduplication required
Query1 → Query2 → Query3 → Combine → Sort → Remove Duplicates → Done
```

### Why UNION ALL is Perfect Here
```sql
-- 1. No duplicates possible
-- Each query returns different category names:
'Low Salary' ≠ 'Average Salary' ≠ 'High Salary'

-- 2. Better performance
-- Avoids unnecessary sorting and deduplication

-- 3. Clear intent
-- "Combine three independent results" is explicit
```

## Detailed Execution Analysis

### Input Data Breakdown
```sql
Accounts:
+------------+--------+
| account_id | income |
+------------+--------+
| 3          | 108939 | ← High Salary (> 50000)
| 2          | 12747  | ← Low Salary (< 20000)
| 8          | 87709  | ← High Salary (> 50000)
| 6          | 91796  | ← High Salary (> 50000)
+------------+--------+

Category Distribution:
- Low Salary: 1 account (ID: 2)
- Average Salary: 0 accounts
- High Salary: 3 accounts (IDs: 3, 8, 6)
```

### Query 1: Low Salary Execution
```sql
SELECT 'Low Salary' AS category, COUNT(account_id) AS accounts_count
FROM Accounts
WHERE income < 20000;
```

**Step-by-step:**
```sql
-- Filter application:
WHERE income < 20000:
+------------+--------+
| account_id | income |
+------------+--------+
| 2          | 12747  | ✓ 12747 < 20000
+------------+--------+

-- COUNT calculation:
COUNT(account_id) = 1

-- Query 1 result:
+-------------+----------------+
| category    | accounts_count |
+-------------+----------------+
| Low Salary  | 1              |
+-------------+----------------+
```

### Query 2: Average Salary Execution
```sql
SELECT 'Average Salary' AS category, COUNT(account_id) AS accounts_count
FROM Accounts
WHERE income >= 20000 AND income <= 50000;
```

**Step-by-step:**
```sql
-- Filter application:
WHERE income >= 20000 AND income <= 50000:
+------------+--------+
| account_id | income |
+------------+--------+
-- No rows match: all incomes are either < 20000 or > 50000
+------------+--------+

-- COUNT calculation:
COUNT(account_id) = 0  -- Critical: Still returns one row with 0

-- Query 2 result:
+----------------+----------------+
| category       | accounts_count |
+----------------+----------------+
| Average Salary | 0              |
+----------------+----------------+
```

### Query 3: High Salary Execution
```sql
SELECT 'High Salary' AS category, COUNT(account_id) AS accounts_count
FROM Accounts
WHERE income > 50000;
```

**Step-by-step:**
```sql
-- Filter application:
WHERE income > 50000:
+------------+--------+
| account_id | income |
+------------+--------+
| 3          | 108939 | ✓ 108939 > 50000
| 8          | 87709  | ✓ 87709 > 50000
| 6          | 91796  | ✓ 91796 > 50000
+------------+--------+

-- COUNT calculation:
COUNT(account_id) = 3

-- Query 3 result:
+-------------+----------------+
| category    | accounts_count |
+-------------+----------------+
| High Salary | 3              |
+-------------+----------------+
```

### UNION ALL Final Combination
```sql
Query 1:              Query 2:               Query 3:
+-------------+---+   +----------------+---+   +-------------+---+
| Low Salary  | 1 |   | Average Salary | 0 |   | High Salary | 3 |
+-------------+---+   +----------------+---+   +-------------+---+

                    UNION ALL ↓

Final Result:
+----------------+----------------+
| category       | accounts_count |
+----------------+----------------+
| Low Salary     | 1              |
| Average Salary | 0              |
| High Salary    | 3              |
+----------------+----------------+
```

## Critical Design Decisions

### Why Three Separate Queries?
```sql
-- Advantage: Guaranteed complete coverage
-- Each query always produces exactly one row
-- COUNT() never fails to return a result
-- Zero counts are preserved as explicit rows
```

### Alternative Approaches and Their Problems

#### Approach 1: Single Query with GROUP BY
```sql
-- ❌ Incomplete solution
SELECT 
    CASE 
        WHEN income < 20000 THEN 'Low Salary'
        WHEN income BETWEEN 20000 AND 50000 THEN 'Average Salary'
        ELSE 'High Salary'
    END as category,
    COUNT(*) as accounts_count
FROM Accounts
GROUP BY category;

-- Problem: Missing categories don't appear in result
-- Example: If no "Average Salary" accounts exist, no row is generated
```

#### Approach 2: Conditional Aggregation
```sql
-- ✅ Works but less readable
SELECT 
    'Low Salary' as category,
    SUM(CASE WHEN income < 20000 THEN 1 ELSE 0 END) as accounts_count
FROM Accounts
UNION ALL
SELECT 
    'Average Salary',
    SUM(CASE WHEN income BETWEEN 20000 AND 50000 THEN 1 ELSE 0 END)
FROM Accounts
UNION ALL
SELECT 
    'High Salary',
    SUM(CASE WHEN income > 50000 THEN 1 ELSE 0 END)
FROM Accounts;

-- Analysis:
-- ✅ Correct results
-- ❌ Less efficient (scans table 3 times)
-- ❌ More complex CASE logic
-- ❌ Harder to modify conditions
```

#### Approach 3: Fixed Categories with LEFT JOIN
```sql
-- ✅ Most sophisticated approach
WITH SalaryCategories AS (
    SELECT 'Low Salary' as category, 0 as min_income, 19999 as max_income
    UNION ALL
    SELECT 'Average Salary', 20000, 50000
    UNION ALL
    SELECT 'High Salary', 50001, 999999999
)
SELECT 
    sc.category,
    COUNT(a.account_id) as accounts_count
FROM SalaryCategories sc
LEFT JOIN Accounts a ON a.income BETWEEN sc.min_income AND sc.max_income
GROUP BY sc.category;

-- Analysis:
-- ✅ Guaranteed complete coverage
-- ✅ Single table scan
-- ❌ More complex structure
-- ❌ Harder to understand and maintain
```

## Edge Cases and Robustness

### Edge Case 1: Empty Accounts Table
```sql
Input: No rows in Accounts table
Processing:
- Query 1: COUNT(*) = 0 → ('Low Salary', 0)
- Query 2: COUNT(*) = 0 → ('Average Salary', 0)
- Query 3: COUNT(*) = 0 → ('High Salary', 0)
Result: All categories show 0 counts ✓
```

### Edge Case 2: Boundary Values
```sql
Input: account with income = 20000 (boundary)
Processing: income >= 20000 AND income <= 50000 → TRUE
Result: Correctly classified as 'Average Salary' ✓

Input: account with income = 50000 (boundary)
Processing: income >= 20000 AND income <= 50000 → TRUE
Result: Correctly classified as 'Average Salary' ✓
```

### Edge Case 3: Single Category Population
```sql
Input: All accounts in one category (e.g., all High Salary)
Processing:
- Low Salary: COUNT(*) = 0
- Average Salary: COUNT(*) = 0
- High Salary: COUNT(*) = actual_count
Result: Zero categories still appear with count 0 ✓
```

### Edge Case 4: Extreme Income Values
```sql
Input: income = 0 (minimum possible)
Processing: 0 < 20000 → TRUE
Result: Correctly classified as 'Low Salary' ✓

Input: income = 999999999 (very high)
Processing: 999999999 > 50000 → TRUE
Result: Correctly classified as 'High Salary' ✓
```

## Performance Analysis

### Time Complexity: O(3n) = O(n)
```sql
-- Each category query: O(n) - full table scan with filter
-- Three queries total: O(3n)
-- UNION ALL combination: O(1) - simple concatenation
-- Overall: O(n) - linear time complexity
```

### Space Complexity: O(1)
```sql
-- Each query result: O(1) - exactly one row
-- UNION ALL result: O(3) = O(1) - exactly three rows
-- Overall: O(1) - constant space
```

### Index Optimization
```sql
-- Recommended index:
CREATE INDEX idx_accounts_income ON Accounts(income);

-- Benefits:
-- WHERE income < 20000 → Index range scan
-- WHERE income >= 20000 AND income <= 50000 → Index range scan
-- WHERE income > 50000 → Index range scan
-- Significant performance improvement for large tables
```

## Real-World Applications

### Customer Segmentation
```sql
-- RFM Analysis: Recency, Frequency, Monetary segments
SELECT 'High Value' as segment, COUNT(*) FROM customers WHERE total_spent > 10000
UNION ALL
SELECT 'Medium Value', COUNT(*) FROM customers WHERE total_spent BETWEEN 1000 AND 10000
UNION ALL
SELECT 'Low Value', COUNT(*) FROM customers WHERE total_spent < 1000;
```

### Inventory Management
```sql
-- Stock level analysis
SELECT 'Critical' as stock_level, COUNT(*) FROM products WHERE quantity < 10
UNION ALL
SELECT 'Low', COUNT(*) FROM products WHERE quantity BETWEEN 10 AND 50
UNION ALL
SELECT 'Normal', COUNT(*) FROM products WHERE quantity > 50;
```

### Sales Performance
```sql
-- Sales target achievement
SELECT 'Exceeds Target' as performance, COUNT(*) FROM sales WHERE amount > target * 1.1
UNION ALL
SELECT 'Meets Target', COUNT(*) FROM sales WHERE amount BETWEEN target * 0.9 AND target * 1.1
UNION ALL
SELECT 'Below Target', COUNT(*) FROM sales WHERE amount < target * 0.9;
```

### Risk Assessment
```sql
-- Credit risk categories
SELECT 'High Risk' as risk_level, COUNT(*) FROM loans WHERE credit_score < 600
UNION ALL
SELECT 'Medium Risk', COUNT(*) FROM loans WHERE credit_score BETWEEN 600 AND 750
UNION ALL
SELECT 'Low Risk', COUNT(*) FROM loans WHERE credit_score > 750;
```

## SQL Concepts Demonstrated

### Advanced Query Composition
```sql
-- UNION ALL for combining independent result sets
-- Multiple WHERE conditions with different logic
-- Literal values in SELECT clauses
-- Consistent column naming across queries
```

### Aggregation Patterns
```sql
-- COUNT() function behavior with empty result sets
-- Guaranteed row generation from aggregate functions
-- Filtering before aggregation for efficiency
```

### Categorical Data Analysis
```sql
-- Fixed category enumeration
-- Boundary condition handling
-- Complete coverage requirements
-- Zero-value preservation
```

## Best Practices Demonstrated

### 1. **Requirement Analysis**
```sql
-- Clear understanding: "All categories must appear"
-- Correct tool selection: UNION ALL for guaranteed coverage
-- Edge case consideration: Zero counts must be preserved
```

### 2. **Code Organization**
```sql
-- Clear comments explaining each category
-- Consistent formatting across queries
-- Logical query ordering (Low → Average → High)
-- Meaningful column aliases
```

### 3. **Performance Consciousness**
```sql
-- Efficient filtering with appropriate WHERE clauses
-- UNION ALL over UNION (no unnecessary deduplication)
-- Index-friendly query structure
-- Minimal table scans
```

### 4. **Maintainability**
```sql
-- Easy to modify category boundaries
-- Simple to add new categories (add UNION ALL + query)
-- Independent queries reduce cross-dependencies
-- Clear business logic expression
```

## Common Pitfalls Avoided

### Pitfall 1: Missing Zero Categories
```sql
-- ❌ Incomplete approach
SELECT category, COUNT(*) FROM 
(SELECT CASE WHEN income < 20000 THEN 'Low' ... END as category FROM Accounts)
GROUP BY category;
-- Problem: Categories with no data disappear
```

### Pitfall 2: Complex CASE Logic
```sql
-- ❌ Hard to maintain
SELECT 
    SUM(CASE WHEN income < 20000 THEN 1 ELSE 0 END) as low,
    SUM(CASE WHEN income BETWEEN 20000 AND 50000 THEN 1 ELSE 0 END) as avg,
    SUM(CASE WHEN income > 50000 THEN 1 ELSE 0 END) as high
FROM Accounts;
-- Problem: Doesn't match required output format
```

### Pitfall 3: Incorrect Boundary Handling
```sql
-- ❌ Wrong boundary logic
WHERE income <= 20000  -- Should be < 20000
WHERE income > 20000 AND income < 50000  -- Should include 50000
```

## Minor Code Quality Notes

### Typo Correction
```sql
-- Original comment:
-- Query for the 'Low Slary' category

-- Corrected:
-- Query for the 'Low Salary' category
```

### Consistency Improvements
```sql
-- Make all aliases consistent:
'High Salary' as category  -- (lowercase 'as')
count(account_id) as accounts_count  -- (lowercase 'count')

-- Should be:
'High Salary' AS category  -- (uppercase 'AS')
COUNT(account_id) AS accounts_count  -- (uppercase 'COUNT')
```

## Why This Solution is Optimal

### 1. **Correctness Guarantee**
```sql
-- Mathematical certainty: Each query produces exactly one row
-- Business requirement: All categories always appear
-- Edge case coverage: Zero counts handled properly
```

### 2. **Simplicity and Clarity**
```sql
-- Direct mapping: One query per business category
-- Readable logic: Category conditions are explicit
-- Standard patterns: Uses basic SQL constructs effectively
```

### 3. **Performance Efficiency**
```sql
-- Optimal filtering: Each query uses precise WHERE conditions
-- Efficient combination: UNION ALL avoids unnecessary processing
-- Index-friendly: Straightforward range conditions
```

### 4. **Maintainability**
```sql
-- Easy modifications: Change conditions in individual queries
-- Simple extensions: Add new categories with additional UNION ALL
-- Independent testing: Each category can be verified separately
```

This solution exemplifies how thoughtful problem analysis leads to elegant SQL solutions. The UNION ALL approach ensures complete coverage while maintaining simplicity and performance, making it an excellent pattern for categorical analysis problems.