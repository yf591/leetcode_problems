# 180. Consecutive Numbers - Solution Explanation

## Problem Overview

Find all numbers that appear at least **three times consecutively** in the Logs table.

**Table Schema:**
```sql
Logs table:
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| num         | varchar |
+-------------+---------+
-- id is the primary key (autoincrement starting from 1)
-- Consecutive means sequential id values with same num
```

**Example:**
```sql
Input: 
+----+-----+
| id | num |
+----+-----+
| 1  | 1   |  ← Start of consecutive 1s
| 2  | 1   |  ← Middle of consecutive 1s  
| 3  | 1   |  ← End of consecutive 1s (3 times total)
| 4  | 2   |
| 5  | 1   |
| 6  | 2   |
| 7  | 2   |  ← Only 2 consecutive 2s (not enough)
+----+-----+

Output: 
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+
```

## Key Insights

### Understanding "Consecutive"
```sql
-- Consecutive = Sequential id values with same num
-- id sequence: 1,2,3 with num: '1','1','1' → Consecutive ✓
-- id sequence: 1,3,4 with num: '1','1','1' → Not consecutive ✗ (missing id=2)
-- id sequence: 5,6,7 with num: '2','2','2' → Consecutive ✓
```

### Window Function Strategy
```sql
-- Challenge: How to compare current row with next two rows?
-- Solution: Use LEAD() to bring "future values" to current row
-- Result: Compare 3 values in a single row condition
```

### LEAD Function Power
```sql
-- LEAD(column, offset) OVER (ORDER BY ...)
-- Brings values from subsequent rows to current row
-- Enables multi-row comparison in single WHERE clause
```

## Solution Approach

Our solution uses **Window Functions with LEAD** to create a sliding window comparison:

```sql
WITH
    NumberLeads AS (
        -- Create a temporary table with the current number and the next two numbers.
        SELECT
            num,
            LEAD(num, 1) OVER (ORDER BY id) AS next_num,
            LEAD(num, 2) OVER (ORDER BY id) AS next_next_num
        FROM
            Logs
    )
-- Select the distinct numbers where all three are the same.
SELECT DISTINCT
    num AS ConsecutiveNums
FROM
    NumberLeads
WHERE
    num = next_num and num = next_next_num;
```

**Strategy:**
1. **CTE with LEAD functions**: Bring next two values to current row
2. **Three-value comparison**: Check if current, next, and next-next are identical
3. **DISTINCT filtering**: Remove duplicate results for same number
4. **Automatic edge handling**: LEAD returns NULL at boundaries

## Step-by-Step Breakdown

### Step 1: CTE with Window Functions
```sql
WITH NumberLeads AS (
    SELECT
        num,
        LEAD(num, 1) OVER (ORDER BY id) AS next_num,
        LEAD(num, 2) OVER (ORDER BY id) AS next_next_num
    FROM Logs
)
```

**LEAD Function Mechanics:**
```sql
-- LEAD(num, 1): Get num value from next row (id + 1)
-- LEAD(num, 2): Get num value from row after next (id + 2)  
-- ORDER BY id: Define "next" based on id sequence
-- Result: Each row contains 3 consecutive values
```

**Why ORDER BY id is Critical:**
```sql
-- Without ORDER BY id: LEAD uses arbitrary row order
-- With ORDER BY id: LEAD follows logical sequence
-- Ensures "consecutive" means sequential id values
```

### Step 2: LEAD Function Execution

#### Input Data Processing
```sql
Original Logs:
+----+-----+
| id | num |
+----+-----+
| 1  | 1   |
| 2  | 1   |  
| 3  | 1   |
| 4  | 2   |
| 5  | 1   |
| 6  | 2   |
| 7  | 2   |
+----+-----+
```

#### LEAD(num, 1) Calculation
```sql
-- For each row, get num from next row:
Row 1 (id=1): LEAD(num,1) = Row 2's num = '1'
Row 2 (id=2): LEAD(num,1) = Row 3's num = '1'  
Row 3 (id=3): LEAD(num,1) = Row 4's num = '2'
Row 4 (id=4): LEAD(num,1) = Row 5's num = '1'
Row 5 (id=5): LEAD(num,1) = Row 6's num = '2'
Row 6 (id=6): LEAD(num,1) = Row 7's num = '2'
Row 7 (id=7): LEAD(num,1) = NULL (no next row)
```

