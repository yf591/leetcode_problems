# 1164. Product Price at a Given Date - Solution Explanation

## Problem Overview

Find the price of each product on **2019-08-16**. If a product had no price changes on or before this date, the default price is **10**.

**Table Schema:**
```sql
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
```

**Expected Output:**
```sql
+------------+-------+
| product_id | price |
+------------+-------+
| 1          | 35    | ← Latest price on/before 2019-08-16
| 2          | 50    | ← Latest price on/before 2019-08-16  
| 3          | 10    | ← Default price (no changes before date)
+------------+-------+
```

## Key Insights

### Two Distinct Business Cases
```sql
-- Case 1: Products WITH price changes on/before target date
-- → Find the MOST RECENT price change

-- Case 2: Products WITHOUT price changes on/before target date  
-- → Apply DEFAULT price of 10
```

### Point-in-Time Data Challenge
```sql
-- Challenge: Historical data with multiple price changes per product
-- Goal: Reconstruct the "state" at a specific point in time
-- Solution: Time-based filtering with aggregation
```

### UNION Strategy for Complete Coverage
```sql
-- Approach: Handle each case separately, then combine
-- Benefit: Optimized logic for each scenario
-- Result: Comprehensive coverage without overlap
```

## Solution Approach

Our solution uses **UNION of Two Targeted Queries** to handle different scenarios:

```sql
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
```

**Strategy:**
1. **Part 1**: Find products with changes on/before target date → Get latest price
2. **Part 2**: Find products with NO changes on/before target date → Apply default price
3. **UNION**: Combine results for complete coverage
4. **Composite key filtering**: Use (product_id, change_date) for precise row selection

## Step-by-Step Breakdown

### Part 1: Latest Price for Products with Changes

#### Main Query Structure
```sql
SELECT
    product_id,
    new_price AS price
FROM
    Products
WHERE
    (product_id, change_date) IN (subquery)
```

**Composite Key Filtering:**
- `(product_id, change_date) IN (...)` - Multi-column condition
- Precisely selects rows matching both product AND latest change date
- Eliminates need for complex JOIN conditions

#### Subquery: Finding Latest Change Dates
```sql
SELECT
    product_id,
    MAX(change_date)
FROM
    Products
WHERE
    change_date <= '2019-08-16'
GROUP BY
    product_id
```

**Subquery Logic:**
1. **Filter by date**: `change_date <= '2019-08-16'` - Only consider relevant changes
2. **Group by product**: `GROUP BY product_id` - Process each product separately  
3. **Find latest**: `MAX(change_date)` - Get most recent change date per product

### Part 2: Default Price for Products without Changes

```sql
SELECT
    product_id,
    10 AS price
FROM
    Products
GROUP BY
    product_id
HAVING
    MIN(change_date) > '2019-08-16'
```

**Logic Explanation:**
1. **Group by product**: `GROUP BY product_id` - Analyze each product's history
2. **Find earliest change**: `MIN(change_date)` - Get first change date per product
3. **Filter condition**: `MIN(change_date) > '2019-08-16'` - First change is AFTER target date
4. **Default price**: `10 AS price` - Apply default for qualifying products

**Why MIN(change_date) Works:**
```sql
-- If MIN(change_date) > target_date
-- → ALL change_dates > target_date  
-- → NO changes on or before target_date
-- → Product qualifies for default price
```

## Detailed Execution Analysis

### Input Data Breakdown
```sql
Products:
+------------+-----------+-------------+
| product_id | new_price | change_date |
+------------+-----------+-------------+
| 1          | 20        | 2019-08-14  | ← Before target
| 2          | 50        | 2019-08-14  | ← Before target
| 1          | 30        | 2019-08-15  | ← Before target
| 1          | 35        | 2019-08-16  | ← On target date
| 2          | 65        | 2019-08-17  | ← After target
| 3          | 20        | 2019-08-18  | ← After target
+------------+-----------+-------------+

Target Date: 2019-08-16
```

### Part 1 Execution Flow

#### Step 1: Subquery Date Filtering
```sql
WHERE change_date <= '2019-08-16':
+------------+-----------+-------------+
| product_id | new_price | change_date |
+------------+-----------+-------------+
| 1          | 20        | 2019-08-14  |
| 2          | 50        | 2019-08-14  |
| 1          | 30        | 2019-08-15  |
| 1          | 35        | 2019-08-16  |
+------------+-----------+-------------+
```

