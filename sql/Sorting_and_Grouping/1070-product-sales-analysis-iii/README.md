# 1070. Product Sales Analysis III - Solution Explanation

## Problem Overview

Write a solution to find all sales that occurred in the **first year** each product was sold.

**Requirements:**
- For each `product_id`, identify the earliest year it appears in the Sales table
- Return **all sales entries** for that product in that earliest year
- Return columns: `product_id`, `first_year`, `quantity`, and `price`

**Table Schema:**
```sql
Sales table:
+-------------+-------+
| Column Name | Type  |
+-------------+-------+
| sale_id     | int   |
| product_id  | int   |
| year        | int   |
| quantity    | int   |
| price       | int   |
+-------------+-------+
-- (sale_id, year) is the primary key
-- A product may have multiple sales entries in the same year
```

**Example:**
```sql
Input: 
+---------+------------+------+----------+-------+
| sale_id | product_id | year | quantity | price |
+---------+------------+------+----------+-------+ 
| 1       | 100        | 2008 | 10       | 5000  |
| 2       | 100        | 2009 | 12       | 5000  |
| 7       | 200        | 2011 | 15       | 9000  |
+---------+------------+------+----------+-------+

Output: 
+------------+------------+----------+-------+
| product_id | first_year | quantity | price |
+------------+------------+----------+-------+ 
| 100        | 2008       | 10       | 5000  |
| 200        | 2011       | 15       | 9000  |
+------------+------------+----------+-------+
```

## Key Insights

### Problem Analysis
```sql
-- Challenge: Find "first year" for each product
-- Complexity: Multiple sales may exist in the same year
-- Goal: Return ALL sales from each product's first year
```

### Window Function Approach
```sql
-- Use RANK() to identify first year sales
-- PARTITION BY product_id → Group by product
-- ORDER BY year ASC → Earliest year gets rank 1
-- Filter WHERE rnk = 1 → Get all first-year sales
```

## Solution Approach

Our solution uses **Window Functions with CTE** for clean separation of ranking and filtering:

```sql
WITH
    RankedSales AS (
        -- Use a window function to rank each sale by year for each product.
        SELECT
            product_id,
            year,
            quantity,
            price,
            RANK() OVER(PARTITION BY product_id ORDER BY year ASC) AS rnk
        FROM
            Sales
    )
-- Select only the sales that have a rank of 1 (the first year)
SELECT
    product_id,
    year AS first_year,
    quantity,
    price
FROM
    RankedSales
WHERE
    rnk = 1;
```

**Strategy:**
1. **CTE with Window Function**: Rank sales by year within each product
2. **RANK() Function**: Handle potential ties (multiple sales in first year)
3. **Partition by Product**: Group ranking by `product_id`
4. **Filter Rank 1**: Select only first-year sales

## Step-by-Step Breakdown

### Step 1: Understanding the Window Function
```sql
RANK() OVER(PARTITION BY product_id ORDER BY year ASC) AS rnk
```

**Component Analysis:**

#### PARTITION BY product_id
```sql
-- Groups the data by product_id
-- Ranking resets for each product
-- Example:
-- Product 100: Rankings within product 100 only
-- Product 200: Rankings within product 200 only
```

#### ORDER BY year ASC
```sql
-- Orders by year in ascending order within each partition
-- Earliest year gets rank 1
-- Later years get higher ranks (2, 3, etc.)
```

#### RANK() vs ROW_NUMBER() vs DENSE_RANK()
```sql
-- RANK(): If ties exist, leaves gaps (1, 1, 3, 4)
-- ROW_NUMBER(): No ties, sequential (1, 2, 3, 4)  
-- DENSE_RANK(): If ties exist, no gaps (1, 1, 2, 3)

-- For this problem: RANK() is appropriate
-- Multiple sales in same year should all get rank 1
```

### Step 2: CTE (Common Table Expression)
```sql
WITH RankedSales AS (
    -- Window function query
)
```

**Benefits of CTE:**
- **Readability**: Separates ranking logic from filtering
- **Maintainability**: Easy to modify ranking criteria
- **Debugging**: Can test CTE independently
- **Performance**: Often optimized by query planner

### Step 3: Filtering and Selection
```sql
SELECT
    product_id,
    year AS first_year,
    quantity,
    price
FROM
    RankedSales
WHERE
    rnk = 1;
```

**Key Points:**
- **Alias year AS first_year**: Match required output format
- **WHERE rnk = 1**: Get only first-year sales
- **All columns**: Return complete sales information

## Detailed Execution Trace

### Example Dataset Analysis

#### Input Data
```sql
Sales table:
+---------+------------+------+----------+-------+
| sale_id | product_id | year | quantity | price |
+---------+------------+------+----------+-------+ 
| 1       | 100        | 2008 | 10       | 5000  |
| 2       | 100        | 2009 | 12       | 5000  |
| 7       | 200        | 2011 | 15       | 9000  |
+---------+------------+------+----------+-------+
```

#### Step 1: Window Function Application