#### LEAD(num, 2) Calculation
```sql
-- For each row, get num from row two positions ahead:
Row 1 (id=1): LEAD(num,2) = Row 3's num = '1'
Row 2 (id=2): LEAD(num,2) = Row 4's num = '2'
Row 3 (id=3): LEAD(num,2) = Row 5's num = '1'  
Row 4 (id=4): LEAD(num,2) = Row 6's num = '2'
Row 5 (id=5): LEAD(num,2) = Row 7's num = '2'
Row 6 (id=6): LEAD(num,2) = NULL (no row at id=8)
Row 7 (id=7): LEAD(num,2) = NULL (no row at id=9)
```

#### Complete CTE Result
```sql
NumberLeads:
+-----+----------+---------------+
| num | next_num | next_next_num |
+-----+----------+---------------+
| 1   | 1        | 1             | ← Row 1: All three are '1'
| 1   | 1        | 2             | ← Row 2: Third value different
| 1   | 2        | 1             | ← Row 3: Second value different
| 2   | 1        | 2             | ← Row 4: All different
| 1   | 2        | 2             | ← Row 5: First value different  
| 2   | 2        | NULL          | ← Row 6: Has NULL
| 2   | NULL     | NULL          | ← Row 7: Has NULLs
+-----+----------+---------------+
```

### Step 3: WHERE Clause Filtering
```sql
WHERE num = next_num AND num = next_next_num
```

**Condition Analysis for Each Row:**
```sql
Row 1: '1' = '1' AND '1' = '1' → TRUE ✓
Row 2: '1' = '1' AND '1' = '2' → FALSE ✗  
Row 3: '1' = '2' AND '1' = '1' → FALSE ✗
Row 4: '2' = '1' AND '2' = '2' → FALSE ✗
Row 5: '1' = '2' AND '1' = '2' → FALSE ✗
Row 6: '2' = '2' AND '2' = NULL → FALSE ✗ (NULL comparison)
Row 7: '2' = NULL AND '2' = NULL → FALSE ✗ (NULL comparison)
```

**Filtered Result:**
```sql
+-----+
| num |
+-----+
| 1   | ← Only Row 1 satisfies condition
+-----+
```

### Step 4: DISTINCT and Final Selection
```sql
SELECT DISTINCT num AS ConsecutiveNums
```

**DISTINCT Purpose:**
```sql
-- Scenario: Number appears 4+ times consecutively
-- Example: 1,1,1,1 → First two rows both satisfy condition
-- DISTINCT ensures each number appears only once in result
```

**Final Output:**
```sql
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+
```

## Detailed Execution Analysis

### Complex Example: Multiple Consecutive Patterns
```sql
Input:
+----+-----+
| id | num |
+----+-----+
| 1  | 1   |
| 2  | 1   |  
| 3  | 1   |
| 4  | 1   | ← 4 consecutive 1s
| 5  | 2   |
| 6  | 3   |
| 7  | 3   |
| 8  | 3   | ← 3 consecutive 3s
| 9  | 3   | ← 4 consecutive 3s
+----+-----+
```

#### CTE Result Analysis
```sql
NumberLeads:
+-----+----------+---------------+
| num | next_num | next_next_num |
+-----+----------+---------------+
| 1   | 1        | 1             | ← ✓ Condition satisfied  
| 1   | 1        | 1             | ← ✓ Condition satisfied
| 1   | 1        | 2             | ← ✗ Third different
| 1   | 2        | 3             | ← ✗ Second & third different
| 2   | 3        | 3             | ← ✗ First different
| 3   | 3        | 3             | ← ✓ Condition satisfied
| 3   | 3        | 3             | ← ✓ Condition satisfied  
| 3   | 3        | NULL          | ← ✗ Has NULL
| 3   | NULL     | NULL          | ← ✗ Has NULLs
+-----+----------+---------------+
```

#### WHERE Filtering Result
```sql
Rows satisfying condition: 1, 1, 3, 3
Before DISTINCT: [1, 1, 3, 3]
After DISTINCT: [1, 3]
```

#### Final Output
```sql
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
| 3               |
+-----------------+
```

## Critical Design Decisions

### Why LEAD Instead of LAG?
```sql
-- LEAD approach (our solution):
-- Current row compares with future rows
-- Natural left-to-right reading

-- LAG approach (alternative):
-- Current row compares with past rows  
-- Requires different mental model
-- Equivalent functionality but different perspective
```

#### LAG Alternative Implementation
```sql
WITH NumberLags AS (
    SELECT 
        num,
        LAG(num, 1) OVER (ORDER BY id) AS prev_num,
        LAG(num, 2) OVER (ORDER BY id) AS prev_prev_num
    FROM Logs
)
SELECT DISTINCT num AS ConsecutiveNums
FROM NumberLags
WHERE num = prev_num AND num = prev_prev_num;
```