#### Step 2: GROUP BY and MAX Aggregation
```sql
GROUP BY product_id:
- Product 1: [2019-08-14, 2019-08-15, 2019-08-16]
- Product 2: [2019-08-14]

MAX(change_date) results:
+------------+-------------+
| product_id | max_date    |
+------------+-------------+
| 1          | 2019-08-16  |
| 2          | 2019-08-14  |
+------------+-------------+
```

#### Step 3: Main Query IN Condition
```sql
(product_id, change_date) IN ((1, '2019-08-16'), (2, '2019-08-14'))

Matching rows:
+------------+-----------+-------------+
| product_id | new_price | change_date |
+------------+-----------+-------------+
| 1          | 35        | 2019-08-16  | ← Matches (1, '2019-08-16')
| 2          | 50        | 2019-08-14  | ← Matches (2, '2019-08-14')
+------------+-----------+-------------+
```

#### Part 1 Result
```sql
+------------+-------+
| product_id | price |
+------------+-------+
| 1          | 35    |
| 2          | 50    |
+------------+-------+
```

### Part 2 Execution Flow

#### Step 1: GROUP BY Analysis
```sql
All products grouped:
- Product 1: [2019-08-14, 2019-08-15, 2019-08-16]
- Product 2: [2019-08-14, 2019-08-17]  
- Product 3: [2019-08-18]
```

#### Step 2: MIN(change_date) Calculation
```sql
+------------+-------------+
| product_id | min_date    |
+------------+-------------+
| 1          | 2019-08-14  |
| 2          | 2019-08-14  |
| 3          | 2019-08-18  |
+------------+-------------+
```

#### Step 3: HAVING Condition Evaluation
```sql
MIN(change_date) > '2019-08-16':
- Product 1: 2019-08-14 > 2019-08-16 → FALSE ✗
- Product 2: 2019-08-14 > 2019-08-16 → FALSE ✗
- Product 3: 2019-08-18 > 2019-08-16 → TRUE ✓

Only Product 3 qualifies for default price
```

#### Part 2 Result
```sql
+------------+-------+
| product_id | price |
+------------+-------+
| 3          | 10    |
+------------+-------+
```

### UNION Final Combination
```sql
Part 1:                    Part 2:
+------------+-------+      +------------+-------+
| product_id | price |      | product_id | price |
+------------+-------+  +   +------------+-------+
| 1          | 35    |      | 3          | 10    |
| 2          | 50    |      +------------+-------+
+------------+-------+

UNION Result:
+------------+-------+
| product_id | price |
+------------+-------+
| 1          | 35    |
| 2          | 50    |
| 3          | 10    |
+------------+-------+
```

## Critical Design Decisions

### Composite Key IN Condition Strategy
```sql
-- Alternative approach (less efficient):
SELECT p1.product_id, p1.new_price
FROM Products p1
WHERE p1.change_date = (
    SELECT MAX(p2.change_date)
    FROM Products p2
    WHERE p2.product_id = p1.product_id
    AND p2.change_date <= '2019-08-16'
)

-- Our approach (more efficient):
WHERE (product_id, change_date) IN (subquery)
-- Single subquery execution vs. correlated subquery per row
```

### HAVING vs WHERE for Aggregated Conditions
```sql
-- HAVING: Applied after GROUP BY (correct for our case)
GROUP BY product_id
HAVING MIN(change_date) > '2019-08-16'

-- WHERE: Applied before GROUP BY (would be incorrect)
WHERE MIN(change_date) > '2019-08-16'  -- Error: aggregate in WHERE
GROUP BY product_id
```

### UNION vs LEFT JOIN Approach
```sql
-- Our UNION approach:
-- Clear separation of logic
-- Each part optimized for its specific case
-- Easy to understand and debug

-- Alternative LEFT JOIN approach:
-- More complex with CASE statements
-- Potential performance issues with large datasets
-- Harder to maintain and understand
```

## Alternative Solutions Comparison