**CTE RankedSales Result:**
```sql
+------------+------+----------+-------+-----+
| product_id | year | quantity | price | rnk |
+------------+------+----------+-------+-----+
| 100        | 2008 | 10       | 5000  | 1   |  ← First year for product 100
| 100        | 2009 | 12       | 5000  | 2   |  ← Second year for product 100
| 200        | 2011 | 15       | 9000  | 1   |  ← First year for product 200
+------------+------+----------+-------+-----+
```

**Ranking Process:**
```sql
-- For product_id = 100:
-- 2008 → rank 1 (earliest year)
-- 2009 → rank 2 (second year)

-- For product_id = 200:  
-- 2011 → rank 1 (earliest and only year)
```

#### Step 2: Filtering WHERE rnk = 1

**Final Result:**
```sql
+------------+------------+----------+-------+
| product_id | first_year | quantity | price |
+------------+------------+----------+-------+ 
| 100        | 2008       | 10       | 5000  |  ← Only rank 1 for product 100
| 200        | 2011       | 15       | 9000  |  ← Only rank 1 for product 200
+------------+------------+----------+-------+
```

### Complex Example: Multiple Sales in First Year

#### Input with Multiple First-Year Sales
```sql
+---------+------------+------+----------+-------+
| sale_id | product_id | year | quantity | price |
+---------+------------+------+----------+-------+ 
| 1       | 100        | 2008 | 10       | 5000  |
| 8       | 100        | 2008 | 5        | 3000  |  ← Another sale in 2008
| 2       | 100        | 2009 | 12       | 5000  |
| 7       | 200        | 2011 | 15       | 9000  |
+---------+------------+------+----------+-------+
```

#### CTE Result with Ties
```sql
+------------+------+----------+-------+-----+
| product_id | year | quantity | price | rnk |
+------------+------+----------+-------+-----+
| 100        | 2008 | 10       | 5000  | 1   |  ← First year, sale 1
| 100        | 2008 | 5        | 3000  | 1   |  ← First year, sale 2 (same rank!)
| 100        | 2009 | 12       | 5000  | 2   |  ← Second year
| 200        | 2011 | 15       | 9000  | 1   |  ← First year for product 200
+------------+------+----------+-------+-----+
```

#### Final Result - Both First-Year Sales
```sql
+------------+------------+----------+-------+
| product_id | first_year | quantity | price |
+------------+------------+----------+-------+ 
| 100        | 2008       | 10       | 5000  |  ← First sale in first year
| 100        | 2008       | 5        | 3000  |  ← Second sale in first year
| 200        | 2011       | 15       | 9000  |
+------------+------------+----------+-------+
```

**Key Insight**: RANK() correctly handles multiple sales in the same year by giving them the same rank.

## Alternative Solutions Comparison

### Solution 1: Subquery with MIN()
```sql
SELECT 
    s.product_id,
    s.year AS first_year,
    s.quantity,
    s.price
FROM Sales s
WHERE s.year = (
    SELECT MIN(year) 
    FROM Sales s2 
    WHERE s2.product_id = s.product_id
);
```

**Analysis:**
- ✅ **Intuitive**: Direct approach using MIN() to find first year
- ✅ **Correct**: Handles multiple sales in first year properly
- ❌ **Performance**: Correlated subquery can be slower for large datasets
- ❌ **Readability**: Less clear for complex scenarios

### Solution 2: Self-Join Approach
```sql
SELECT DISTINCT
    s1.product_id,
    s1.year AS first_year,
    s1.quantity,
    s1.price
FROM Sales s1
INNER JOIN (
    SELECT 
        product_id, 
        MIN(year) AS min_year
    FROM Sales
    GROUP BY product_id
) s2 ON s1.product_id = s2.product_id 
    AND s1.year = s2.min_year;
```

**Analysis:**
- ✅ **Performance**: Can be efficient with proper indexing
- ✅ **Clear separation**: Logic separated into two distinct parts
- ❌ **Complexity**: More verbose and complex
- ❌ **DISTINCT needed**: May produce duplicates without DISTINCT

### Solution 3: EXISTS with Subquery
```sql
SELECT 
    product_id,
    year AS first_year,
    quantity,
    price
FROM Sales s1
WHERE NOT EXISTS (
    SELECT 1 
    FROM Sales s2 
    WHERE s2.product_id = s1.product_id 
      AND s2.year < s1.year
);
```

**Analysis:**
- ✅ **Logical**: "No earlier year exists" approach
- ✅ **Flexible**: Easy to modify conditions
- ❌ **Performance**: NOT EXISTS can be slower than window functions
- ❌ **Complexity**: Less intuitive logic flow

## Why Our Solution is Optimal

### 1. **Performance Efficiency**
```sql
-- Window functions are optimized in modern SQL engines
-- Single table scan with partitioning
-- No correlated subqueries or multiple joins
-- Efficient for large datasets
```

### 2. **Readability and Maintainability**
```sql
-- CTE clearly separates ranking from filtering
-- Self-documenting with descriptive names
-- Easy to modify ranking criteria if needed
-- Clear logical flow
```