### Why ORDER BY id is Essential
```sql
-- Without ORDER BY:
LEAD(num, 1) OVER () -- Uses arbitrary row order
-- Could return: id=5's num for id=1's LEAD
-- Breaks consecutive logic

-- With ORDER BY id:
LEAD(num, 1) OVER (ORDER BY id) -- Uses id sequence
-- Returns: id=2's num for id=1's LEAD  
-- Maintains consecutive meaning
```

### Automatic NULL Handling
```sql
-- Edge case: Last two rows
-- LEAD returns NULL when no subsequent rows exist
-- NULL = 'any_value' always evaluates to FALSE
-- Automatically excludes boundary cases
-- No special handling required
```

## Alternative Solutions Comparison

### Solution 1: Self-JOIN Approach
```sql
SELECT DISTINCT l1.num AS ConsecutiveNums
FROM Logs l1
JOIN Logs l2 ON l1.id = l2.id - 1 AND l1.num = l2.num
JOIN Logs l3 ON l1.id = l3.id - 2 AND l1.num = l3.num;
```

**Analysis:**
- ✅ **Intuitive**: Direct representation of "consecutive"
- ✅ **Clear logic**: Explicit id relationships
- ❌ **Performance**: Multiple table scans and joins
- ❌ **Complexity**: Complex ON conditions
- ❌ **Scalability**: Poor performance with large datasets

### Solution 2: Gap and Islands Pattern
```sql
WITH GroupedNums AS (
    SELECT 
        num,
        id - ROW_NUMBER() OVER (PARTITION BY num ORDER BY id) AS grp
    FROM Logs
),
ConsecutiveCounts AS (
    SELECT 
        num,
        COUNT(*) as consecutive_count
    FROM GroupedNums
    GROUP BY num, grp
)
SELECT DISTINCT num AS ConsecutiveNums
FROM ConsecutiveCounts
WHERE consecutive_count >= 3;
```

**Analysis:**
- ✅ **Powerful**: Handles any consecutive count requirement
- ✅ **Scalable**: Efficient for large datasets
- ✅ **Flexible**: Easy to change from 3 to N consecutive
- ❌ **Complex**: Difficult to understand gap-and-islands logic
- ❌ **Overkill**: Too sophisticated for this specific problem

### Solution 3: Correlated Subquery
```sql
SELECT DISTINCT num AS ConsecutiveNums
FROM Logs l1
WHERE EXISTS (
    SELECT 1 FROM Logs l2 
    WHERE l2.id = l1.id + 1 AND l2.num = l1.num
) AND EXISTS (
    SELECT 1 FROM Logs l3
    WHERE l3.id = l1.id + 2 AND l3.num = l1.num
);
```

**Analysis:**
- ✅ **Readable**: Clear EXISTS logic
- ✅ **Intuitive**: Directly checks for next two occurrences
- ❌ **Performance**: Multiple subquery executions
- ❌ **Efficiency**: Correlated subqueries are typically slower
- ❌ **Scalability**: Performance degrades with data size

## Why Our Solution is Optimal

### 1. **Performance Efficiency**
```sql
-- Single table scan with window function
-- Window functions are highly optimized in modern databases
-- No expensive JOINs or correlated subqueries
-- Excellent execution plan characteristics
```

### 2. **Code Simplicity**
```sql
-- Clear and concise logic
-- Easy to understand and maintain
-- Minimal code complexity
-- Self-documenting structure
```

### 3. **Scalability and Flexibility**
```sql
-- Easy to modify for N consecutive occurrences:
-- Add LEAD(num, 3), LEAD(num, 4), etc.
-- Extend WHERE clause with additional conditions
-- No fundamental structural changes required
```

### 4. **Robust Edge Case Handling**
```sql
-- Automatic NULL handling at boundaries
-- No special cases for small datasets
-- Works correctly with any data distribution
-- Built-in protection against edge conditions
```

## Performance Analysis

### Time Complexity: O(n log n)
```sql
-- Window function requires sorting: O(n log n)
-- WHERE clause evaluation: O(n)
-- DISTINCT operation: O(n) with hash-based approach
-- Overall: O(n log n) dominated by sorting requirement
```

### Space Complexity: O(n)
```sql
-- CTE storage: O(n)
-- Window function buffer: O(n)  
-- DISTINCT hash table: O(k) where k = unique numbers
-- Overall: O(n) linear space usage
```