### Solution 1: Window Function Approach
```sql
WITH RankedPrices AS (
    SELECT 
        product_id,
        new_price,
        change_date,
        ROW_NUMBER() OVER (
            PARTITION BY product_id 
            ORDER BY 
                CASE WHEN change_date <= '2019-08-16' THEN change_date END DESC
        ) as rn
    FROM Products
),
AllProducts AS (
    SELECT DISTINCT product_id FROM Products
)
SELECT 
    ap.product_id,
    COALESCE(rp.new_price, 10) as price
FROM AllProducts ap
LEFT JOIN RankedPrices rp ON ap.product_id = rp.product_id AND rp.rn = 1;
```

**Analysis:**
- ✅ **Single query**: No UNION needed
- ✅ **Flexible**: Easy to change target date
- ❌ **Complexity**: Window functions + CASE + COALESCE
- ❌ **Performance**: More complex execution plan
- ❌ **Readability**: Harder to understand logic flow

### Solution 2: Correlated Subquery Approach
```sql
SELECT 
    DISTINCT product_id,
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM Products p2 
            WHERE p2.product_id = p.product_id 
            AND p2.change_date <= '2019-08-16'
        )
        THEN (
            SELECT new_price FROM Products p3
            WHERE p3.product_id = p.product_id 
            AND p3.change_date <= '2019-08-16'
            ORDER BY p3.change_date DESC 
            LIMIT 1
        )
        ELSE 10
    END as price
FROM Products p;
```

**Analysis:**
- ✅ **Logic clarity**: CASE statement makes conditions explicit
- ✅ **Single result set**: No UNION required
- ❌ **Performance**: Multiple correlated subqueries per row
- ❌ **Efficiency**: Repeated table scans
- ❌ **Scalability**: Poor performance with large datasets

### Solution 3: Self-JOIN with Aggregation
```sql
SELECT 
    p1.product_id,
    COALESCE(p2.new_price, 10) as price
FROM (SELECT DISTINCT product_id FROM Products) p1
LEFT JOIN (
    SELECT 
        product_id,
        new_price,
        change_date
    FROM Products p
    WHERE change_date <= '2019-08-16'
    AND change_date = (
        SELECT MAX(change_date)
        FROM Products p2
        WHERE p2.product_id = p.product_id
        AND p2.change_date <= '2019-08-16'
    )
) p2 ON p1.product_id = p2.product_id;
```

**Analysis:**
- ✅ **Comprehensive**: Handles all products in one query
- ❌ **Complexity**: Nested subqueries in JOIN condition
- ❌ **Performance**: Correlated subquery in JOIN
- ❌ **Maintainability**: Complex nested structure

## Why Our Solution is Optimal

### 1. **Clear Problem Decomposition**
```sql
-- Each part addresses exactly one business case
-- Part 1: Products with changes → Latest price
-- Part 2: Products without changes → Default price
-- Clean separation of concerns
```

### 2. **Optimal Performance Characteristics**
```sql
-- Each part uses efficient aggregation patterns
-- No correlated subqueries
-- Minimal table scans
-- Database optimizer-friendly structure
```

### 3. **Maintainable and Debuggable**
```sql
-- Easy to test each part independently
-- Clear comments explain business logic
-- Straightforward to modify for different requirements
-- Standard SQL patterns
```

### 4. **Complete Coverage Guarantee**
```sql
-- Mathematical certainty: every product falls into exactly one case
-- Case 1: MIN(change_date) <= target_date
-- Case 2: MIN(change_date) > target_date
-- No overlap, no gaps
```

## Performance Analysis

### Time Complexity: O(n + k log k)
```sql
-- Part 1 subquery: O(n) scan + O(k log k) grouping (k = unique products)
-- Part 1 main query: O(n) scan with hash lookup
-- Part 2: O(n) scan + O(k) grouping
-- Overall: O(n + k log k) - efficient for typical datasets
```

### Space Complexity: O(k)
```sql
-- Subquery results: O(k) - one row per product
-- GROUP BY hash tables: O(k)
-- UNION result set: O(k)
-- Overall: O(k) - scales with number of products, not total rows
```

### Index Optimization Opportunities
```sql
-- Recommended indexes:
CREATE INDEX idx_products_date_product ON Products(change_date, product_id);
CREATE INDEX idx_products_product_date ON Products(product_id, change_date);

-- Benefits:
-- Fast date range filtering
-- Efficient GROUP BY operations
-- Quick composite key lookups
```