### 3. **Correctness and Robustness**
```sql
-- RANK() properly handles ties (multiple sales in same year)
-- Window function ensures all first-year sales are included
-- No risk of missing data due to grouping issues
```

### 4. **Scalability**
```sql
-- Efficient for large datasets
-- Window functions leverage database optimizations
-- Single pass through data with partitioning
```

## Performance Considerations

### Index Recommendations
```sql
-- Optimal index for this query:
CREATE INDEX idx_sales_product_year ON Sales(product_id, year);

-- This index supports:
-- 1. PARTITION BY product_id (grouping)
-- 2. ORDER BY year ASC (sorting within partition)
-- 3. Efficient filtering in WHERE clause
```

### Query Execution Plan
```sql
-- Expected execution plan:
-- 1. Index scan on (product_id, year)
-- 2. Window function calculation with partitioning
-- 3. Filter on rank = 1
-- 4. Return result set

-- No expensive operations like:
-- - Full table scans
-- - Nested loops for correlated subqueries
-- - Complex joins
```

### Performance Characteristics
```sql
-- Time Complexity: O(n log n) for sorting within partitions
-- Space Complexity: O(n) for intermediate CTE results
-- Very efficient for typical sales data volumes
```

## Edge Cases and Robustness

### Edge Case 1: Single Product, Single Year
```sql
Input:
| product_id | year | quantity | price |
| 100        | 2008 | 10       | 5000  |

Output:
| product_id | first_year | quantity | price |
| 100        | 2008       | 10       | 5000  |

-- Works correctly: Only sale gets rank 1
```

### Edge Case 2: Multiple Products, Same First Year
```sql
Input:
| product_id | year | quantity | price |
| 100        | 2008 | 10       | 5000  |
| 200        | 2008 | 15       | 9000  |

Output:
| product_id | first_year | quantity | price |
| 100        | 2008       | 10       | 5000  |
| 200        | 2008       | 15       | 9000  |

-- Works correctly: Each product handled independently
```

### Edge Case 3: No Sales Data
```sql
Input: Empty Sales table

Output: Empty result set

-- Works correctly: Window function handles empty input gracefully
```

### Edge Case 4: Identical Years for All Sales
```sql
Input:
| product_id | year | quantity | price |
| 100        | 2008 | 10       | 5000  |
| 100        | 2008 | 12       | 6000  |
| 100        | 2008 | 8        | 4000  |

Output:
| product_id | first_year | quantity | price |
| 100        | 2008       | 10       | 5000  |
| 100        | 2008       | 12       | 6000  |
| 100        | 2008       | 8        | 4000  |

-- Works correctly: All sales get rank 1, all are returned
```

## SQL Concepts Demonstrated

### Window Functions Mastery
```sql
-- PARTITION BY: Grouping data for window operations
-- ORDER BY: Defining sort order within partitions
-- RANK(): Handling ties appropriately
-- Window function vs. GROUP BY differences
```

### CTE (Common Table Expression) Benefits
```sql
-- Code organization and readability
-- Intermediate result naming and reuse
-- Complex query decomposition
-- Debugging and testing capabilities
```

### Ranking Function Selection
```sql
-- RANK() vs ROW_NUMBER() vs DENSE_RANK()
-- When to use each ranking function
-- Handling ties in ranking scenarios
-- Performance implications of different functions
```

## Real-World Applications

### Business Intelligence
```sql
-- Customer acquisition analysis (first purchase year)
-- Product launch tracking (initial sales performance)
-- Market entry analysis (first year in new markets)
```

### Data Analytics
```sql
-- Time series analysis (baseline establishment)
-- Cohort analysis (first interaction identification)
-- Performance benchmarking (initial metrics capture)
```

### Reporting Requirements
```sql
-- Executive dashboards (launch year summaries)
-- Product lifecycle reports (inception data)
-- Sales performance tracking (initial results)
```

## Best Practices Demonstrated

### 1. **Proper Window Function Usage**
```sql
-- Correct partitioning for business logic
-- Appropriate ordering for ranking requirements
-- Right ranking function for tie handling
```

### 2. **CTE for Code Organization**
```sql
-- Logical separation of concerns
-- Improved readability and maintainability
-- Easier testing and debugging
```

### 3. **Column Aliasing**
```sql
-- year AS first_year: Match output requirements
-- Descriptive CTE and column names
-- Self-documenting code structure
```

### 4. **Efficient Query Structure**
```sql
-- Single table access in CTE
-- Minimal data transformation
-- Optimized for database engine processing
```

### 5. **Comprehensive Comments**
```sql
-- Explain window function purpose
-- Document CTE logic
-- Clarify filtering criteria
```

This solution exemplifies modern SQL best practices, demonstrating efficient use of window functions and CTEs to solve complex analytical problems. The approach showcases how to handle ranking scenarios with proper tie management while maintaining optimal performance and code clarity essential for production database environments.