### Real-World Performance
```sql
-- Modern database window function optimizations
-- Efficient memory management for large datasets
-- Good performance characteristics for typical data sizes
-- Scales well compared to JOIN-based alternatives
```

## Edge Cases and Robustness

### Edge Case 1: Empty Table
```sql
Input: Empty Logs table
CTE Result: Empty result set
Final Output: Empty result set
✓ Handled correctly
```

### Edge Case 2: Single Row
```sql
Input: One row only
LEAD functions return NULL
WHERE condition fails (NULL comparisons)
Output: Empty result set
✓ Handled correctly - need at least 3 rows for 3 consecutive
```

### Edge Case 3: Two Rows Only
```sql
Input: Two rows only
LEAD(num, 2) returns NULL for all rows
WHERE condition fails
Output: Empty result set  
✓ Handled correctly
```

### Edge Case 4: All Same Numbers
```sql
Input: All rows have identical num values
Multiple rows satisfy WHERE condition
DISTINCT removes duplicates
Output: Single number
✓ Handled correctly
```

### Edge Case 5: No Consecutive Patterns
```sql
Input: Alternating or non-consecutive patterns
No rows satisfy three-way equality condition
Output: Empty result set
✓ Handled correctly
```

### Edge Case 6: Exactly Three Consecutive
```sql
Input: Exactly 3 consecutive occurrences
First row of the sequence satisfies condition
Output: Contains the number
✓ Handled correctly
```

### Edge Case 7: More Than Three Consecutive
```sql
Input: 4+ consecutive occurrences
Multiple rows satisfy condition (overlap)
DISTINCT ensures single result per number
Output: Each qualifying number appears once
✓ Handled correctly with DISTINCT
```

## Real-World Applications

### Log Analysis and Monitoring
```sql
-- System failure detection: Same error appearing consecutively
-- Performance monitoring: Consecutive slow response times
-- Security analysis: Repeated failed login attempts
-- Network monitoring: Consecutive packet losses
```

### Time Series Data Analysis
```sql
-- Financial data: Consecutive price movements
-- Sensor data: Consecutive readings above/below threshold
-- Weather patterns: Consecutive days of specific conditions
-- IoT monitoring: Device status patterns
```

### Quality Control and Manufacturing
```sql
-- Production line: Consecutive defective products
-- Quality metrics: Consecutive failed tests
-- Equipment monitoring: Consecutive warning signals
-- Process control: Consecutive out-of-spec measurements
```

### Business Intelligence
```sql
-- Customer behavior: Consecutive purchases of same product
-- Sales analysis: Consecutive periods of same performance
-- User engagement: Consecutive login patterns
-- Marketing: Consecutive campaign response patterns
```

## SQL Concepts Demonstrated

### Window Functions Mastery
```sql
-- LEAD function with multiple offsets
-- ORDER BY clause importance in window functions
-- Window function performance characteristics
-- Practical application of analytical functions
```

### CTE (Common Table Expression) Usage
```sql
-- Query structure organization
-- Intermediate result set creation
-- Code readability improvement
-- Complex query decomposition
```

### Comparison Operations and NULL Handling
```sql
-- Multiple equality conditions with AND
-- Automatic NULL handling in comparisons
-- DISTINCT for duplicate removal
-- Proper column aliasing
```

### Advanced SELECT Patterns
```sql
-- Window functions in CTEs
-- Filtering after window function application
-- Complex WHERE conditions
-- Result set transformation
```

## Best Practices Demonstrated

### 1. **Clear Query Structure**
```sql
-- Well-commented CTE explaining purpose
-- Logical separation of data preparation and filtering
-- Meaningful column aliases (ConsecutiveNums)
-- Readable formatting and indentation
```

### 2. **Efficient Algorithm Design**
```sql
-- Single-pass solution with window functions
-- Avoiding expensive self-joins
-- Leveraging database engine optimizations
-- Minimizing data movement and processing
```

### 3. **Robust Edge Case Handling**
```sql
-- Automatic boundary condition management
-- NULL-safe comparisons
-- No special case code required
-- Consistent behavior across all input scenarios
```

### 4. **Maintainable Code Patterns**
```sql
-- Self-documenting variable names
-- Standard SQL patterns and idioms
-- Easy to modify for different requirements
-- Clear separation of concerns
```

This solution exemplifies how modern SQL window functions can elegantly solve complex analytical problems. The LEAD function approach transforms a potentially complex multi-join problem into a clean, efficient, and maintainable solution that handles all edge cases gracefully while delivering optimal performance.