## Edge Cases and Robustness

### Edge Case 1: Product with Single Change on Target Date
```sql
Input: product_id=1, change_date='2019-08-16', new_price=25
Processing:
- Part 1: change_date <= '2019-08-16' ✓ → MAX = '2019-08-16' → price = 25
- Part 2: MIN(change_date) = '2019-08-16' > '2019-08-16' ✗ → excluded
Result: price = 25 ✓
```

### Edge Case 2: Product with Multiple Changes on Same Date
```sql
Input: Multiple rows with same product_id and change_date
Processing:
- Subquery returns same (product_id, date) pair
- Main query may return multiple rows
- Business decision needed: should this be allowed?
Note: Real systems typically prevent this with unique constraints
```

### Edge Case 3: All Products Changed After Target Date
```sql
Input: All change_dates > '2019-08-16'
Processing:
- Part 1: WHERE change_date <= '2019-08-16' → empty set
- Part 2: All products have MIN(change_date) > '2019-08-16' → all get price = 10
Result: All products with default price ✓
```

### Edge Case 4: Product with Changes Before and After Target Date
```sql
Input: product_id=1, dates=['2019-08-10', '2019-08-20'], prices=[15, 25]
Processing:
- Part 1: Only '2019-08-10' satisfies date filter → price = 15
- Part 2: MIN = '2019-08-10' <= '2019-08-16' → excluded
Result: price = 15 ✓
```

### Edge Case 5: Empty Products Table
```sql
Input: No rows in Products table
Processing:
- Part 1: Empty subquery → empty result
- Part 2: No groups → empty result
- UNION: Empty result
Result: Empty result set ✓
```

## Real-World Applications

### E-commerce Price Management
```sql
-- Historical pricing for financial reporting
-- Price at specific dates for order processing
-- Audit trails for price changes
-- Promotional pricing effective dates
```

### Financial Data Systems
```sql
-- Stock prices at market close dates
-- Interest rates effective on specific dates
-- Currency exchange rates for historical transactions
-- Asset valuations for portfolio reports
```

### Inventory and Supply Chain
```sql
-- Product costs for COGS calculations
-- Vendor pricing effective dates
-- Contract pricing with date ranges
-- Cost basis for inventory valuation
```

### SaaS and Subscription Systems
```sql
-- Subscription pricing at renewal dates
-- Feature availability based on plan changes
-- Billing rate changes over time
-- Usage tier pricing effective dates
```

## SQL Concepts Demonstrated

### Advanced Query Composition
```sql
-- UNION for combining distinct result sets
-- Composite key conditions with IN operator
-- Subqueries for data preparation
-- Aggregation with filtering (HAVING)
```

### Temporal Data Management
```sql
-- Point-in-time data reconstruction
-- Historical state queries
-- Time-based filtering strategies
-- Default value handling for missing data
```

### Performance Optimization Patterns
```sql
-- Efficient aggregation techniques
-- Avoiding correlated subqueries
-- Leveraging composite indexes
-- Query structure for optimizer efficiency
```

### Business Logic Implementation
```sql
-- Multiple scenario handling
-- Complete data coverage strategies
-- Default value application
-- Data integrity considerations
```

## Best Practices Demonstrated

### 1. **Problem Analysis and Decomposition**
```sql
-- Clear identification of business scenarios
-- Logical separation of different cases
-- Appropriate tool selection for each case
-- Comprehensive solution coverage
```

### 2. **SQL Code Organization**
```sql
-- Clear comments explaining business logic
-- Logical query structure with meaningful aliases
-- Readable formatting and indentation
-- Self-documenting code patterns
```

### 3. **Performance Considerations**
```sql
-- Efficient aggregation patterns
-- Avoiding expensive operations (correlated subqueries)
-- Index-friendly query structures
-- Scalable solution design
```

### 4. **Maintainability and Flexibility**
```sql
-- Easy to modify for different target dates
-- Clear separation between data preparation and business logic
-- Standard SQL patterns for portability
-- Debugging-friendly structure
```

This solution exemplifies how thoughtful problem decomposition can lead to elegant, efficient, and maintainable SQL solutions. The UNION approach provides clear separation of concerns while ensuring complete coverage of all business scenarios, making it an excellent pattern for temporal data management problems.